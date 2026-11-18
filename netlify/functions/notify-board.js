// POST /api/notify-board   (called by the Airtable "new member" automation)
// Header: x-notify-secret: <NOTIFY_SECRET>
// Body:   { name, company, email, phone, tier, amountPaid, recordUrl }
// Emails the board a task: send the new member a personal welcome from your own address.
// Blank rows (no name, email or company) are ignored so test/blank records never email anyone.
const crypto = require("crypto");
const { allowlist, json } = require("./lib/auth");

const clean = (v, max) => String(v == null ? "" : v).replace(/[\r\n\t]+/g, " ").trim().slice(0, max || 200);
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function same(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(String(b || ""));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function recipients() {
  const list = (process.env.NOTIFY_EMAILS || "").split(/[,;\s]+/).map((s) => s.trim().toLowerCase()).filter(Boolean);
  return list.length ? list : allowlist();
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return json(405, { ok: false, error: "method_not_allowed" });

  const secret = process.env.NOTIFY_SECRET;
  const given = event.headers["x-notify-secret"] || event.headers["X-Notify-Secret"];
  if (!secret || secret.length < 20 || !same(given, secret)) return json(401, { ok: false, error: "unauthorized" });

  let b = {};
  try { b = JSON.parse(event.body || "{}"); } catch { return json(400, { ok: false, error: "bad_json" }); }

  const name = clean(b.name, 120), company = clean(b.company, 160), email = clean(b.email, 254).toLowerCase();
  const phone = clean(b.phone, 40), tier = clean(b.tier, 80), amount = clean(b.amountPaid, 20), recordUrl = clean(b.recordUrl, 300);
  if (!name && !email && !company) return json(200, { ok: true, skipped: "blank_record" });

  const to = recipients();
  const key = process.env.RESEND_API_KEY;
  if (!key || !to.length) return json(500, { ok: false, error: "not_configured" });

  const who = name || company || email;
  const first = (name.split(/\s+/)[0] || "there");
  const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const mailto = validEmail
    ? "mailto:" + encodeURIComponent(email).replace(/%40/g, "@") +
      "?subject=" + encodeURIComponent("Welcome to OKNAHRA") +
      "&body=" + encodeURIComponent(`Hi ${first},\n\nWelcome to OKNAHRA, and thank you for joining. I'm glad to have you with us. If there is anything I can help with, or if you'd like an introduction to other members, just reply to this note.\n\n`)
    : "";
  const lines = [
    ["Name", name], ["Organization", company], ["Email", email], ["Phone", phone],
    ["Membership", tier], ["Amount paid", amount ? "$" + amount.replace(/^\$/, "") : ""],
  ].filter((r) => r[1]);

  const text = [
    `New OKNAHRA member: ${who}`,
    "",
    "YOUR TASK: send them a short, personal welcome email from your own address.",
    "To avoid two people writing, reply-all to this message with \"I've got it\" before you send.",
    "",
    ...lines.map((r) => `${r[0]}: ${r[1]}`),
    ...(recordUrl ? ["", `Airtable record: ${recordUrl}`] : []),
  ].join("\n");

  const rows = lines.map((r) => `<tr><td style="padding:4px 16px 4px 0;color:#6B5E52">${esc(r[0])}</td><td style="padding:4px 0"><strong>${esc(r[1])}</strong></td></tr>`).join("");
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;color:#2B2118;max-width:560px">
<h2 style="margin:0 0 12px">New OKNAHRA member: ${esc(who)}</h2>
<p style="margin:0 0 12px"><strong>Your task:</strong> send them a short, personal welcome email from your own address.</p>
<p style="margin:0 0 16px;color:#6B5E52">To avoid two people writing, reply-all with &ldquo;I&rsquo;ve got it&rdquo; before you send.</p>
<table style="border-collapse:collapse;margin:0 0 18px">${rows}</table>
${mailto ? `<p><a href="${mailto}" style="display:inline-block;background:#D3373C;color:#fff;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:600">Write the welcome email</a></p>` : ""}
${recordUrl ? `<p style="font-size:13px;color:#6B5E52"><a href="${esc(recordUrl)}">Open the Airtable record</a></p>` : ""}
</div>`;

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: process.env.MAIL_FROM || "OKNAHRA Board Portal <no-reply@oknahra.net>",
        to,
        subject: `New OKNAHRA member: ${who}. Please send a personal welcome`,
        text, html,
      }),
    });
    if (!res.ok) throw new Error("Resend " + res.status + " " + (await res.text()).slice(0, 200));
  } catch (err) {
    console.error("notify-board failed:", err.message);
    return json(502, { ok: false, error: "send_failed" });
  }
  return json(200, { ok: true, sent: to.length });
};
