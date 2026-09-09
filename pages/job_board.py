def render():
    return """
<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="/index.html">Home</a> / Job Board</p>
    <span class="eyebrow">Careers in Indian Country HR</span>
    <h1>Job Board</h1>
    <p style="max-width:60ch; color:var(--color-text-muted); font-size:1.05rem;">
      Open HR roles with Oklahoma tribal governments and tribal enterprises.
    </p>
  </div>
</section>

<section>
  <div class="container">
    <table class="data-table">
      <thead>
        <tr><th>Position</th><th>Organization</th><th>Location</th><th>Posted</th></tr>
      </thead>
      <tbody>
        <tr><td colspan="4" style="color:var(--color-text-muted);">No open listings yet — check back soon, or list your role below.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section-alt">
  <div class="container" style="text-align:center;">
    <h2>List a job opening</h2>
    <p style="max-width:56ch; margin:0 auto 20px; color:var(--color-text-muted);">
      A $100 listing fee applies per posting. Once a Stripe Payment Link is created for this fee,
      it replaces the button below (same pattern as Membership).
    </p>
    <a class="btn btn-primary" href="#" aria-disabled="true">List a Job — $100 (set up in Stripe)</a>
  </div>
</section>
"""
