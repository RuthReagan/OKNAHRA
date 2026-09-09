def _tier_card(t):
    feats = "\n".join(f"<li>{f}</li>" for f in t["features"])
    link = t.get("stripe_link")
    if link:
        is_placeholder = link.startswith("PASTE_")
        if is_placeholder:
            cta = f'<a class="btn btn-primary btn-block" href="#" aria-disabled="true" data-stripe-slot="{link}">Sponsor — set up in Stripe</a>'
        else:
            cta = f'<a class="btn btn-primary btn-block" href="{link}" rel="noopener">Become a Sponsor</a>'
    else:
        cta = '<a class="btn btn-outline btn-block" href="/contact.html">Inquire</a>'
    return f"""
      <div class="price-card">
        <h3>{t['name']}</h3>
        <div class="price-amount" style="font-size:1.3rem;">{t['price']}</div>
        <ul>{feats}</ul>
        {cta}
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
      "Become a Sponsor" buttons are wired for Stripe Payment Links, same pattern as the
      Membership page. Create one Payment Link per tier in the Stripe Dashboard
      (Payment Links → New), then paste each URL into <code>build.py</code> in place of the
      matching <code>PASTE_STRIPE_PAYMENT_LINK_SPONSOR_…</code> placeholder and rebuild.
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
