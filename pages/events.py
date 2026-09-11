def render():
    return """
<section class="page-hero">
  <div class="container page-hero-grid">
    <div>
      <p class="breadcrumb"><a href="/index.html">Home</a> / Events</p>
      <span class="eyebrow">Events</span>
      <h1>Summits, trainings &amp; networking</h1>
      <p style="max-width:60ch; color:var(--color-text-muted); font-size:1.05rem;">
        OKNAHRA holds a biannual Summit and hosts training and networking events
        throughout the year for members across Oklahoma's tribal HR community.
      </p>
    </div>
    <div class="media-banner">
      <img src="/images/stock/events-hero.jpg" alt="Regalia at an OKNAHRA gathering" loading="eager">
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Upcoming</span>
      <h2>Upcoming events</h2>
    </div>
    <div class="card-grid">
      <div class="card">
        <span class="badge">Summit</span>
        <h3 style="margin-top:10px;">OKNAHRA Biannual Summit</h3>
        <p>Date, venue, and registration to be announced.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container" style="text-align:center;">
    <h2>Have an event to share with members?</h2>
    <p style="color:var(--color-text-muted);">Reach out and we'll help get it in front of the OKNAHRA community.</p>
    <a class="btn btn-primary" href="/contact.html">Contact Us</a>
  </div>
</section>
"""
