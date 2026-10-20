"""Board portal shell. Public HTML contains no data: everything is fetched from
/api/admin-data, which only answers to a signed-in board member."""


def render():
    return """
<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="/index.html">Home</a> / Board portal</p>
    <span class="eyebrow">Board members only</span>
    <h1>Board Portal</h1>
  </div>
</section>

<section class="adm" id="adm-root">
  <div class="container">

    <!-- Signed-out view -->
    <div id="adm-login" class="adm-login" hidden>
      <div class="card">
        <h2 style="font-size:1.5rem">Sign in</h2>
        <p class="adm-muted">Enter your board email address and we'll send you a one-time sign-in link. No password needed.</p>
        <p id="adm-expired" class="adm-note adm-note-warn" hidden>That sign-in link has expired or was already used. Request a new one below.</p>
        <form id="adm-login-form" novalidate>
          <div class="form-field">
            <label for="adm-email">Board email address</label>
            <input id="adm-email" name="email" type="email" autocomplete="email" required>
          </div>
          <button class="btn btn-primary btn-block" type="submit" id="adm-send">Email me a sign-in link</button>
        </form>
        <p id="adm-login-msg" class="adm-note" role="status" hidden></p>
      </div>
    </div>

    <!-- Loading -->
    <p id="adm-loading" class="adm-muted" role="status">Loading…</p>

    <!-- Signed-in dashboard -->
    <div id="adm-dash" hidden>
      <div class="adm-bar">
        <p class="adm-muted" id="adm-who"></p>
        <div class="adm-bar-actions">
          <a class="btn btn-gold btn-sm" id="adm-csv" href="/api/admin-members-csv" download>Download current members (CSV)</a>
          <button class="btn btn-outline btn-sm" type="button" id="adm-logout">Sign out</button>
        </div>
      </div>

      <h2 class="adm-h">Revenue</h2>
      <div id="adm-revenue-msg" class="adm-note adm-note-warn" hidden></div>
      <div id="adm-revenue">
        <div class="adm-tiles" id="adm-rev-tiles"></div>
        <div class="adm-panel">
          <div class="adm-panel-head">
            <h3>Revenue by month</h3>
            <span class="adm-muted" id="adm-chart-sub"></span>
          </div>
          <div class="adm-chart-wrap"><svg id="adm-chart" role="img" aria-label="Bar chart of revenue by month"></svg><div class="adm-tip" id="adm-tip" hidden></div></div>
          <details class="adm-table-view">
            <summary>View as table</summary>
            <div class="adm-scroll"><table class="adm-table" id="adm-month-table"></table></div>
          </details>
        </div>
        <div class="adm-two">
          <div class="adm-panel"><h3>Where it comes from</h3><div id="adm-kind"></div></div>
          <div class="adm-panel"><h3>Recent payments</h3><div class="adm-scroll"><table class="adm-table" id="adm-recent"></table></div></div>
        </div>
      </div>

      <h2 class="adm-h">Membership</h2>
      <div id="adm-members-msg" class="adm-note adm-note-warn" hidden></div>
      <div id="adm-members">
        <div class="adm-tiles" id="adm-mem-tiles"></div>
        <div class="adm-two">
          <div class="adm-panel"><h3>Current members by tier</h3><div id="adm-tier"></div></div>
          <div class="adm-panel"><h3>All members by status</h3><div id="adm-status"></div></div>
        </div>
        <div class="adm-panel">
          <div class="adm-panel-head">
            <h3>Member list</h3>
            <div class="adm-filters">
              <label class="visually-hidden" for="adm-search">Search members</label>
              <input id="adm-search" type="search" placeholder="Search name, company, email">
              <label class="visually-hidden" for="adm-status-filter">Filter by status</label>
              <select id="adm-status-filter"><option value="">All statuses</option></select>
            </div>
          </div>
          <div class="adm-scroll"><table class="adm-table" id="adm-list"></table></div>
          <p class="adm-muted" id="adm-list-count"></p>
          <p class="adm-muted"><a id="adm-csv-all" href="/api/admin-members-csv?all=1" download>Download everyone, including inactive (CSV)</a></p>
        </div>
      </div>
      <p class="adm-muted" id="adm-stamp"></p>
    </div>
  </div>
</section>
<script src="/js/admin.js" defer></script>
"""
