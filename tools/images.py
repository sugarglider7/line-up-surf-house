#!/usr/bin/env python3
"""Turn selected originals from research/raw/images/ into site/assets/img/*.webp.

Declarative: edit SPEC below, then `python3 tools/images.py`. Sequential, one image at a
time (VM resource rule). Writes tools/img_manifest.json, which tools/build.py reads for
width/height, dominant colour (LQIP background) and srcset variants.

SPEC fields
  name     output stem (files: <name>-<w>.webp)
  src      path relative to research/raw/images/
  crop     (x0, y0, x1, y1) in source pixels, or None for the full frame
  widths   output widths (never upscaled beyond the crop width)
  q        WebP quality
  treat    optional: "duotone" (ink → haze, used for the sunset band)
  horizon  True → detect the sea horizon row inside the crop and store it as a fraction;
           a float → measured by eye (use when the beach edge fools the detector)
  fmt      optional: "jpg" (Open Graph image)
  rotate   optional degrees (PIL sign: negative = clockwise) applied before the crop, to level a tilted horizon
"""
import json
import os
import sys

from PIL import Image, ImageFilter, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO, "research", "raw", "images")
OUT = os.path.join(REPO, "site", "assets", "img")
MANIFEST = os.path.join(REPO, "tools", "img_manifest.json")
MAX_BYTES = 440 * 1024

INK = (15, 37, 51)      # --ink  #0f2533
HAZE = (240, 222, 190)  # --haze #f0debe

SPEC = [
    # Cover: the view from upstairs over the beach car park to Anza's surf (Booking, property upload)
    dict(name="hero-m", src="hires/bk-03-dt-seaview-A-635804457-2048.jpg", crop=(150, 180, 1350, 1680), widths=[640, 900], q=80, horizon=True),
    dict(name="hero-d", src="hires/bk-03-dt-seaview-A-635804457-2048.jpg", crop=(140, 700, 1536, 1485), widths=[1000, 1396], q=80, horizon=True),
    # 01 First light: sea-view room window framing beach and sea
    dict(name="window", src="hires/bk-47-dt-seaview-A-635804467-2048.jpg", crop=(40, 0, 1536, 1870), widths=[640, 1000], q=74),
    # 02 First session: shop front + banner, boards against the mural, wetsuit rail, logo board nose
    dict(name="shopfront", src="gm-owner-03.jpg", crop=(0, 120, 1200, 1600), widths=[640, 1000], q=74),
    dict(name="boards", src="gm-owner-01.jpg", crop=(0, 100, 1200, 1600), widths=[640, 1000], q=74),
    dict(name="wetsuits", src="gm-owner-05.jpg", crop=(0, 100, 1200, 1600), widths=[640, 1000], q=74),
    dict(name="logo-board", src="gm-owner-07.jpg", crop=None, widths=[640, 1080], q=76),
    # 03 Midday: the four room types (+ door plaques)
    dict(name="room-seaview", src="hires/bk-73-dt-seaview-A-635804461-2048.jpg", crop=(0, 160, 1536, 2048), widths=[480, 800], q=72),
    dict(name="room-triple", src="hires/bk-46-triple-seaview-635808077-2048.jpg", crop=(0, 100, 1536, 1990), widths=[480, 800], q=72),
    dict(name="room-private", src="hires/bk-55-dt-privbath-A-635809335-2048.jpg", crop=(0, 160, 1536, 2048), widths=[480, 800], q=72),
    dict(name="room-compact", src="hires/bk-80-dt-A-640506966-2048.jpg", crop=(0, 60, 1536, 1950), widths=[480, 800], q=72),
    # 05 Sunset: hazy late light over the beach from a sea-view room, duotone
    dict(name="late-light", src="hires/bk-17-dt-seaview-B-694632909-2048.jpg", crop=(110, 430, 900, 1010), widths=[640, 790], q=74, treat="duotone"),
    # Open Graph: the LINE UP mural (accommodation · Surf School · Shop)
    dict(name="og", src="gm-owner-06.jpg", crop=(0, 360, 1200, 990), widths=[1200], q=82, fmt="jpg"),
    # Phase 3 inner pages
    # Rooms masthead: black window frame around the beach and sea, from a sea-view room
    dict(name="view-window", src="hires/bk-32-dt-seaview-A-635804469-2048.jpg", crop=(0, 64, 1536, 1984), widths=[640, 1000], q=74),
    # Room sets (second photo per type)
    dict(name="room-seaview-dbl", src="bk-13-dt-seaview-B-694632891.jpg", crop=(0, 56, 675, 900), widths=[480, 675], q=74),
    dict(name="room-triple-3", src="hires/bk-29-triple-seaview-635808047-2048.jpg", crop=(0, 64, 1536, 1984), widths=[480, 800], q=72),
    dict(name="room-private-twin", src="bk-06-dt-privbath-B-635800861.jpg", crop=(0, 56, 675, 900), widths=[480, 675], q=74),
    dict(name="reef-plaque", src="hires/bk-26-dt-B-640505626-2048.jpg", crop=(0, 64, 1536, 1984), widths=[480, 800], q=72),
    # The house masthead: the LINE UP mural
    dict(name="mural", src="gm-owner-06.jpg", crop=(0, 100, 1200, 1600), widths=[640, 1000], q=74),
    # Surf masthead: inside the shop, racks of yellow boards
    dict(name="shop-inside", src="gm-owner-04.jpg", crop=(0, 100, 1200, 1600), widths=[640, 1000], q=74),
    # Anza band: the beach, the car park and the surf from upstairs. The phone was tilted ~2.7° (horizon y 1316 at
    # x 270 → 1270 at x 1250), so level it first; the levelled horizon sits at source row ≈1293 → 0.45 of the crop.
    dict(name="anza-view", src="hires/bk-45-dt-seaview-A-635804459-2048.jpg", rotate=-2.69, crop=(150, 906, 1440, 1766), widths=[800, 1200, 1290], q=76, horizon=0.45),
]


