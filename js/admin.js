// OKNAHRA board portal. All data comes from /api/admin-data (session-protected).
// Every value from Stripe/Airtable is inserted with textContent, never as HTML.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
  var usd2 = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
  var money = function (cents) { return (cents % 100 === 0 ? usd : usd2).format(cents / 100); };
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var monthLabel = function (k, long) { var p = k.split("-"); return MONTHS[+p[1] - 1] + (long ? " " + p[0] : ""); };

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); return n; }
  function show(n, on) { n.hidden = !on; }

  function tile(label, value, sub) {
    var t = el("div", "adm-tile");
    t.appendChild(el("span", "adm-tile-label", label));
    t.appendChild(el("strong", "adm-tile-value", value));
    if (sub) t.appendChild(el("span", "adm-tile-sub", sub));
    return t;
  }

  function table(node, head, rows, numCols) {
    clear(node);
    var thead = el("thead"), tr = el("tr");
    head.forEach(function (h, i) { var th = el("th", numCols && numCols.indexOf(i) > -1 ? "num" : "", h); th.scope = "col"; tr.appendChild(th); });
    thead.appendChild(tr); node.appendChild(thead);
    var tb = el("tbody");
    rows.forEach(function (r) {
      var row = el("tr");
      r.forEach(function (c, i) { row.appendChild(el("td", numCols && numCols.indexOf(i) > -1 ? "num" : "", c)); });
      tb.appendChild(row);
    });
    node.appendChild(tb);
  }

  // Horizontal share bars: one hue, length encodes magnitude, value printed at the end.
  function shareBars(node, items, fmt) {
    clear(node);
    if (!items.length) { node.appendChild(el("p", "adm-muted", "Nothing to show yet.")); return; }
    var max = Math.max.apply(null, items.map(function (i) { return i.v; })) || 1;
    items.forEach(function (i) {
      var row = el("div", "adm-bar-row");
      row.appendChild(el("span", "adm-bar-label", i.label));
      var track = el("span", "adm-bar-track"), fill = el("span", "adm-bar-fill");
      fill.style.width = Math.max(2, (i.v / max) * 100) + "%";
      track.appendChild(fill); row.appendChild(track);
      row.appendChild(el("span", "adm-bar-val", fmt(i.v)));
      node.appendChild(row);
    });
  }

  // ---------- Chart ----------
  function niceMax(v) {
    if (v <= 0) return 100;
    var p = Math.pow(10, Math.floor(Math.log10(v))), n = v / p;
    var step = n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10;
    return step * p;
  }
  function drawChart(months) {
    var svg = clear($("adm-chart")), tip = $("adm-tip");
    var NS = "http://www.w3.org/2000/svg";
    var W = 720, H = 280, L = 56, R = 12, T = 14, B = 34;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    var data = months.slice(-12);
    var top = niceMax(Math.max.apply(null, data.map(function (m) { return m.cents; }).concat([1])));
    var ticks = 4;
    var y = function (c) { return T + (H - T - B) * (1 - c / top); };
    function node(name, attrs, text) {
      var n = document.createElementNS(NS, name);
      for (var k in attrs) n.setAttribute(k, attrs[k]);
      if (text != null) n.textContent = text;
      svg.appendChild(n); return n;
    }
    for (var i = 0; i <= ticks; i++) {
      var v = (top / ticks) * i, yy = y(v);
      node("line", { x1: L, x2: W - R, y1: yy, y2: yy, class: i === 0 ? "adm-axis" : "adm-grid" });
      node("text", { x: L - 8, y: yy + 4, "text-anchor": "end", class: "adm-axis-text" }, usd.format(v / 100));
    }
    var slot = (W - L - R) / data.length, bw = Math.min(44, slot - 8);
    data.forEach(function (m, idx) {
      var cx = L + slot * idx + slot / 2, h = Math.max(0, y(0) - y(m.cents));
      var g = node("g", { class: "adm-mark", tabindex: "0", "aria-label": monthLabel(m.month, true) + ": " + money(m.cents) });
      svg.removeChild(g);
      // Wide invisible hit target, then the bar (rounded data end, flat on the baseline).
      var hit = document.createElementNS(NS, "rect");
      hit.setAttribute("x", cx - slot / 2); hit.setAttribute("y", T); hit.setAttribute("width", slot); hit.setAttribute("height", H - T - B); hit.setAttribute("fill", "transparent");
      g.appendChild(hit);
      if (h > 0) {
        var r = Math.min(4, h, bw / 2), x0 = cx - bw / 2, x1 = cx + bw / 2, y0 = y(0), yt = y(m.cents);
        var path = document.createElementNS(NS, "path");
        path.setAttribute("d", "M" + x0 + "," + y0 + "V" + (yt + r) + "Q" + x0 + "," + yt + " " + (x0 + r) + "," + yt + "H" + (x1 - r) + "Q" + x1 + "," + yt + " " + x1 + "," + (yt + r) + "V" + y0 + "Z");
        path.setAttribute("class", "adm-bar-mark");
        g.appendChild(path);
      }
      var lab = document.createElementNS(NS, "text");
      lab.setAttribute("x", cx); lab.setAttribute("y", H - 12); lab.setAttribute("text-anchor", "middle"); lab.setAttribute("class", "adm-axis-text");
      lab.textContent = monthLabel(m.month);
      g.appendChild(lab);
      function on() {
        var box = svg.getBoundingClientRect(), scale = box.width / W;
        tip.textContent = monthLabel(m.month, true) + " — " + money(m.cents);
        tip.hidden = false;
        tip.style.left = Math.min(Math.max(cx * scale, 70), box.width - 70) + "px";
        tip.style.top = Math.max(0, (m.cents ? y(m.cents) : y(0)) * scale - 38) + "px";
      }
      g.addEventListener("mouseenter", on); g.addEventListener("focus", on);
      g.addEventListener("mouseleave", function () { tip.hidden = true; });
      g.addEventListener("blur", function () { tip.hidden = true; });
      svg.appendChild(g);
    });
  }

  // ---------- Sections ----------
  function renderRevenue(res) {
    var msg = $("adm-revenue-msg");
    if (!res.ok) {
      show($("adm-revenue"), false); show(msg, true);
      msg.textContent = res.error === "not_configured" ? "Revenue isn't connected yet. The Stripe read-only key still needs to be added to the site settings." : "Revenue couldn't be loaded from Stripe just now. Refresh in a minute.";
      return;
    }
    show($("adm-revenue"), true); show(msg, false);
    var r = res.data, t = clear($("adm-rev-tiles"));
    t.appendChild(tile("Total revenue", money(r.totalCents), r.refundCents ? "after " + money(r.refundCents) + " refunded" : "all time"));
    t.appendChild(tile("This month", money(r.thisMonthCents), monthLabel(r.thisMonth, true)));
    t.appendChild(tile("Last month", money(r.lastMonthCents), monthLabel(r.lastMonth, true)));
    t.appendChild(tile("Year to date", money(r.ytdCents), r.thisMonth.slice(0, 4)));
    t.appendChild(tile("Payments", String(r.paymentCount), "average " + money(r.avgCents)));
    $("adm-chart-sub").textContent = "Last " + Math.min(12, r.months.length) + " months, paid in Stripe";
    drawChart(r.months);
    table($("adm-month-table"), ["Month", "Revenue"], r.months.slice().reverse().map(function (m) { return [monthLabel(m.month, true), money(m.cents)]; }), [1]);
    shareBars($("adm-kind"), r.byKind.map(function (k) { return { label: k.label, v: k.cents }; }), money);
    table($("adm-recent"), ["Date", "From", "Type", "Amount"], r.recent.map(function (p) { return [p.date, p.who, p.kind, money(p.cents)]; }), [3]);
  }

  var allMembers = [];
  function renderList() {
    var q = $("adm-search").value.trim().toLowerCase(), st = $("adm-status-filter").value;
    var rows = allMembers.filter(function (m) {
      return (!st || (m.status || "Not set") === st) && (!q || [m.name, m.company, m.email].join(" ").toLowerCase().indexOf(q) > -1);
    });
    table($("adm-list"), ["Name", "Organization", "Email", "Tier", "Status", "Joined"], rows.map(function (m) {
      return [m.name || "(no name)", m.company, m.email, m.tier, m.status || "Not set", m.joined];
    }));
    $("adm-list-count").textContent = "Showing " + rows.length + " of " + allMembers.length + " members.";
  }
  function renderMembers(res) {
    var msg = $("adm-members-msg");
    if (!res.ok) {
      show($("adm-members"), false); show(msg, true);
      msg.textContent = res.error === "not_configured" ? "Membership isn't connected yet. The Airtable access token still needs to be added to the site settings." : "Members couldn't be loaded from Airtable just now. Refresh in a minute.";
      return;
    }
    show($("adm-members"), true); show(msg, false);
    var m = res.data, t = clear($("adm-mem-tiles"));
    t.appendChild(tile("Current members", String(m.active), "status Active"));
    t.appendChild(tile("Total on record", String(m.total), m.inactive + " not active"));
    t.appendChild(tile("Joined this month", String(m.newThisMonth)));
    if (m.incompleteRows) t.appendChild(tile("Incomplete rows", String(m.incompleteRows), "blank rows in Airtable, not counted"));
    shareBars($("adm-tier"), m.byTier.map(function (x) { return { label: x.label, v: x.count }; }), String);
    shareBars($("adm-status"), m.byStatus.map(function (x) { return { label: x.label, v: x.count }; }), String);
    allMembers = m.list;
    var sel = $("adm-status-filter");
    while (sel.options.length > 1) sel.remove(1);
    m.byStatus.forEach(function (s) { var o = el("option", "", s.label); o.value = s.label; sel.appendChild(o); });
    renderList();
  }

  // ---------- Boot ----------
  function showLogin() {
    show($("adm-loading"), false); show($("adm-dash"), false); show($("adm-login"), true);
    if (/[?&]error=expired/.test(location.search)) show($("adm-expired"), true);
  }
  function load() {
    fetch("/api/admin-data", { credentials: "same-origin", cache: "no-store" })
      .then(function (r) {
        if (r.status === 401) { showLogin(); return null; }
        if (!r.ok) throw new Error("status " + r.status);
        return r.json();
      })
      .then(function (d) {
        if (!d) return;
        show($("adm-loading"), false); show($("adm-login"), false); show($("adm-dash"), true);
        $("adm-who").textContent = "Signed in as " + d.user;
        renderRevenue(d.revenue); renderMembers(d.members);
        $("adm-stamp").textContent = "Data refreshed " + new Date(d.generatedAt).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }) + ". Reload the page for the latest.";
      })
      .catch(function () {
        $("adm-loading").textContent = "The portal couldn't load. Refresh the page, or try again in a minute.";
      });
  }

  $("adm-login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var email = $("adm-email").value.trim(), msg = $("adm-login-msg"), btn = $("adm-send");
    if (!email) { $("adm-email").focus(); return; }
    btn.disabled = true; btn.textContent = "Sending…";
    fetch("/api/auth-request", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email }) })
      .then(function (r) { return r.json(); })
      .then(function (d) { msg.textContent = d.message || "Check your email for a sign-in link."; })
      .catch(function () { msg.textContent = "That didn't go through. Check your connection and try again."; })
      .then(function () { show(msg, true); btn.disabled = false; btn.textContent = "Email me a sign-in link"; });
  });
  $("adm-logout").addEventListener("click", function () {
    fetch("/api/auth-logout", { method: "POST", credentials: "same-origin" }).then(function () { location.href = "/admin/"; });
  });
  $("adm-search").addEventListener("input", renderList);
  $("adm-status-filter").addEventListener("change", renderList);
  load();
})();
