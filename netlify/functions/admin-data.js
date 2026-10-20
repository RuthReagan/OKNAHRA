// GET /api/admin-data  (signed-in board members only)
const { sessionFromEvent, json } = require("./lib/auth");
const { fetchMembers, summarizeMembers, fetchCharges, summarizeRevenue } = require("./lib/sources");

async function safe(fn) {
  try { return { ok: true, data: await fn() }; }
  catch (e) {
    if (e.message !== "not_configured") console.error("admin-data:", e.message);
    return { ok: false, error: e.message === "not_configured" ? "not_configured" : "unavailable" };
  }
}

exports.handler = async (event) => {
  let who;
  try { who = sessionFromEvent(event); } catch (e) { console.error(e.message); return json(500, { ok: false, error: "server_not_configured" }); }
  if (!who) return json(401, { ok: false, error: "signed_out" });

  const [revenue, members] = await Promise.all([
    safe(async () => summarizeRevenue(await fetchCharges())),
    safe(async () => summarizeMembers(await fetchMembers())),
  ]);
  return json(200, { ok: true, user: who, generatedAt: new Date().toISOString(), revenue, members });
};
