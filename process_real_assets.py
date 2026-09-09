#!/usr/bin/env python3
"""One-time processing of the REAL assets staged from the client's Dropbox/
Downloads folder (via the connected device) into the site's images/ folder,
replacing the earlier generated placeholders. Run once; outputs land in
images/ as real production-ready files.
"""
import os
import numpy as np
from PIL import Image

SRC = "/mnt/user-data/uploads/OKNAHRA"
ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "images")
DOCS = os.path.join(ROOT, "documents")


def whiten_to_transparent(im, threshold=235):
    """Turn near-white background transparent with a soft edge, keep the art opaque."""
    im = im.convert("RGBA")
    arr = np.array(im).astype(np.float32)
    rgb = arr[:, :, :3]
    # "whiteness" = how close to pure white each pixel is
    whiteness = rgb.min(axis=2)
    alpha = 255 - np.clip((whiteness - (threshold - 40)) / max(1, (255 - (threshold - 40))) * 255, 0, 255)
    alpha = np.clip(alpha, 0, 255)
    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype("uint8"), "RGBA")


def trim(im):
    arr = np.array(im.convert("RGBA"))
    mask = arr[:, :, 3] > 8
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return im
    return im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1))


def pad_to_square(im, pad_frac=0.12):
    im = trim(im)
    w, h = im.size
    side = int(max(w, h) * (1 + pad_frac))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return canvas


def save_logo():
    src = Image.open(os.path.join(SRC, "OKNAHRA logo final-7c12c42.png"))
    full = whiten_to_transparent(src)
    full = trim(full)
    os.makedirs(os.path.join(IMG, "logos"), exist_ok=True)
    full.save(os.path.join(IMG, "logos", "oknahra-full-lockup.png"))
    print("full lockup:", full.size)

    # Feather-art-only band (above the wordmark) for a compact square mark
    arr = np.array(Image.open(os.path.join(SRC, "OKNAHRA logo final-7c12c42.png")).convert("RGB"))
    feathers_band = Image.fromarray(arr[0:906, :, :])
    feathers = whiten_to_transparent(feathers_band)
    feathers_sq = pad_to_square(feathers, pad_frac=0.06)
    for size in (512, 192, 96):
        feathers_sq.resize((size, size), Image.LANCZOS).save(
            os.path.join(IMG, "logos", f"oknahra-icon-{size}.png")
        )
    feathers_sq.resize((32, 32), Image.LANCZOS).save(os.path.join(IMG, "logos", "favicon.png"))
    print("icon mark:", feathers_sq.size)


def save_partner_logo(filename, outname, threshold=235):
    src = Image.open(os.path.join(SRC, filename))
    out = whiten_to_transparent(src, threshold=threshold)
    out = trim(out)
    out.save(os.path.join(IMG, "logos", outname))
    print(outname, out.size)


STOCK_PLAN = {
    # source filename                 -> (site filename,          max width, used for)
    "AdobeStock_805223306.jpeg": ("hero-primary.jpg", 1600, "Home hero"),
    "AdobeStock_23960880.jpeg": ("about-hero.jpg", 1400, "About Us hero"),
    "AdobeStock_499475418.jpeg": ("membership-support.jpg", 1400, "Membership page"),
    "AdobeStock_126190017.jpeg": ("events-hero.jpg", 1400, "Events page"),
    "AdobeStock_174985406.jpeg": ("sponsorship-support.jpg", 1400, "Sponsorship page"),
}


def save_stock():
    os.makedirs(os.path.join(IMG, "stock"), exist_ok=True)
    for src_name, (out_name, max_w, _use) in STOCK_PLAN.items():
        im = Image.open(os.path.join(SRC, src_name)).convert("RGB")
        w, h = im.size
        if w > max_w:
            im = im.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
        im.save(os.path.join(IMG, "stock", out_name), quality=82, optimize=True)
        print(out_name, im.size)


def save_bylaws():
    os.makedirs(DOCS, exist_ok=True)
    src = os.path.join(SRC, "OKNAHRA 2025 Bylaws.pdf")
    with open(src, "rb") as f:
        data = f.read()
    with open(os.path.join(DOCS, "oknahra-2025-bylaws.pdf"), "wb") as f:
        f.write(data)
    print("bylaws pdf:", len(data), "bytes")


if __name__ == "__main__":
    save_logo()
    save_partner_logo("NNAHRA-Logo-web (1).png", "nnahra.png")
    save_partner_logo("HRCI_logo.png", "hrci.png", threshold=240)
    save_stock()
    save_bylaws()
    print("done")
