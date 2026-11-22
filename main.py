#!/usr/bin/env python3
"""World news in one image — 22 November 2026.

Draws a 1024x1024 PNG news summary: one hero story across the top
and four more stories in a 2x2 grid below. Fully deterministic:
no network, no clock, no randomness.

The DejaVu fonts are bundled in fonts/ next to this script, so the
build works on any machine whether or not the system has them
installed. Output goes to /output/entry.png when that directory is
writable (the path the make.fun harness reads) and to output.png
next to this script otherwise.
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
GAP = 16

NAVY = (10, 25, 47)
PANEL = (17, 42, 70)
PANEL_LINE = (38, 74, 110)
WHITE = (240, 244, 248)
MUTED = (168, 188, 208)
AMBER = (255, 176, 32)
RED = (226, 75, 66)

_HERE = os.path.dirname(os.path.abspath(__file__))

SYSTEM_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/TTF",
    "/usr/share/fonts/dejavu",
]


def _font_paths(bold):
    """Candidate font files, best first: bundled, then system."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    paths = [
        os.path.join(_HERE, "fonts", name),
        os.path.join(_HERE, name),
    ]
    paths.extend(os.path.join(d, name) for d in SYSTEM_FONT_DIRS)
    return paths


def load_font(bold, size):
    for path in _font_paths(bold):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    # Last resort: Pillow's built-in default font. The layout still
    # renders and the program still exits 0 on a bare machine.
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()

HERO = {
    "tag": "TOP STORY",
    "headline": "US denies Iran downed an F-16 over the Gulf",
    "summary": (
        "Tehran claims it shot down a US fighter jet over the Persian Gulf. "
        "The Pentagon says no American aircraft was lost."
    ),
}

STORIES = [
    {
        "tag": "MEXICO",
        "headline": "Mexico captures 'El Chapo Isidro'",
        "summary": (
            "FBI most-wanted drug lord seized in Guasave, Sinaloa. "
            "Eleven people were killed in the operation."
        ),
    },
    {
        "tag": "TRADE",
        "headline": "EU and Indonesia sign trade deal",
        "summary": (
            "CEPA sealed in Brussels after a decade of talks. 98.5% of EU "
            "goods lines go tariff-free, saving about \u20ac600M a year."
        ),
    },
    {
        "tag": "GENEVA",
        "headline": "UN 'killer robot' talks end with no rules",
        "summary": (
            "Negotiations in Geneva on autonomous weapons close "
            "without binding limits."
        ),
    },
    {
        "tag": "UKRAINE",
        "headline": "Russia strikes Kryvyi Rih and Kyiv",
        "summary": (
            "A 7-year-old boy and a paramedic were killed. Three missiles "
            "and 148 drones launched; 58 people wounded."
        ),
    },
]


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, lines, font, x, y, fill, line_height):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def draw_tag(draw, text, x, y, accent):
    """Small filled tag chip; returns the width it used."""
    font = load_font(True, 20)
    pad_x = 12
    pad_y = 7
    text_w = int(draw.textlength(text, font=font))
    chip_w = text_w + 2 * pad_x
    chip_h = 20 + 2 * pad_y
    draw.rounded_rectangle(
        [x, y, x + chip_w, y + chip_h], radius=6, fill=accent
    )
    draw.text(
        (x + pad_x, y + pad_y - 1), text, font=font, fill=NAVY
    )
    return chip_w, chip_h


def draw_header(draw):
    title_font = load_font(True, 46)
    date_font = load_font(True, 22)
    draw.text(
        (MARGIN, 34), "WORLD NEWS", font=title_font, fill=WHITE
    )
    date_text = "22 NOVEMBER 2026"
    date_w = int(draw.textlength(date_text, font=date_font))
    draw.text(
        (WIDTH - MARGIN - date_w, 50),
        date_text,
        font=date_font,
        fill=AMBER,
    )
    draw.line(
        [(MARGIN, 108), (WIDTH - MARGIN, 108)],
        fill=PANEL_LINE,
        width=2,
    )


def draw_hero(draw):
    x0 = MARGIN
    y0 = 126
    x1 = WIDTH - MARGIN
    y1 = 448
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL)
    draw.rounded_rectangle(
        [x0, y0, x0 + 8, y1], radius=4, fill=RED
    )
    inner_x = x0 + 30
    inner_w = x1 - inner_x - 30
    _, chip_h = draw_tag(draw, HERO["tag"], inner_x, y0 + 24, AMBER)
    head_font = load_font(True, 46)
    head_lines = wrap(draw, HERO["headline"], head_font, inner_w)
    y = y0 + 24 + chip_h + 22
    y = draw_lines(draw, head_lines, head_font, inner_x, y, WHITE, 56)
    sum_font = load_font(False, 25)
    sum_lines = wrap(draw, HERO["summary"], sum_font, inner_w)
    y += 14
    draw_lines(draw, sum_lines, sum_font, inner_x, y, MUTED, 34)


def draw_card(draw, story, x0, y0, w, h):
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=12, fill=PANEL)
    inner_x = x0 + 22
    inner_w = w - 44
    tag_font = load_font(True, 19)
    draw.text(
        (inner_x, y0 + 18), story["tag"], font=tag_font, fill=AMBER
    )
    head_font = load_font(True, 27)
    head_lines = wrap(draw, story["headline"], head_font, inner_w)
    y = y0 + 50
    y = draw_lines(draw, head_lines, head_font, inner_x, y, WHITE, 33)
    sum_font = load_font(False, 20)
    sum_lines = wrap(draw, story["summary"], sum_font, inner_w)
    y += 8
    draw_lines(draw, sum_lines, sum_font, inner_x, y, MUTED, 26)


def draw_grid(draw):
    grid_y = 464
    grid_h = 460
    card_w = (WIDTH - 2 * MARGIN - GAP) // 2
    card_h = (grid_h - GAP) // 2
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x0 = MARGIN + col * (card_w + GAP)
        y0 = grid_y + row * (card_h + GAP)
        draw_card(draw, story, x0, y0, card_w, card_h)


def draw_footer(draw):
    draw.line(
        [(MARGIN, 946), (WIDTH - MARGIN, 946)],
        fill=PANEL_LINE,
        width=2,
    )
    foot_font = load_font(False, 18)
    draw.text(
        (MARGIN, 962),
        "22 November 2026",
        font=foot_font,
        fill=WHITE,
    )
    sources = "Sources: Reuters  |  AP  |  CNN  |  EU  |  NPR  |  United24"
    src_w = int(draw.textlength(sources, font=foot_font))
    draw.text(
        (WIDTH - MARGIN - src_w, 962),
        sources,
        font=foot_font,
        fill=MUTED,
    )


def build():
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw_header(draw)
    draw_hero(draw)
    draw_grid(draw)
    draw_footer(draw)
    return image


def main():
    image = build()
    # Try the harness path first, then next to this script. Either one
    # succeeding is enough; a read-only checkout must not kill the run
    # when /output is writable, and vice versa.
    targets = [
        "/output/entry.png",
        os.path.join(_HERE, "output.png"),
    ]
    saved = []
    for out_path in targets:
        try:
            parent = os.path.dirname(out_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            image.save(out_path, format="PNG")
            saved.append(out_path)
        except OSError:
            continue
    if not saved:
        raise SystemExit("could not write the output image anywhere")
    print("wrote", ", ".join(saved), image.size)


if __name__ == "__main__":
    main()
