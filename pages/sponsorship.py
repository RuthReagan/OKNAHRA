def _tier_card(t):
    feats = "\n".join(f"<li>{f}</li>" for f in t["features"])
    return f"""
      <div class="price-card">
        <h3>{t['name']}</h3>
        <div class="price-amount" style="font-size:1.3rem;">{t['price']}</div>
        <ul>{feats}</ul>
        <a class="btn btn-outline btn-block" href="/contact.html">Inquire</a>
      </div>"""


def render(tiers):
    cards = "\n".join(_tier_card(t) for t in tiers)
    return f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div>
      <p class="breadcrumb"><a href="/index.html">Home</a> / Sponsorship</p>
      <span class="eyebrow">Partner with OKNAHRA</span>
      <h1>Sponsorship &amp; Partnership</h1>
      <p style="max-width:60ch; color:var(--color-text-muted); font-size:1.05rem;">
        Sponsorship dollars fund the Summit, member programming, and OKNAHRA's
        advocacy work on behalf of HR professionals across Oklahoma's tribal
        nations.
      </p>
    </div>
    <div class="media-banner">
      <img src="/images/stock/sponsorship-support.jpg" alt="OKNAHRA partner meeting" loading="eager">
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="pricing-grid">
      {cards}
    </div>
    <p class="placeholder-note" style="margin-top:28px;">
      Tier pricing is pending confirmation from the board (a prior "Corporate — $500/yr" tier was flagged for removal).
      Once amounts are final, either list a Stripe Payment Link per tier here (same pattern as
      the Membership page) or keep this page as an inquiry form if sponsorships are custom-quoted.
    </p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Current Partners</span>
      <h2>Thank you to our partners</h2>
    </div>
    <div class="sponsor-logos">
      <img src="/images/logos/nnahra.png" alt="NNAHRA">
      <img src="/images/logos/shrm.png" alt="SHRM">
      <img src="/images/logos/hrci.png" alt="HR Certification Institute">
    </div>
  </div>
</section>
"""
