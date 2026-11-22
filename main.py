#!/usr/bin/env python3
"""
News-image generator for the make.fun daily news-image bounty
"news-image-20261122" - "Sum up 22 November's world news in one image".

Draws a 1024x1024 PNG news infographic from scratch using only Pillow
shapes, lines, fills, gradients and text. No photographs, no logos,
no pasted images, no network access, no API keys.

Run:  python3 main.py
Writes output.png + entry.png next to this file, and /output/entry.png
when an /output directory exists (the make.fun harness path).
Deterministic: two runs write identical bytes.
"""

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LOCAL = os.path.join(HERE, "output.png")
OUT_ENTRY = os.path.join(HERE, "entry.png")
OUT_HARNESS = "/output/entry.png"

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
BG_TOP = (13, 21, 38)        # deep navy
BG_BOT = (10, 16, 30)
PANEL = (22, 35, 61)          # card navy
PANEL_LINE = (48, 68, 104)
HERO_PANEL = (24, 40, 70)
INK = (240, 244, 252)         # near-white
MUTED = (159, 176, 204)       # grey-blue
AMBER = (242, 183, 5)         # accent gold
TEAL = (45, 212, 191)
RED = (248, 113, 113)
BLUE = (96, 165, 250)
GREEN = (74, 222, 128)
PURPLE = (192, 132, 252)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---- story data (22 Nov 2026 news; see sources.md for dates) ------------
HERO = {
    "rank": "01",
    "tag": "WAR  ·  GULF",
    "headline": "US denies Iran hit an F-16 over the Gulf",
    "summary": ("US Central Command said on Saturday no American F-16 was "
                "attacked, after Iranian state media claimed air defences "
                "hit one on Friday evening; Bahrain warned residents of a "
                "potential threat the same day."),
    "sources": "Reuters",
}

STORIES = [
    {
        "rank": "02",
        "tag": "CRIME  ·  MEXICO",
        "headline": "Mexico captures FBI most-wanted 'El Chapo Isidro'",
        "summary": ("Special forces seized Fausto Isidro Meza Flores in "
                    "Guasave on Friday night; 11 people were killed in the "
                    "gunfights, and cartel gunmen set up burning roadblocks "
                    "across Sinaloa."),
        "sources": "Reuters  ·  AP",
        "icon": "badge",
        "accent": AMBER,
    },
    {
        "rank": "03",
        "tag": "TRADE  ·  BRUSSELS",
        "headline": "EU and Indonesia sign trade deal after 10 years",
        "summary": ("The CEPA and investment pact signed in Brussels on "
                    "Saturday scrap duties on 98.5% of EU goods lines; EU "
                    "exporters save about \u20ac600 million a year once it "
                    "takes effect in 2027."),
        "sources": "Reuters  ·  EU Council",
        "icon": "ship",
        "accent": BLUE,
    },
    {
        "rank": "04",
        "tag": "TECH  ·  GENEVA",
        "headline": "UN 'killer robot' talks end with no binding rules",
        "summary": ("After a week of talks ending at 04:30 on Saturday, "
                    "states agreed only to spend two more years drafting a "
                    "possible pact by 2028; the US and Russia resisted "
                    "binding limits."),
        "sources": "NPR  ·  TechXplore",
        "icon": "robot",
        "accent": PURPLE,
    },
    {
        "rank": "05",
        "tag": "WAR  ·  UKRAINE",
        "headline": "Russia strikes again: boy, 7, and paramedic killed",
        "summary": ("A fresh overnight barrage of 3 missiles and 148 drones "
                    "hit Kryvyi Rih and Kyiv early on Saturday; 58 people "
                    "were injured and homes and a hospital were damaged."),
        "sources": "UNITED24  ·  SunnyGoat",
        "icon": "burst",
        "accent": RED,
    },
]


