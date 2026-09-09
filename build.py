#!/usr/bin/env python3
"""
Static site builder for the OKNAHRA website rebuild.
Generates fully static HTML pages (no build step needed at hosting time —
the /home/claude/oknahra-site/dist folder IS the deployable site) from
shared header/footer templates + per-page content defined below.

Edit board members, pricing, and copy in this file, then re-run:
    python3 build.py
"""
import os, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SITE_URL = "https://oknahra.net"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About Us"),
    ("membership.html", "Membership"),
    ("sponsorship.html", "Sponsorship"),
    ("events.html", "Events"),
    ("job-board.html", "Job Board"),
    ("certification.html", "Certification"),
    ("contact.html", "Contact"),
]

# ---------------------------------------------------------------
# BOARD ROSTER
# Source: OKNAHRA 2025 Bylaws (Article VII — 10 officer seats) +
# Ruth Reagan's Sept 2026 edit list. Seats marked vacant/pending
# are seats the bylaws define that we don't have a confirmed name
# for yet — replace when the updated roster comes in.
# ---------------------------------------------------------------
BOARD = [
    {
        "name": "Ruth Reagan, TMP",
        "role": "President",  # NOTE: placeholder seat assignment — confirm exact officer title
        "photo": None,
        "bio": "Founder and CEO of Reagan Strategic Solutions.",
        "status": "confirmed",
        "note": "Name/credentials/title updated per Sept 2026 request. Confirm which of the 10 bylaws officer seats this is (site previously did not specify).",
    },
    {
        "name": "Vacant",
        "role": "Treasurer",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Terasita Cowan was originally proposed for this seat, but the Sept 8 2026 clarification confirmed she's being removed from the board along with Julio Munez and Yonne Tiger — not added. Confirm who currently holds Treasurer.",
    },
    {
        "name": "Lena McQuary",
        "role": "Board Member at Large – NNAHRA Liaison",
        "photo": None,
        "bio": "Chief Human Resources Officer at Downstream Casino Resort and an enrolled Quapaw Nation member, with 16 years leading HR for the tribal enterprise. 2022 NNAHRA HR Leader of the Year and named one of CIO Views Magazine's Top 10 Most Influential HR Executives of 2024. Certified Tribal Human Resources Professional (I & II).",
        "status": "confirmed",
        "note": "Bio/credentials sourced from her NNAHRA board listing (nnahra.org) per request; photo to be sourced from the same page or requested directly — not redistributed here without confirming she's OK with the same headshot being reused on OKNAHRA's site.",
    },
    {
        "name": "Brandee Ingram",
        "role": "Secretary",
        "photo": None,
        "bio": "Human Resources Director, Rock & Brews Casino.",
        "status": "confirmed",
        "note": "Photo requested from Brandee, not yet received.",
    },
    {
        "name": "Vacant",
        "role": "President-Elect",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    {
        "name": "Vacant",
        "role": "Past President",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    {
        "name": "Vacant",
        "role": "VP, Leadership Development",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    {
        "name": "Vacant",
        "role": "VP, Membership",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    {
        "name": "Vacant",
        "role": "VP, Legislative Affairs",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    {
        "name": "Vacant",
        "role": "Board Member at Large – Sponsorships",
        "photo": None,
        "bio": "",
        "status": "vacant",
        "note": "Not covered by the Sept 2026 edit list — confirm who currently holds this bylaws-defined seat.",
    },
    # Removed per request — kept here (not rendered) so the edit is traceable:
    # Julio Munez — removed, prior title unknown, slot rendered as vacant above.
    # Yonne Tiger — removed, prior title unknown, slot rendered as vacant above.
]

MEMBERSHIP_TIERS = [
    {
        "name": "Associate Membership",
        "price": "$100",
        "period": "/ year",
        "eligibility": "For individuals actively employed in HR or another role with a Native American tribe or tribal enterprise.",
        "features": [
            "Full voting rights at the annual Membership Meeting",
            "Eligible to hold elected office on the Board",
            "Reduced pricing on OKNAHRA events and the biannual Summit",
            "Newsletter, job board, and networking directory access",
        ],
        "featured": True,
        "stripe_link": "PASTE_STRIPE_PAYMENT_LINK_ASSOCIATE",
    },
    {
        "name": "Native Non-Profit Associate",
        "price": "$100",
        "period": "/ year",
        "eligibility": "For employees or elected officials of Native non-profit organizations.",
        "features": [
            "Non-voting membership",
            "Reduced pricing on OKNAHRA events and the biannual Summit",
            "Newsletter, job board, and networking directory access",
        ],
        "featured": False,
        "stripe_link": "PASTE_STRIPE_PAYMENT_LINK_NONPROFIT",
    },
    {
        "name": "Corporate Membership",
        "price": "$150",
        "period": "/ year",
        "eligibility": "For vendors, consultants, and suppliers who serve tribal enterprises but aren't employed by one.",
        "features": [
            "Non-voting membership",
            "Visibility with HR decision-makers across Oklahoma tribal enterprises",
            "Newsletter and event access",
        ],
        "featured": False,
        "stripe_link": "https://buy.stripe.com/test_bJebJ15R241FaWRdUl9k404",
    },
    {
        "name": "Student Membership",
        "price": "$25",
        "period": "/ year",
        "eligibility": "For students enrolled in post-secondary education in HR or a related field.",
        "features": [
            "Non-voting membership",
            "Reduced pricing on OKNAHRA events and the biannual Summit",
            "Newsletter, job board, and networking directory access",
        ],
        "featured": False,
        "stripe_link": "https://buy.stripe.com/test_7sY6oH2EQ9lZ4yt03v9k403",
    },
]

SPONSORSHIP_TIERS = [
    {"name": "Red Sponsor", "price": "$500", "feather": "red-feather.png", "features": ["Logo on the OKNAHRA Partners page", "Recognition at one event", "One complimentary OKNAHRA membership"], "stripe_link": "https://buy.stripe.com/test_bJe9ATbbm55JaWR03v9k408"},
    {"name": "Yellow Sponsor", "price": "$1,000", "feather": "yellow-feather.png", "features": ["Logo on the OKNAHRA Partners page", "Recognition at all events", "Newsletter mention", "One complimentary OKNAHRA membership"], "stripe_link": "https://buy.stripe.com/test_4gM28r1AMgOr1mh8A19k407"},
    {"name": "White Sponsor", "price": "$2,500", "feather": "white-feather.png", "features": ["Logo on the OKNAHRA Partners page and homepage", "Recognition at all events", "Newsletter mention", "Exhibit table at the Summit", "One complimentary OKNAHRA membership"], "stripe_link": "https://buy.stripe.com/test_5kQ8wPdjubu74ytdUl9k406"},
    {"name": "Black Sponsor", "price": "$5,000", "feather": "black-feather.png", "features": ["Logo on the OKNAHRA Partners page and homepage", "Premier recognition at all events", "Newsletter mention", "Exhibit table at the Summit", "Complimentary OKNAHRA memberships for your team"], "stripe_link": "https://buy.stripe.com/test_7sYdR9frC69N1mh03v9k405"},
]

YEAR = datetime.datetime.now().year


def nav_html(active):
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        items.append(f'<a href="{href}"{current}>{label}</a>')
    return "\n      ".join(items)


def layout(title, description, active, body, extra_head=""):
    canonical = f"{SITE_URL}/{'' if active == 'index.html' else active}"
    og_image = f"{SITE_URL}/images/social/og-cover.jpg"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OKNAHRA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/logos/favicon.png">
<link rel="apple-touch-icon" href="/images/logos/oknahra-icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/styles.css">
{extra_head}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="nav-wrap">
    <a class="brand" href="/index.html">
      <img class="brand-mark" src="/images/logos/oknahra-full-lockup.png" alt="OKNAHRA — Oklahoma Native American Human Resources Association" width="220" height="108">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="mainNav" onclick="var n=document.getElementById('mainNav');var open=n.classList.toggle('open');this.setAttribute('aria-expanded',open);">
      <span aria-hidden="true">☰</span><span class="visually-hidden">Menu</span>
    </button>
    <nav class="main-nav" id="mainNav" aria-label="Primary">
      {nav_html(active)}
      <a class="nav-cta" href="/membership.html">Join / Renew</a>
    </nav>
  </div>
</header>
<div class="motif-divider" role="presentation"></div>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h4>OKNAHRA</h4>
      <p style="color:#C9BBA6; max-width:32ch; font-size:0.92rem;">The Oklahoma Native American Human Resources Association supports HR professionals serving Oklahoma's tribal nations and tribal enterprises.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <a href="/about.html">About Us</a>
      <a href="/membership.html">Membership</a>
      <a href="/sponsorship.html">Sponsorship</a>
      <a href="/events.html">Events</a>
    </div>
    <div>
      <h4>Resources</h4>
      <a href="/job-board.html">Job Board</a>
      <a href="/certification.html">Certification</a>
      <a href="https://nnahra.org/" rel="noopener">NNAHRA (National)</a>
      <a href="https://www.shrm.org/" rel="noopener">SHRM</a>
    </div>
    <div>
      <h4>Contact</h4>
      <a href="/contact.html">Get in touch</a>
      <a href="mailto:info@oknahra.net">info@oknahra.net</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>&copy; {YEAR} OKNAHRA — Oklahoma Native American Human Resources Association. A 501(c)(6) nonprofit.</span>
    <span>Oklahoma, USA</span>
  </div>
</footer>
<script src="/js/main.js"></script>
</body>
</html>
"""


def write(path, html):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    # static assets
    shutil.copytree(os.path.join(ROOT, "css"), os.path.join(DIST, "css"))
    shutil.copytree(os.path.join(ROOT, "js"), os.path.join(DIST, "js"))
    shutil.copytree(os.path.join(ROOT, "images"), os.path.join(DIST, "images"))
    if os.path.isdir(os.path.join(ROOT, "documents")):
        shutil.copytree(os.path.join(ROOT, "documents"), os.path.join(DIST, "documents"))

    from pages import home, about, membership, sponsorship, events, job_board, certification, contact

    org_jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NGO",
  "name": "Oklahoma Native American Human Resources Association",
  "alternateName": "OKNAHRA",
  "url": "{SITE_URL}/",
  "logo": "{SITE_URL}/images/logos/oknahra-mark.png",
  "areaServed": "Oklahoma, USA",
  "memberOf": {{"@type": "Organization", "name": "NNAHRA", "url": "https://nnahra.org/"}}
}}
</script>"""
    write("index.html", layout(
        "OKNAHRA | Oklahoma Native American HR Association",
        "OKNAHRA supports HR professionals serving Oklahoma's tribal nations and tribal enterprises through community, certification, and advocacy.",
        "index.html", home.render(), extra_head=org_jsonld,
    ))
    write("about.html", layout(
        "About Us | OKNAHRA",
        "Meet the OKNAHRA board and learn the mission behind the Oklahoma Native American Human Resources Association.",
        "about.html", about.render(BOARD),
    ))
    write("membership.html", layout(
        "Membership | OKNAHRA",
        "Join OKNAHRA. Compare membership tiers for tribal HR professionals, non-profit associates, corporate partners, and students.",
        "membership.html", membership.render(MEMBERSHIP_TIERS),
    ))
    write("sponsorship.html", layout(
        "Sponsorship | OKNAHRA",
        "Partner with OKNAHRA. Sponsorship tiers and benefits for organizations supporting Oklahoma tribal HR.",
        "sponsorship.html", sponsorship.render(SPONSORSHIP_TIERS),
    ))
    write("events.html", layout(
        "Events | OKNAHRA",
        "OKNAHRA events, the biannual Summit, and networking opportunities for Oklahoma tribal HR professionals.",
        "events.html", events.render(),
    ))
    write("job-board.html", layout(
        "Job Board | OKNAHRA",
        "Browse HR career opportunities in Oklahoma's tribal enterprises, or list your open role with OKNAHRA.",
        "job-board.html", job_board.render(),
    ))
    write("certification.html", layout(
        "Certification | OKNAHRA",
        "Tribal HR certification pathways and professional development for OKNAHRA members.",
        "certification.html", certification.render(),
    ))
    write("contact.html", layout(
        "Contact | OKNAHRA",
        "Get in touch with the OKNAHRA board.",
        "contact.html", contact.render(),
    ))

    write_sitemap()
    write_robots()
    print(f"Built {len(NAV)} pages to {DIST}")


def write_sitemap():
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}/{href}</loc></url>" for href, _ in NAV
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    write("sitemap.xml", xml)


def write_robots():
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    build()
