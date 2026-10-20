const { cookieHeader, json } = require("./lib/auth");
exports.handler = async () => ({
  ...json(200, { ok: true }),
  multiValueHeaders: { "Set-Cookie": [cookieHeader("", 0)] },
});