# ---- icons (shapes only) -------------------------------------------------
def icon_burst(d, cx, cy, r, col):
    # missile-burst star over city bars
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else int(r * 0.45)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, outline=col, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)
    base = cy + r + 16
    for i, h in enumerate([22, 38, 28, 46, 26]):
        x0 = cx - 58 + i * 25
        d.rectangle([x0, base - h, x0 + 17, base], fill=col)


def icon_radar(d, cx, cy, r, col):
    # radar scope: concentric rings, sweep line, blips
    import math
    for rr in (r, int(r * 0.66), int(r * 0.33)):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col, width=4)
    ang = -math.pi / 4
    d.line([(cx, cy), (cx + int(r * 0.95) * math.cos(ang),
                       cy + int(r * 0.95) * math.sin(ang))],
           fill=AMBER, width=5)
    for bx, by in ((0.45, -0.3), (-0.5, 0.35), (0.15, 0.55)):
        d.ellipse([cx + int(r * bx) - 5, cy + int(r * by) - 5,
                   cx + int(r * bx) + 5, cy + int(r * by) + 5], fill=col)


def icon_badge(d, cx, cy, r, col):
    # five-point star badge
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else int(r * 0.45)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, outline=col, width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=col)


def icon_robot(d, cx, cy, r, col):
    # robot head: antenna, rounded head, eyes, mouth grille
    d.line([(cx, cy - r - 12), (cx, cy - int(r * 0.55))], fill=col, width=4)
    d.ellipse([cx - 6, cy - r - 18, cx + 6, cy - r - 6], fill=AMBER)
    d.rounded_rectangle([cx - int(r * 0.85), cy - int(r * 0.55),
                         cx + int(r * 0.85), cy + int(r * 0.7)],
                        radius=12, outline=col, width=4)
    d.ellipse([cx - int(r * 0.5) - 6, cy - int(r * 0.15) - 6,
               cx - int(r * 0.5) + 6, cy - int(r * 0.15) + 6], fill=col)
    d.ellipse([cx + int(r * 0.5) - 6, cy - int(r * 0.15) - 6,
               cx + int(r * 0.5) + 6, cy - int(r * 0.15) + 6], fill=col)
    for i in range(3):
        x0 = cx - int(r * 0.4) + i * int(r * 0.4)
        d.line([(x0, cy + int(r * 0.4)), (x0 + int(r * 0.2),
                                          cy + int(r * 0.4))],
               fill=col, width=3)


def icon_ship(d, cx, cy, r, col):
    # stacked containers on a hull
    d.rectangle([cx - r, cy - int(r * 0.55), cx - 6, cy - 4], fill=col)
    d.rectangle([cx + 2, cy - int(r * 0.55), cx + r, cy - 4], fill=AMBER)
    d.rectangle([cx - int(r * 0.7), cy, cx + int(r * 0.7), cy + int(r * 0.35)],
                fill=col)
    d.polygon([(cx - r - 6, cy + int(r * 0.35)), (cx + r + 6, cy + int(r * 0.35)),
               (cx + int(r * 0.6), cy + int(r * 0.8)),
               (cx - int(r * 0.6), cy + int(r * 0.8))], fill=col)
    d.line([cx - r - 10, cy + r + 8, cx + r + 10, cy + r + 8],
           fill=MUTED, width=3)


ICONS = {"burst": icon_burst, "radar": icon_radar, "badge": icon_badge,
         "robot": icon_robot, "ship": icon_ship}


