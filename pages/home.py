def render():
    return """
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
        <div class="stat"><strong>500+</strong><span>HR professionals engaged since founding</span></div>
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
      <h2>Built by Oklahoma tribal HR, for Oklahoma tribal HR</h2>
      <p style="color:var(--color-text-muted);">A state-level affiliate of NNAHRA, focused on the specific workforce, legal, and cultural realities of HR inside Oklahoma's tribal governments and enterprises.</p>
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

<section>
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Partners</span>
      <h2>Proud to work alongside</h2>
    </div>
    <div class="sponsor-logos">
      <img src="/images/logos/nnahra.png" alt="NNAHRA">
      <img src="/images/logos/shrm.png" alt="SHRM">
      <img src="/images/logos/hrci.png" alt="HR Certification Institute">
    </div>
    <p style="text-align:center; margin-top:24px;"><a class="btn btn-gold" href="/sponsorship.html">Become a Sponsor</a></p>
  </div>
</section>

<section class="section-alt">
  <div class="container" style="text-align:center;">
    <h2>Ready to join Oklahoma's tribal HR community?</h2>
    <p style="max-width:56ch; margin:0 auto 24px; color:var(--color-text-muted);">Membership supports the programs, certification, and advocacy that make OKNAHRA valuable for HR professionals across Indian Country.</p>
    <a class="btn btn-primary" href="/membership.html">View Membership Options</a>
  </div>
</section>
"""
