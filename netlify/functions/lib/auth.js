// Shared helpers for the OKNAHRA board portal functions.
// No npm dependencies: only Node built-ins and the platform fetch.
const crypto = require("crypto");

const COOKIE = "oknahra_admin";
const LOGIN_TTL_MS = 15 * 60 * 1000;          // sign-in link lifetime
const SESSION_TTL_MS = 12 * 60 * 60 * 1000;   // signed-in session lifetime

function siteUrl() {
  return (process.env.SITE_URL || "https://oknahra.net").replace(/\/+$/, "");
}

function allowlist() {
  return (process.env.ADMIN_EMAILS || "")
    .split(/[,;\s]+/)
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);
}

function secret() {
  const s = process.env.SESSION_SECRET || "";
  if (s.length < 32) throw new Error("SESSION_SECRET missing or too short (need 32+ characters)");
  return s;
}

const b64 = (buf) => Buffer.from(buf).toString("base64url");

// Signed, expiring token. `kind` keeps a sign-in link from being usable as a session cookie.
function sign(kind, email, ttlMs) {
  const payload = b64(JSON.stringify({ k: kind, e: email, x: Date.now() + ttlMs }));
  const mac = crypto.createHmac("sha256", secret()).update(kind + "." + payload).digest("base64url");
  return payload + "." + mac;
}

function verify(kind, token) {
  if (typeof token !== "string" || token.length > 2000) return null;
  const [payload, mac] = token.split(".");
  if (!payload || !mac) return null;
  const expected = crypto.createHmac("sha256", secret()).update(kind + "." + payload).digest("base64url");
  const a = Buffer.from(mac);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let data;
  try { data = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")); } catch { return null; }
  if (!data || data.k !== kind || typeof data.e !== "string" || !(data.x > Date.now())) return null;
  // Re-check the allowlist on every request, so removing a board member takes effect immediately.
  if (!allowlist().includes(data.e.toLowerCase())) return null;
  return data.e.toLowerCase();
}

function cookieHeader(value, maxAgeSec) {
  return `${COOKIE}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAgeSec}`;
}

function sessionFromEvent(event) {
  const raw = (event.headers && (event.headers.cookie || event.headers.Cookie)) || "";
  const m = raw.split(/;\s*/).find((c) => c.startsWith(COOKIE + "="));
  if (!m) return null;
  return verify("session", m.slice(COOKIE.length + 1));
}

const NO_STORE = { "Cache-Control": "no-store", "X-Robots-Tag": "noindex" };

function json(status, body, extraHeaders) {
  return {
    statusCode: status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...NO_STORE, ...(extraHeaders || {}) },
    body: JSON.stringify(body),
  };
}

// Month key in Oklahoma time, e.g. "2026-10"
const monthFmt = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Chicago", year: "numeric", month: "2-digit" });
function monthKey(unixSeconds) {
  const p = monthFmt.formatToParts(new Date(unixSeconds * 1000));
  return p.find((x) => x.type === "year").value + "-" + p.find((x) => x.type === "month").value;
}

module.exports = {
  LOGIN_TTL_MS, SESSION_TTL_MS, siteUrl, allowlist, sign, verify, cookieHeader,
  sessionFromEvent, json, NO_STORE, monthKey, COOKIE,
};