# ---- build ----------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # vertical gradient background
    for y in range(H):
        t = y / H
        col = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=col)
    # faint decorative dots
    for gx in range(60, W - 40, 46):
        for gy in (118, 136):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(30, 46, 78))

    # ---- header ---------------------------------------------------------
    d.text((36, 26), "THE WORLD IN ONE DAY", font=font(38, bold=True), fill=INK)
    d.text((36, 76), "SUNDAY  \u00b7  22 NOVEMBER 2026",
           font=font(18, bold=True), fill=AMBER)
    d.text((W - 36, 34), "GLOBAL EDITION", font=font(17, bold=True),
           fill=MUTED, anchor="ra")
    d.text((W - 36, 62), "5 stories  \u00b7  Sunday 22 Nov 2026",
           font=font(14), fill=MUTED, anchor="ra")
    d.line([(36, 112), (W - 36, 112)], fill=AMBER, width=3)

    # ---- hero story -----------------------------------------------------
    hx, hy, hw, hh = 36, 128, 952, 252
    rounded(d, [hx, hy, hx + hw, hy + hh], 18, fill=HERO_PANEL,
            outline=PANEL_LINE, width=2)
    ix, iy, iw, ih = hx + 22, hy + 22, 196, 208
    rounded(d, [ix, iy, ix + iw, iy + ih], 14, fill=(16, 28, 52))
    icon_radar(d, ix + iw // 2, iy + 82, 52, RED)
    d.text((ix + iw // 2, iy + ih - 24), "GULF  \u00b7  SATURDAY",
           font=font(14, bold=True), fill=RED, anchor="ma")
    tx = hx + 242
    d.text((tx, hy + 22), "01  \u00b7  WAR", font=font(15, bold=True), fill=RED)
    y = draw_text_block(d, tx, hy + 48, HERO["headline"], font(27, bold=True),
                        INK, 688, 34)
    y = draw_text_block(d, tx, y + 8, HERO["summary"], font(16),
                        (205, 216, 235), 688, 23)
    d.text((tx, hy + hh - 30), "Sources:  " + HERO["sources"],
           font=font(13), fill=MUTED)

    # ---- grid of 4 stories ----------------------------------------------
    gx0, gy0 = 36, 404
    cw, ch, gap = 466, 236, 20
    for i, s in enumerate(STORIES):
        x = gx0 + (i % 2) * (cw + gap)
        y = gy0 + (i // 2) * (ch + gap)
        rounded(d, [x, y, x + cw, y + ch], 16, fill=PANEL,
                outline=PANEL_LINE, width=2)
        d.line([(x, y + 4), (x, y + ch - 4)], fill=s["accent"], width=5)
        ix, iy = x + 18, y + 18
        rounded(d, [ix, iy, ix + 96, iy + 96], 12, fill=(16, 28, 52))
        ICONS[s["icon"]](d, ix + 48, iy + 48, 30, s["accent"])
        tx = x + 130
        d.text((tx, y + 14), f"{s['rank']}  \u00b7  {s['tag']}",
               font=font(12, bold=True), fill=s["accent"])
        yy = draw_text_block(d, tx, y + 36, s["headline"], font(17, bold=True),
                             INK, 322, 22)
        draw_text_block(d, tx, yy + 5, s["summary"], font(12),
                        (205, 216, 235), 322, 17)
        d.text((tx, y + ch - 24), "Sources:  " + s["sources"],
               font=font(11), fill=MUTED)

    # ---- footer ---------------------------------------------------------
    d.line([(36, 920), (W - 36, 920)], fill=PANEL_LINE, width=2)
    d.text((36, 934),
           "Sources: Reuters  \u00b7  AP  \u00b7  NPR  \u00b7  TechXplore  \u00b7  "
           "UNITED24  \u00b7  EU Council",
           font=font(12), fill=MUTED)
    d.text((36, 956),
           "Full sources and first-publication dates in sources.md  \u2014  "
           "all stories reported 21\u201322 Nov 2026",
           font=font(12), fill=MUTED)
    d.text((36, 984),
           "All graphics are drawn from shapes, lines and text only - "
           "no photographs.",
           font=font(12), fill=MUTED)

    img.save(OUT_LOCAL, "PNG")
    img.save(OUT_ENTRY, "PNG")
    if os.path.isdir("/output"):
        img.save(OUT_HARNESS, "PNG")
    return OUT_LOCAL


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
