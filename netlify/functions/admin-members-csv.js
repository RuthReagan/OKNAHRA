// GET /api/admin-members-csv[?all=1]  -> CSV of current (Active) members; all=1 includes everyone
const { sessionFromEvent, NO_STORE } = require("./lib/auth");
const { fetchMembers, isActive } = require("./lib/sources");

// Prevent spreadsheet formula injection from member-entered text.
const cell = (v) => {
  let s = v == null ? "" : String(v);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
};

exports.handler = async (event) => {
  let who;
  try { who = sessionFromEvent(event); } catch { who = null; }
  if (!who) return { statusCode: 401, headers: { "Content-Type": "text/plain", ...NO_STORE }, body: "Sign in to download." };

  let data;
  try { data = await fetchMembers(); } catch (e) {
    return { statusCode: 502, headers: { "Content-Type": "text/plain", ...NO_STORE }, body: "Member data is unavailable right now." };
  }
  const all = (event.queryStringParameters || {}).all === "1";
  const rows = data.members.filter((m) => all || isActive(m)).sort((a, b) => a.name.localeCompare(b.name));
  const head = ["Name", "Company / Organization", "Email", "Phone", "Membership Tier", "Status", "Join Date", "Renewal Date", "Amount Paid", "Payment Method", "Notes"];
  const lines = [head.map(cell).join(",")].concat(
    rows.map((m) => [m.name, m.company, m.email, m.phone, m.tier, m.status, m.joined, m.renews, m.amount == null ? "" : m.amount, m.payment, m.notes].map(cell).join(","))
  );
  const stamp = new Date().toISOString().slice(0, 10);
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="oknahra-${all ? "all-members" : "current-members"}-${stamp}.csv"`,
      ...NO_STORE,
    },
    body: "﻿" + lines.join("\r\n") + "\r\n",
  };
};
