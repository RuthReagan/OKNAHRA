TIER_BADGE_COLORS = {
    "Red": ("var(--oknahra-red-dark)", "#FFFFFF"),
    "Yellow": ("var(--oknahra-gold)", "var(--oknahra-black)"),
    "White": ("var(--oknahra-tan)", "var(--oknahra-black)"),
    "Black": ("var(--oknahra-black)", "var(--oknahra-cream)"),
}


def _all_sponsors(tiers):
    out = []
    for t in tiers or []:
        color = t["name"].split()[0]
        for s in t.get("sponsors", []):
            out.append({"name": s["name"], "logo": s["logo"], "tier_name": t["name"], "color": color})
    return out


def _sponsor_chip(s):
    bg, fg = TIER_BADGE_COLORS.get(s["color"], ("var(--oknahra-tan)", "var(--oknahra-black)"))
    return f"""
      <div style="flex:0 0 auto; display:flex; flex-direction:column; align-items:center; gap:8px;">
        <a class="logo-chip" href="/sponsorship.html" style="padding:16px 28px;">
          <img src="/images/logos/{s['logo']}" alt="{s['name']}" style="max-height:40px; width:auto;">
        </a>
        <span style="font-size:.72rem; font-weight:700; letter-spacing:.03em; text-transform:uppercase; padding:3px 10px; border-radius:999px; background:{bg}; color:{fg};">{s['tier_name']}</span>
      </div>"""


def _tier_preview_card(t):
    feather = t.get("feather")
    feather_img = (
        f'<div style="width:64px; height:64px; margin:0 auto 8px; border-radius:50%; '
        f'background:var(--oknahra-tan); display:flex; align-items:center; justify-content:center;">'
        f'<img src="/images/logos/feathers/{feather}" alt="" aria-hidden="true" '
        f'style="height:40px; width:auto; display:block;"></div>'
        if feather else ""
    )
    return f"""
      <div class="card" style="text-align:center;">
        {feather_img}
        <h3 style="margin-bottom:4px;">{t['name']}</h3>
        <div class="price-amount" style="font-size:1.1rem;">{t['price']}</div>
      </div>"""


def render(sponsorship_tiers=None):
    all_sponsors = _all_sponsors(sponsorship_tiers)
    sponsor_chips = "\n".join(_sponsor_chip(s) for s in all_sponsors)
    sponsors_section = f"""
<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Sponsors</span>
      <h2>Our Sponsors</h2>
      <p style="color:var(--color-text-muted);">Organizations investing directly in OKNAHRA's mission — shown with their sponsorship level.</p>
    </div>
    <div style="display:flex; flex-wrap:nowrap; gap:28px; align-items:flex-start; overflow-x:auto; -webkit-overflow-scrolling:touch; padding:4px 4px 12px; justify-content:center;">
      {sponsor_chips}
    </div>
    <p style="text-align:center; margin-top:24px;"><a class="btn btn-gold" href="/sponsorship.html">Become a Sponsor</a></p>
  </div>
</section>""" if sponsor_chips else ""
    tier_cards = "\n".join(_tier_preview_card(t) for t in (sponsorship_tiers or []))
    tiers_section = f"""
<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Sponsorship</span>
      <h2>Sponsorship levels</h2>
      <p style="color:var(--color-text-muted);">Four tiers, each named for a feather in the OKNAHRA mark.</p>
    </div>
    <div class="card-grid" style="grid-template-columns:repeat(4, 1fr);">
      {tier_cards}
    </div>
    <p style="text-align:center; margin-top:24px;"><a class="btn btn-gold" href="/sponsorship.html">See Sponsorship Details</a></p>
  </div>
</section>""" if tier_cards else ""
    return f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">Oklahoma Native American HR Association</span>
      <h1>HR excellence in service of Oklahoma's tribal nations.</h1>
      <p style="font-size:1.15rem; color:var(--color-text-muted); max-width:56ch;">
        OKNAHRA connects, certifies, and champions the HR professionals who
        support tribal governments and tribal enterprises across Oklahoma —
        so Indian Country's workforce is led by people equipped to serve it well.
      </p>
      <div style="display:flex; gap:14px; flex-wrap:wrap; margin-top:28px;">
        <a class="btn btn-primary" href="/membership.html">Become a Member</a>
        <a class="btn btn-outline" href="/about.html">Meet the Board</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>39</strong><span>Oklahoma tribal nations in our service area</span></div>
        <div class="stat stat-cta"><strong>Now Forming</strong><span>Be one of OKNAHRA's founding members</span></div>
        <div class="stat"><strong>2×</strong><span>Annual Summits per year</span></div>
      </div>
      <p class="placeholder-note" style="margin-top:18px;">Stat figures carried over from prior materials — confirm current numbers before launch.</p>
    </div>
    <div class="hero-art">
      <img src="/images/stock/hero-primary.jpg" alt="Oklahoma tribal HR professionals collaborating in a meeting" loading="eager">
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Why OKNAHRA</span>
      <h2>Purpose-built for the realities of tribal HR in Oklahoma</h2>
      <p style="color:var(--color-text-muted);">Focused on the specific workforce, legal, and cultural realities of HR inside Oklahoma's tribal governments and enterprises.</p>
    </div>
    <div class="card-grid">
      <div class="card">
        <h3>Community &amp; Networking</h3>
        <p>Connect with HR peers across Oklahoma's tribal nations at the biannual Summit and year-round member events.</p>
      </div>
      <div class="card">
        <h3>Professional Development</h3>
        <p>Certification pathways, training, and leadership development built for HR inside tribal enterprises.</p>
      </div>
      <div class="card">
        <h3>Advocacy &amp; Voice</h3>
        <p>A collective voice on legislative and regulatory issues affecting employment and HR in Indian Country.</p>
      </div>
    </div>
  </div>
</section>
{sponsors_section}
<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Partners</span>
      <h2>Proud to work alongside</h2>
    </div>
    <div class="sponsor-logos">
      <a class="logo-chip" href="https://nnahra.org/" target="_blank" rel="noopener"><img src="/images/logos/nnahra.png" alt="NNAHRA"></a>
      <a class="logo-chip" href="https://www.shrm.org/" target="_blank" rel="noopener"><img src="/images/logos/shrm.png" alt="SHRM"></a>
      <a class="logo-chip" href="https://www.hrci.org/" target="_blank" rel="noopener"><img src="/images/logos/hrci.png" alt="HR Certification Institute"></a>
    </div>
  </div>
</section>
{tiers_section}
<section class="section-alt">
  <div class="container" style="text-align:center;">
    <h2>Ready to join Oklahoma's tribal HR community?</h2>
    <p style="max-width:56ch; margin:0 auto 24px; color:var(--color-text-muted);">Membership supports the programs, certification, and advocacy that make OKNAHRA valuable for HR professionals across Indian Country.</p>
    <a class="btn btn-primary" href="/membership.html">View Membership Options</a>
  </div>
</section>
"""
