def _tier_card(t):
    featured = " featured" if t.get("featured") else ""
    feats = "\n".join(f"<li>{f}</li>" for f in t["features"])
    if t.get("stripe_link"):
        is_placeholder = t["stripe_link"].startswith("PASTE_")
        if is_placeholder:
            cta = f'<a class="btn btn-primary btn-block" href="#" aria-disabled="true" data-stripe-slot="{t["stripe_link"]}">Join — set up in Stripe</a>'
        else:
            cta = f'<a class="btn btn-primary btn-block" href="{t["stripe_link"]}" rel="noopener">Join Now</a>'
    else:
        cta = '<a class="btn btn-outline btn-block" href="/contact.html">Contact Us</a>'
    return f"""
      <div class="price-card{featured}">
        <h3>{t['name']}</h3>
        <div class="price-amount">{t['price']} <small>{t['period']}</small></div>
        <p style="font-size:0.9rem; color:var(--color-text-muted);">{t['eligibility']}</p>
        <ul>{feats}</ul>
        {cta}
      </div>"""


def render(tiers):
    cards = "\n".join(_tier_card(t) for t in tiers)
    return f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div>
      <p class="breadcrumb"><a href="/index.html">Home</a> / Membership</p>
      <span class="eyebrow">Membership</span>
      <h1>Join OKNAHRA</h1>
      <p style="max-width:60ch; color:var(--color-text-muted); font-size:1.05rem;">
        Membership runs one year from the date payment is received. Choose the
        class that matches your role — see the full eligibility rules in our
        <a href="/documents/oknahra-2025-bylaws.pdf">Bylaws</a>.
      </p>
    </div>
    <div class="media-banner">
      <img src="/images/stock/membership-support.jpg" alt="OKNAHRA members collaborating" loading="eager">
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="pricing-grid">
      {cards}
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">How dues are used</span>
      <h2>Your membership funds the mission</h2>
    </div>
    <div class="card-grid">
      <div class="card"><h3>Programming</h3><p>The biannual Summit, training, and networking events for Oklahoma tribal HR professionals.</p></div>
      <div class="card"><h3>Advocacy</h3><p>Monitoring and responding to legislation affecting employment across Indian Country.</p></div>
      <div class="card"><h3>Certification</h3><p>Supporting tribal-specific HR certification pathways and continuing education.</p></div>
    </div>
  </div>
</section>
"""
