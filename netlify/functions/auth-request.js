// POST /api/auth-request  { email }
// If the address is on the board list, emails a 15-minute sign-in link.
// The response is identical either way, so the form can't be used to discover who is on the list.
const { allowlist, sign, siteUrl, json, LOGIN_TTL_MS } = require("./lib/auth");

const GENERIC = { ok: true, message: "If that address is on the board list, a sign-in link is on its way. It expires in 15 minutes." };

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return json(405, { ok: false, error: "method_not_allowed" });

  // Same-origin only.
  const origin = event.headers.origin || event.headers.Origin;
  if (origin && origin.replace(/\/+$/, "") !== siteUrl() && !/^https:\/\/[a-z0-9-]+--[a-z0-9-]+\.netlify\.app$/.test(origin)) {
    return json(403, { ok: false, error: "bad_origin" });
  }

  let email = "";
  try { email = String(JSON.parse(event.body || "{}").email || "").trim().toLowerCase(); } catch { /* ignore */ }
  if (!email || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json(200, GENERIC);

  if (!allowlist().includes(email)) return json(200, GENERIC);

  try {
    const token = sign("login", email, LOGIN_TTL_MS);
    const link = `${siteUrl()}/api/auth-verify?token=${encodeURIComponent(token)}`;
    const key = process.env.RESEND_API_KEY;
    const from = process.env.MAIL_FROM || "OKNAHRA Board Portal <no-reply@oknahra.net>";
    if (!key) throw new Error("RESEND_API_KEY not set");

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from,
        to: [email],
        subject: "Your OKNAHRA board sign-in link",
        text: `Use this link to sign in to the OKNAHRA board portal. It works once you open it and expires in 15 minutes.\n\n${link}\n\nIf you didn't ask for this, you can ignore this email.`,
        html: `<p>Use this link to sign in to the OKNAHRA board portal. It expires in 15 minutes.</p><p><a href="${link}" style="display:inline-block;background:#D3373C;color:#fff;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:600">Sign in to the board portal</a></p><p style="color:#6B5E52;font-size:13px">If you didn't ask for this, you can ignore this email.</p>`,
      }),
    });
    if (!res.ok) throw new Error("Resend " + res.status + " " + (await res.text()).slice(0, 200));
  } catch (err) {
    console.error("auth-request failed:", err.message);
    // Still generic to the caller; the Netlify function log has the detail.
  }
  return json(200, GENERIC);
};