def find_horizon(im):
    """Row (fraction of height) with the strongest sky→sea step, sampled across the middle 60%."""
    g = im.convert("RGB")
    w, h = g.size
    small = g.resize((max(1, w // 4), max(1, h // 4)))
    sw, sh = small.size
    px = small.load()
    best, best_y = 0, sh // 2
    for y in range(sh // 5, sh - 2):
        diff = 0
        for x in range(int(sw * 0.2), int(sw * 0.8)):
            r1, g1, b1 = px[x, y]
            r2, g2, b2 = px[x, y + 1]
            diff += (r1 + g1 + b1) - (r2 + g2 + b2)  # sky brighter than sea
        if diff > best:
            best, best_y = diff, y
    return round((best_y + 1) / sh, 4)


def dominant(im):
    c = im.convert("RGB").resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    return "#%02x%02x%02x" % c


def favicons():
    """PNG favicons drawn to match site/favicon.svg: sun on the horizon, two swell lines."""
    from PIL import ImageDraw
    site = os.path.join(REPO, "site")

    def icon(size, rounded):
        k = 8
        big = 64 * k
        im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if rounded:
            d.rounded_rectangle((0, 0, big - 1, big - 1), radius=12 * k, fill=INK + (255,))
        else:
            d.rectangle((0, 0, big, big), fill=INK + (255,))
        d.pieslice((18 * k, 25 * k, 46 * k, 53 * k), 180, 360, fill=(236, 208, 60, 255))
        d.rectangle((8 * k, 38 * k, 56 * k, 41.5 * k), fill=HAZE + (255,))
        d.rectangle((14 * k, 46 * k, 50 * k, 48 * k), fill=HAZE + (140,))
        d.rectangle((20 * k, 52 * k, 44 * k, 54 * k), fill=HAZE + (77,))
        return im.resize((size, size), Image.LANCZOS)

    icon(32, True).save(os.path.join(site, "favicon-32.png"), optimize=True)
    icon(180, False).convert("RGB").save(os.path.join(site, "apple-touch-icon.png"), optimize=True)
    print("favicons: favicon-32.png apple-touch-icon.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    if not only or "favicons" in only:
        favicons()
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    for spec in SPEC:
        if only and spec["name"] not in only:
            continue
        with Image.open(os.path.join(RAW, spec["src"])) as src:
            src = ImageOps.exif_transpose(src).convert("RGB")
            if spec.get("rotate"):
                src = src.rotate(spec["rotate"], resample=Image.BICUBIC)
            im = src.crop(spec["crop"]) if spec.get("crop") else src.copy()
        if spec.get("treat") == "duotone":
            gray = ImageOps.autocontrast(im.convert("L"), cutoff=1)
            im = ImageOps.colorize(gray, black=INK, white=HAZE, mid=(110, 118, 128))  # slate mids, haze highlights
        entry = {
            "w": im.width, "h": im.height, "color": dominant(im), "variants": [],
        }
        if spec.get("horizon") is True:
            entry["horizon"] = find_horizon(im)
        elif spec.get("horizon"):
            entry["horizon"] = spec["horizon"]
        ext = spec.get("fmt", "webp")
        for w in spec["widths"]:
            w = min(w, im.width)
            h = round(im.height * w / im.width)
            out = im.resize((w, h), Image.LANCZOS)
            if w < im.width:
                out = out.filter(ImageFilter.UnsharpMask(radius=0.6, percent=40, threshold=2))
            fn = f"{spec['name']}-{w}.{ext}"
            path = os.path.join(OUT, fn)
            q = spec["q"]
            while True:
                if ext == "jpg":
                    out.save(path, "JPEG", quality=q, optimize=True, progressive=True)
                else:
                    out.save(path, "WEBP", quality=q, method=6)
                if os.path.getsize(path) <= MAX_BYTES or q <= 50:
                    break
                q -= 4
            size = os.path.getsize(path)
            entry["variants"].append({"w": w, "h": h, "file": fn, "kb": round(size / 1024, 1)})
            print(f"{fn:28s} {w}x{h} {size // 1024:4d} KB q{q}")
            out.close()
        manifest[spec["name"]] = entry
        im.close()
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print("manifest:", MANIFEST)


if __name__ == "__main__":
    main()
