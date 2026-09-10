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
    <p style="max-width:56ch; margin:0 auto 16px; color:var(--color-text-muted);">
      $100 per posting — <strong>free for sponsors</strong> and <strong>$50 for members</strong>.
      Already a member or sponsor? Email us to confirm your status and we'll send you a discount
      code to use at checkout.
    </p>
    <a class="btn btn-primary" href="#" aria-disabled="true">List a Job — $100 (set up in Stripe)</a>
    <p class="placeholder-note" style="max-width:56ch; margin:20px auto 0; text-align:left;">
      Pricing plan (not yet built): one $100 Stripe Payment Link, with two Stripe promo codes —
      a $50-off code for members, a 100%-off code for sponsors — checked and issued by staff
      against the Airtable Members/Sponsors base before someone posts. No self-service login yet;
      that's the Phase 3 member portal work (see project notes). Once decided, replace the button
      below the same way Membership's Payment Link was wired up.
    </p>
  </div>
</section>
"""
