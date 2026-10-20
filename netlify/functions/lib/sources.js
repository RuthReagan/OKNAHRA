// Read-only data access: Airtable (members) and Stripe (revenue).
const { monthKey } = require("./auth");

const AIRTABLE_BASE = process.env.AIRTABLE_BASE_ID || "appoyt42BvPPNVDVr";
const AIRTABLE_MEMBERS = process.env.AIRTABLE_MEMBERS_TABLE_ID || "tbl3mSuVM5q31bgd4";

const str = (v) => (Array.isArray(v) ? v.join(", ") : v == null ? "" : typeof v === "object" ? (v.name || "") : String(v));

// ---------------- Members (Airtable) ----------------
async function fetchMembers() {
  const token = process.env.AIRTABLE_TOKEN || process.env.AIRTABLE; // accept either variable name
  if (!token) throw new Error("not_configured");
  const rows = [];
  let offset = "";
  for (let i = 0; i < 30; i++) {
    const url = `https://api.airtable.com/v0/${AIRTABLE_BASE}/${AIRTABLE_MEMBERS}?pageSize=100` + (offset ? `&offset=${encodeURIComponent(offset)}` : "");
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    if (!res.ok) throw new Error("Airtable " + res.status);
    const data = await res.json();
    rows.push(...data.records);
    if (!data.offset) break;
    offset = data.offset;
  }
  const all = rows.map((r) => {
    const f = r.fields || {};
    const amount = f["Amount Paid"];
    return {
      id: r.id,
      name: str(f["Name"]).trim(),
      company: str(f["Company / Organization"]).trim(),
      email: str(f["Email"]).trim(),
      phone: str(f["Phone"]).trim(),
      tier: str(f["Membership Tier"]).trim(),
      status: str(f["Status"]).trim(),
      joined: str(f["Join Date"]).slice(0, 10),
      renews: str(f["Renewal Date"]).slice(0, 10),
      amount: typeof amount === "number" ? amount : amount ? Number(String(amount).replace(/[^0-9.-]/g, "")) || null : null,
      payment: str(f["Payment Method"]).trim(),
      notes: str(f["Notes"]).trim(),
    };
  });
  // A real member row has at least a name, email or organization. Blank test rows are counted separately.
  const members = all.filter((m) => m.name || m.email || m.company);
  return { members, incomplete: all.length - members.length };
}

const isActive = (m) => m.status.toLowerCase() === "active";

function summarizeMembers({ members, incomplete }) {
  const active = members.filter(isActive);
  const nowMonth = monthKey(Date.now() / 1000);
  const tally = (list, key) => {
    const o = {};
    list.forEach((m) => { const k = m[key] || "Not set"; o[k] = (o[k] || 0) + 1; });
    return Object.entries(o).map(([label, count]) => ({ label, count })).sort((a, b) => b.count - a.count);
  };
  return {
    total: members.length,
    active: active.length,
    inactive: members.length - active.length,
    newThisMonth: members.filter((m) => m.joined.slice(0, 7) === nowMonth).length,
    incompleteRows: incomplete,
    byTier: tally(active, "tier"),
    byStatus: tally(members, "status"),
    list: members
      .slice()
      .sort((a, b) => (b.joined || "").localeCompare(a.joined || "") || a.name.localeCompare(b.name)),
  };
}

// ---------------- Revenue (Stripe) ----------------
async function fetchCharges() {
  const key = process.env.STRIPE_READ_KEY;
  if (!key) throw new Error("not_configured");
  const auth = "Basic " + Buffer.from(key + ":").toString("base64");
  const charges = [];
  let after = "";
  for (let i = 0; i < 50; i++) {
    const url = "https://api.stripe.com/v1/charges?limit=100" + (after ? `&starting_after=${after}` : "");
    const res = await fetch(url, { headers: { Authorization: auth } });
    if (!res.ok) throw new Error("Stripe " + res.status);
    const data = await res.json();
    charges.push(...data.data);
    if (!data.has_more || !data.data.length) break;
    after = data.data[data.data.length - 1].id;
  }
  return charges;
}

function summarizeRevenue(charges) {
  const paid = charges.filter((c) => c.paid && c.status === "succeeded" && c.livemode !== false);
  const cents = (c) => (c.amount || 0) - (c.amount_refunded || 0);
  // Categories: any payment of $500+ is a sponsorship (memberships top out at $150, job postings are $100);
  // otherwise a recurring subscription/invoice is a membership and a one-time payment is a job posting.
  const SPONSORSHIP_MIN_CENTS = 50000;
  const kindOf = (c) =>
    (c.amount || 0) >= SPONSORSHIP_MIN_CENTS ? "Sponsorships" : c.invoice ? "Memberships" : "Job postings";
  const now = new Date();
  const thisMonth = monthKey(now.getTime() / 1000);
  const lastMonth = monthKey(new Date(now.getFullYear(), now.getMonth() - 1, 15).getTime() / 1000);
  const year = thisMonth.slice(0, 4);

  const byMonth = {};
  let total = 0, gross = 0, refunds = 0, ytd = 0;
  const byKind = {};
  paid.forEach((c) => {
    const mk = monthKey(c.created);
    byMonth[mk] = (byMonth[mk] || 0) + cents(c);
    total += cents(c); gross += c.amount || 0; refunds += c.amount_refunded || 0;
    if (mk.startsWith(year)) ytd += cents(c);
    const k = kindOf(c);
    byKind[k] = (byKind[k] || 0) + cents(c);
  });

  // Continuous month series, oldest charge -> now (capped at the last 24 months)
  const months = [];
  const first = paid.length ? Math.min(...paid.map((c) => c.created)) : now.getTime() / 1000;
  let [y, m] = monthKey(first).split("-").map(Number);
  const [ey, em] = thisMonth.split("-").map(Number);
  while (y < ey || (y === ey && m <= em)) {
    const k = `${y}-${String(m).padStart(2, "0")}`;
    months.push({ month: k, cents: byMonth[k] || 0 });
    m++; if (m > 12) { m = 1; y++; }
  }

  const recent = paid
    .slice()
    .sort((a, b) => b.created - a.created)
    .slice(0, 12)
    .map((c) => ({
      date: new Date(c.created * 1000).toISOString().slice(0, 10),
      who: (c.billing_details && (c.billing_details.name || c.billing_details.email)) || c.receipt_email || "Stripe customer",
      kind: kindOf(c),
      cents: cents(c),
    }));

  return {
    totalCents: total,
    grossCents: gross,
    refundCents: refunds,
    thisMonthCents: byMonth[thisMonth] || 0,
    lastMonthCents: byMonth[lastMonth] || 0,
    ytdCents: ytd,
    paymentCount: paid.length,
    avgCents: paid.length ? Math.round(total / paid.length) : 0,
    byKind: Object.entries(byKind).map(([label, cents]) => ({ label, cents })).sort((a, b) => b.cents - a.cents),
    months: months.slice(-24),
    recent,
    thisMonth,
    lastMonth,
  };
}

module.exports = { fetchMembers, summarizeMembers, fetchCharges, summarizeRevenue, isActive };
