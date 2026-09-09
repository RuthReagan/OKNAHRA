def _person_card(m):
    vacant = m["status"] == "vacant"
    photo_block = (
        f'<img src="/images/board/{m["photo"]}" alt="{m["name"]}">'
        if m.get("photo") else
        ('Photo pending' if not vacant else 'Seat open')
    )
    bio = f"<p>{m['bio']}</p>" if m.get("bio") else ""
    note = f'<p class="placeholder-note">{m["note"]}</p>' if m.get("note") else ""
    cls = "person vacant" if vacant else "person"
    return f"""
      <div class="{cls}">
        <div class="person-photo">{photo_block}</div>
        <h3>{m['name']}</h3>
        <span class="role">{m['role']}</span>
        {bio}
        {note}
      </div>"""


def render(board):
    cards = "\n".join(_person_card(m) for m in board)
    return f"""
<section class="page-hero">
  <div class="container page-hero-grid">
    <div>
      <p class="breadcrumb"><a href="/index.html">Home</a> / About Us</p>
      <span class="eyebrow">About OKNAHRA</span>
      <h1>Serving the HR backbone of Oklahoma's tribal nations</h1>
      <p style="max-width:60ch; color:var(--color-text-muted); font-size:1.05rem;">
        OKNAHRA is an Oklahoma nonprofit corporation organized under Section 501(c)(6)
        of the Internal Revenue Code — self-governing, non-commercial, and nonpartisan,
        built to strengthen HR practice across Oklahoma's tribal governments and tribal
        enterprises.
      </p>
    </div>
    <div class="media-banner">
      <img src="/images/stock/about-hero.jpg" alt="OKNAHRA member at work" loading="eager">
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="card-grid">
      <div class="card">
        <h3>Our Purpose</h3>
        <p>To engage in lawful activity in support of HR professionals working with or for Oklahoma tribal nations and tribal enterprises, consistent with our nonprofit, nonpartisan charter.</p>
      </div>
      <div class="card">
        <h3>Governance</h3>
        <p>Governed by a Board of Directors of no fewer than seven and no more than fifteen members, elected annually by the membership at the OKNAHRA biannual Summit or by electronic poll.</p>
      </div>
      <div class="card">
        <h3>Our Bylaws</h3>
        <p>Read the full <a href="/documents/oknahra-2025-bylaws.pdf">2025 Bylaws (PDF)</a> for details on membership classes, board structure, and standing committees.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Board of Directors</span>
      <h2>Meet the Board</h2>
      <p style="color:var(--color-text-muted);">Board terms and seats follow the OKNAHRA Bylaws (Article VII). Seats without a confirmed name below are being updated — see note on each.</p>
    </div>
    <div class="people-grid">
      {cards}
    </div>
  </div>
</section>
"""
