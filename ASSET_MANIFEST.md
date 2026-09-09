# Asset manifest — status of real vs. placeholder assets

## Now real (pulled from the connected OKNAHRA folder)

| Site path | Source | Notes |
|---|---|---|
| `images/logos/oknahra-full-lockup.png` | `OKNAHRA logo final-7c12c42.png` | White background made transparent; used in the header at any size |
| `images/logos/oknahra-icon-{512,192,96}.png`, `images/logos/favicon.png` | cropped from the same file (feather art only) | Square icon versions for favicon / apple touch icon |
| `images/logos/nnahra.png` | `NNAHRA-Logo-web (1).png` | Background made transparent |
| `images/logos/hrci.png` | `HRCI_logo.png` | Background made transparent |
| `documents/oknahra-2025-bylaws.pdf` | `OKNAHRA 2025 Bylaws.pdf` | Linked from the About and Membership pages |
| `images/stock/hero-primary.jpg` | `AdobeStock_805223306.jpeg` | Home hero |
| `images/stock/about-hero.jpg` | `AdobeStock_23960880.jpeg` | About Us hero |
| `images/stock/membership-support.jpg` | `AdobeStock_499475418.jpeg` | Membership page |
| `images/stock/events-hero.jpg` | `AdobeStock_126190017.jpeg` | Events page |
| `images/stock/sponsorship-support.jpg` | `AdobeStock_174985406.jpeg` | Sponsorship page |

The brand palette in `css/styles.css` was also re-sampled directly from the
real logo's exact pixel colors (red `rgb(211,55,60)`, black `rgb(32,31,31)`,
yellow `rgb(255,242,21)`) rather than the earlier approximation.

There are ~50 more licensed stock photos in the source folder not used yet
(the rest of the `AdobeStock_*.jpeg` files) — happy to swap in different ones
for any page if these don't feel like the right fit.

## Still placeholder / still needed

- **SHRM logo** — not present in the folder; the partner strip shows a text
  placeholder box. Either send the file or I'll link "SHRM" as text only.
- **Board photos** — Ruth Reagan, Lena McQuary, and Brandee Ingram all still
  show "Photo pending" (see notes on each in `pages/about.py` for why).
- **Four unidentified headshots** in the folder — `C Richey Headshot.png`,
  `Darius McGee.jfif`, `Head shot - Tal Moore.jpg`, `Headshot JN.jpg` — real
  professional headshots of people not mentioned in any edit list so far.
  These look like they could be other current board members (the bylaws
  define 6 more officer seats with no name yet: President-Elect, Past
  President, VP Leadership Development, VP Membership, VP Legislative
  Affairs, Board Member at Large – Sponsorships). **I didn't guess-assign
  them** — tell me which seat (if any) each belongs to and I'll wire them in.
- **Treasurer seat** — vacant pending confirmation (see board note: Terasita
  Cowan was proposed then confirmed removed, not added).

## Board photos going forward (`images/board/`)

1. Save a photo as `images/board/<first-last>.jpg`.
2. In `pages/about.py`, set that person's `"photo"` field to the filename.
3. Re-run `python3 build.py`.
