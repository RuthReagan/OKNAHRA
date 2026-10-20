// GET /api/auth-verify?token=...  -> sets the session cookie and redirects to /admin/
const { verify, sign, cookieHeader, SESSION_TTL_MS, siteUrl, NO_STORE } = require("./lib/auth");

exports.handler = async (event) => {
  const token = (event.queryStringParameters || {}).token;
  const email = verify("login", token);
  if (!email) {
    return { statusCode: 302, headers: { Location: `${siteUrl()}/admin/?error=expired`, ...NO_STORE } };
  }
  const session = sign("session", email, SESSION_TTL_MS);
  return {
    statusCode: 302,
    headers: { Location: `${siteUrl()}/admin/`, ...NO_STORE },
    multiValueHeaders: { "Set-Cookie": [cookieHeader(session, Math.floor(SESSION_TTL_MS / 1000))] },
  };
};
