#!/usr/bin/env python3
"""Renderer for the news-image-20261117 entry.

Draws three 1024x1024 variants (A: tile grid, B: newspaper front page,
C: big lead + compact list) with Pillow, using only the Liberation Sans
fonts bundled in build/fonts/ (SIL OFL 1.1, see build/fonts/OFL.txt).
All artwork is original code-drawn shapes: no photos, no logos, no faces.
Every story text comes from SOURCES.md (verified against >= 2 sources).

Run:  python3 build/render.py
Out:  build/variants/variant_a.png, variant_b.png, variant_c.png
      plus 512px downscales used for the legibility check in EVAL.md.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_REG = os.path.join(HERE, "fonts", "LiberationSans-Regular.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "LiberationSans-Bold.ttf")
OUT_DIR = os.path.join(HERE, "variants")

W = H = 1024
DATE_LINE = "TUESDAY 17 NOVEMBER 2026"

# ---------------------------------------------------------------- stories

LEAD = {
    "cat": "WAR \u00b7 EUROPE",
    "color": (229, 72, 77),
    "headline": "UKRAINE COLLAPSES A SPAN OF THE CRIMEA BRIDGE",
    "sub": ("Second day of strikes: the road arch falls into the Kerch Strait. "
            "Russia strikes Kyiv's bridges in reply; the Kremlin vows to rebuild."),
    "sub_b": ("Second day of strikes: the road arch falls into the Kerch Strait. "
              "Russia strikes Kyiv's bridges in reply."),
    "icon": "bridge",
}

STORIES = [
    {
        "cat": "MIDDLE EAST \u00b7 CONFLICT",
        "color": (255, 138, 61),
        "headline": "IRAN FIRES DRONES AT U.S. RADAR IN BAHRAIN",
        "sub": ("Bahrain says the attack was intercepted \u2014 no casualties or damage. "
                "Tanker attacks rise in the Strait of Hormuz."),
        "sub_short": ("Bahrain says it was intercepted \u2014 no casualties or damage. "
                      "Tanker attacks rise in Hormuz."),
        "tile_sub": "Intercepted \u2014 no casualties or damage. Tanker attacks rise in Hormuz.",
        "list_headline": "IRAN FIRES DRONES AT U.S. RADAR IN BAHRAIN",
        "list_sub": "Intercepted \u2014 no casualties or damage. Tanker attacks rise.",
        "col_headline": "IRAN DRONES TARGET BAHRAIN RADAR",
        "b_sub": "Intercepted; no casualties. Tanker attacks rise in Hormuz.",
        "icon": "radar",
    },
    {
        "cat": "DIPLOMACY \u00b7 ASIA",
        "color": (77, 163, 255),
        "headline": "TRUMP OPENS ASIA TRIP IN MANILA",
        "sub": ("Quad and ASEAN talks first \u2014 then Shenzhen, for a first "
                "Xi\u2013Putin\u2013Trump summit on Thursday on nuclear arms."),
        "sub_short": ("Quad talks first \u2014 then Shenzhen, for a first "
                      "Xi\u2013Putin\u2013Trump summit Thursday on nuclear arms."),
        "tile_sub": "Quad talks first, then a first Xi\u2013Putin\u2013Trump summit Thursday.",
        "list_headline": "TRUMP OPENS ASIA TRIP IN MANILA",
        "list_sub": "Quad talks; first Xi\u2013Putin\u2013Trump summit Thursday, on nuclear arms.",
        "b_sub": "Quad talks first; Xi\u2013Putin\u2013Trump summit Thursday on nuclear arms.",
        "icon": "globe",
    },
    {
        "cat": "HEALTH \u00b7 AMERICAS",
        "color": (177, 140, 255),
        "headline": "U.S. LOSES MEASLES ELIMINATION STATUS",
        "sub": ("PAHO ends the 26-year status; Mexico and Bolivia lose theirs too. "
                "More than 5,400 cases in 2026 \u2014 the most since 1991."),
        "sub_short": ("PAHO ends the 26-year status; Mexico, Bolivia too. "
                      "Most cases since 1991: 5,400+."),
        "tile_sub": "26-year status ends; Mexico and Bolivia too. Most cases since 1991.",
        "list_headline": "U.S. LOSES MEASLES ELIMINATION STATUS",
        "list_sub": "26-year status ends; 5,400+ cases in 2026, most since 1991.",
        "b_sub": "PAHO ends the 26-year status; Mexico, Bolivia too.",
        "icon": "virus",
    },
    {
        "cat": "CLIMATE \u00b7 COP31",
        "color": (63, 185, 111),
        "headline": "FIVE NATIONS PLEDGE FOSSIL-FUEL PHASE-OUT PLANS AT COP31",
        "sub": ("Denmark, Spain, Portugal, Ireland and Luxembourg announce roadmaps "
                "in Antalya. Draft deal proposes $120bn a year for adaptation by 2035."),
        "sub_short": ("Denmark, Spain, Portugal, Ireland and Luxembourg announce roadmaps "
                      "in Antalya. Draft deal proposes $120bn a year for adaptation by 2035."),
        "tile_sub": "Denmark, Spain, Portugal, Ireland, Luxembourg pledge roadmaps in Antalya.",
        "tile_headline": "FOSSIL-FUEL PHASE-OUT PLANS AT COP31",
        "list_headline": "FOSSIL-FUEL PHASE-OUT PLANS AT COP31",
        "list_sub": "Denmark, Spain, Portugal, Ireland, Luxembourg announce roadmaps.",
        "b_sub": ("Five nations announce roadmaps in Antalya. Draft deal proposes "
                  "$120bn a year for adaptation by 2035."),
        "icon": "leaf",
    },
    {
        "cat": "AFRICA \u00b7 SUDAN",
        "color": (232, 197, 71),
        "headline": "UN VERIFIES 2,230 CIVILIAN DEATHS IN SUDAN",
        "sub": ("UN rights report (Jan\u2013Oct): over 1,630 killed by drones \u2014 "
                "nearly three in four. The true toll is likely higher."),
        "sub_short": ("UN rights report (Jan\u2013Oct): over 1,630 killed by drones \u2014 "
                      "nearly three in four. The true toll is likely higher."),
        "tile_sub": ("UN rights report (Jan\u2013Oct): over 1,630 killed by drones \u2014 "
                     "nearly three in four. The true toll is likely higher."),
        "list_headline": "UN VERIFIES 2,230 CIVILIAN DEATHS IN SUDAN",
        "list_sub": "UN report, Jan\u2013Oct: 1,630+ killed by drones; toll likely higher.",
        "b_sub": ("UN rights report (Jan\u2013Oct): over 1,630 killed by drones \u2014 "
                  "nearly three in four. The true toll is likely higher."),
        "icon": "drone",
    },
]

FOOTER = "Compiled from multiple news sources \u00b7 Full sources in SOURCES.md"

# ---------------------------------------------------------------- helpers

_cache = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    return _cache[key]


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    """Word-wrap s to lines of at most max_w px. Returns list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            if text_w(draw, word, fnt) > max_w:
                raise ValueError(f"single word too wide: {word!r}")
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, s, fnt, fill, max_w, line_h, max_lines=None, align="left"):
    """Draw wrapped text; raise if it exceeds max_lines (no silent overflow)."""
    x, y = xy
    lines = wrap(draw, s, fnt, max_w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"text needs {len(lines)} lines > {max_lines}: {s[:60]!r}")
    for ln in lines:
        lx = x
        if align == "center":
            lx = x + (max_w - text_w(draw, ln, fnt)) / 2
        elif align == "right":
            lx = x + max_w - text_w(draw, ln, fnt)
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += line_h
    return y


def chip(draw, xy, s, fnt, color, text_color=(10, 14, 24), pad_x=10, pad_y=5):
    x, y = xy
    w = text_w(draw, s, fnt) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=color)
    draw.text((x + pad_x, y + pad_y - 2), s, font=fnt, fill=text_color)
    return w, h


# ---------------------------------------------------------------- icons
# All icons are simple original line/shape drawings inside a box (x, y, s).

def icon_bridge(draw, x, y, s, color, water=(90, 150, 220)):
    """Bridge with a collapsed middle span: deck with a gap, pylons, cables,
    a fallen segment tilted in the water, waves below."""
    lw = max(3, s // 15)
    deck_y = y + s * 0.40
    # pylons
    for tx in (x + s * 0.12, x + s * 0.88):
        draw.line([tx, deck_y - s * 0.26, tx, deck_y + s * 0.30], fill=color, width=lw)
    # cable-stayed fans from both pylon tops down to the deck
    for tx in (x + s * 0.12, x + s * 0.88):
        for f in (-0.09, 0.09, 0.19, 0.29):
            px = tx + s * f
            if x + s * 0.02 <= px <= x + s * 0.98 and not (x + s * 0.40 < px < x + s * 0.60):
                draw.line([tx, deck_y - s * 0.26, px, deck_y],
                          fill=color, width=max(2, lw - 1))
    # deck segments with a gap in the middle
    draw.line([x + s * 0.03, deck_y, x + s * 0.41, deck_y], fill=color, width=lw + 1)
    draw.line([x + s * 0.59, deck_y, x + s * 0.97, deck_y], fill=color, width=lw + 1)
    # broken ends dipping toward the water
    draw.line([x + s * 0.41, deck_y, x + s * 0.47, deck_y + s * 0.09], fill=color, width=lw)
    draw.line([x + s * 0.59, deck_y, x + s * 0.53, deck_y + s * 0.09], fill=color, width=lw)
    # fallen span, tilted in the water
    draw.line([x + s * 0.38, deck_y + s * 0.30, x + s * 0.64, deck_y + s * 0.40],
              fill=color, width=lw + 1)
    draw.line([x + s * 0.38, deck_y + s * 0.37, x + s * 0.64, deck_y + s * 0.47],
              fill=color, width=lw)
    # waves
    for wy in (deck_y + s * 0.52, deck_y + s * 0.63):
        xx = x + s * 0.05
        while xx < x + s * 0.86:
            draw.arc([xx, wy, xx + s * 0.12, wy + s * 0.07], start=180, end=360,
                     fill=water, width=max(2, lw - 1))
            xx += s * 0.13


def icon_radar(draw, x, y, s, color):
    lw = max(3, s // 13)
    cx, cy = x + s * 0.36, y + s * 0.60
    # dish (bowl) on a stand, with signal arcs above it
    draw.arc([cx - s * 0.28, cy - s * 0.34, cx + s * 0.28, cy + s * 0.20],
             start=305, end=125, fill=color, width=lw)
    draw.line([cx - s * 0.20, cy - s * 0.22, cx + s * 0.24, cy + s * 0.06], fill=color, width=lw)
    draw.line([cx, cy - s * 0.02, cx + s * 0.22, cy - s * 0.30], fill=color, width=lw)
    draw.ellipse([cx + s * 0.18, cy - s * 0.34, cx + s * 0.27, cy - s * 0.25], fill=color)
    draw.line([cx, cy + s * 0.04, cx - s * 0.11, cy + s * 0.36], fill=color, width=lw)
    draw.line([cx, cy + s * 0.04, cx + s * 0.13, cy + s * 0.36], fill=color, width=lw)
    draw.line([cx - s * 0.17, cy + s * 0.36, cx + s * 0.19, cy + s * 0.36], fill=color, width=lw)
    for r in (0.15, 0.26, 0.37):
        draw.arc([cx + s * 0.23 - s * r, cy - s * 0.30 - s * r,
                  cx + s * 0.23 + s * r, cy - s * 0.30 + s * r],
                 start=305, end=35, fill=color, width=max(2, lw - 1))


def icon_globe(draw, x, y, s, color):
    lw = max(3, s // 14)
    cx, cy, r = x + s * 0.42, y + s * 0.50, s * 0.36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=lw)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=max(2, lw - 1))
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=max(2, lw - 1))
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], start=0, end=180, fill=color, width=max(2, lw - 1))
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], start=180, end=360, fill=color, width=max(2, lw - 1))
    # route arc to a pin (summit ahead)
    draw.arc([cx + r * 0.4, cy - r * 1.15, cx + r * 1.7, cy + r * 0.2], start=200, end=330, fill=color, width=max(2, lw - 1))
    px, py = cx + r * 1.28, cy - r * 0.92
    draw.ellipse([px - s * 0.05, py - s * 0.05, px + s * 0.05, py + s * 0.05], fill=color)


def icon_virus(draw, x, y, s, color):
    lw = max(3, s // 14)
    cx, cy, r = x + s * 0.48, y + s * 0.50, s * 0.24
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + s * 0.13) * math.cos(a), cy + (r + s * 0.13) * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=color, width=lw)
        draw.ellipse([x2 - s * 0.05, y2 - s * 0.05, x2 + s * 0.05, y2 + s * 0.05], fill=color)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=lw)
    for ox, oy in ((-0.09, -0.05), (0.08, 0.02), (-0.01, 0.11)):
        draw.ellipse([cx + s * ox - s * 0.035, cy + s * oy - s * 0.035,
                      cx + s * ox + s * 0.035, cy + s * oy + s * 0.035], fill=color)


def _bez(p0, p1, p2, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        px = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        py = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((px, py))
    return pts


def icon_leaf(draw, x, y, s, color):
    lw = max(3, s // 14)
    base = (x + s * 0.16, y + s * 0.84)
    tip = (x + s * 0.84, y + s * 0.16)
    upper = _bez(base, (x + s * 0.30, y + s * 0.18), tip)
    lower = _bez(tip, (x + s * 0.82, y + s * 0.70), base)
    draw.line(upper + lower, fill=color, width=lw, joint="curve")
    # vein from base to tip, stem below base
    draw.line([base[0], base[1], tip[0] - s * 0.06, tip[1] + s * 0.06], fill=color, width=max(2, lw - 1))
    draw.line([base[0], base[1], x + s * 0.08, y + s * 0.94], fill=color, width=lw)
    # small downward arrow (emissions down), clear of the leaf
    ax, ay = x + s * 0.88, y + s * 0.58
    draw.line([ax, ay, ax, ay + s * 0.22], fill=color, width=lw)
    draw.polygon([(ax - s * 0.07, ay + s * 0.17), (ax + s * 0.07, ay + s * 0.17),
                  (ax, ay + s * 0.32)], fill=color)


def icon_drone(draw, x, y, s, color):
    lw = max(3, s // 14)
    cx, cy = x + s * 0.50, y + s * 0.40
    for ox, oy in ((-0.30, -0.20), (0.30, -0.20), (-0.30, 0.20), (0.30, 0.20)):
        rx, ry = cx + s * ox, cy + s * oy
        draw.line([cx, cy, rx, ry], fill=color, width=max(2, lw - 1))
        draw.ellipse([rx - s * 0.10, ry - s * 0.035, rx + s * 0.10, ry + s * 0.035],
                     outline=color, width=max(2, lw - 1))
    draw.rectangle([cx - s * 0.11, cy - s * 0.07, cx + s * 0.11, cy + s * 0.07], outline=color, width=lw)
    draw.ellipse([cx - s * 0.035, cy - s * 0.035, cx + s * 0.035, cy + s * 0.035], fill=color)
    # ground line with small houses (civilians below, no violence depicted)
    gy = y + s * 0.88
    draw.line([x + s * 0.08, gy, x + s * 0.92, gy], fill=color, width=max(2, lw - 1))
    for hx in (0.24, 0.50, 0.76):
        bx = x + s * hx
        draw.rectangle([bx - s * 0.07, gy - s * 0.12, bx + s * 0.07, gy], outline=color, width=max(2, lw - 1))
        draw.polygon([(bx - s * 0.09, gy - s * 0.12), (bx + s * 0.09, gy - s * 0.12), (bx, gy - s * 0.22)], outline=color)


ICONS = {"bridge": icon_bridge, "radar": icon_radar, "globe": icon_globe,
         "virus": icon_virus, "leaf": icon_leaf, "drone": icon_drone}


# ---------------------------------------------------------------- variant A
# Dark tile grid: header band, big lead panel, 3 tiles, then 2 wide tiles.

def variant_a():
    bg = (13, 21, 38)
    panel = (22, 34, 58)
    lead_panel = (26, 42, 74)
    ink = (242, 245, 250)
    muted = (185, 196, 216)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    M = 36

    # header
    d.text((M, 26), "WORLD NEWS", font=font(58, True), fill=ink)
    d.text((W - M, 30), DATE_LINE, font=font(30, True), fill=(255, 209, 102), anchor="ra")
    d.text((W - M, 72), "THE DAY IN ONE IMAGE", font=font(20, True), fill=muted, anchor="ra")
    d.line([M, 118, W - M, 118], fill=(255, 209, 102), width=3)

    # lead panel
    ly0, ly1 = 134, 400
    d.rounded_rectangle([M, ly0, W - M, ly1], radius=18, fill=lead_panel)
    d.rectangle([M, ly0, M + 10, ly1], fill=LEAD["color"])
    tx = M + 34
    cw, _ = chip(d, (tx, ly0 + 22), LEAD["cat"], font(20, True), LEAD["color"], text_color=(255, 255, 255))
    d.text((tx + cw + 14, ly0 + 26), "LEAD STORY", font=font(20, True), fill=muted)
    y = block(d, (tx, ly0 + 68), LEAD["headline"], font(44, True), ink, 690, 52, max_lines=2)
    block(d, (tx, y + 10), LEAD["sub_b"], font(22), muted, 660, 29, max_lines=3)
    icon_bridge(d, 776, ly0 + 76, 176, (140, 190, 255))

    # two rows of 2 tiles, then one wide tile
    gap = 12
    tw = (W - 2 * M - gap) // 2
    ty, th = 416, 172
    for i, story in enumerate(STORIES[:2]):
        draw_tile_a(d, story, M + i * (tw + gap), ty, tw, th, panel, ink, muted)
    ty2 = ty + th + gap
    for i, story in enumerate(STORIES[2:4]):
        draw_tile_a(d, story, M + i * (tw + gap), ty2, tw, th, panel, ink, muted)
    ty3 = ty2 + th + gap
    draw_tile_a(d, STORIES[4], M, ty3, W - 2 * M, 182, panel, ink, muted, wide=True)

    d.text((W // 2, 986), FOOTER, font=font(19), fill=muted, anchor="ma")
    return img


def draw_tile_a(d, story, x0, y0, w0, h0, panel, ink, muted, wide=False):
    d.rounded_rectangle([x0, y0, x0 + w0, y0 + h0], radius=14, fill=panel)
    d.rectangle([x0, y0, x0 + 7, y0 + h0], fill=story["color"])
    tx = x0 + 24
    chip(d, (tx, y0 + 14), story["cat"], font(19, True), story["color"])
    if wide:
        ICONS[story["icon"]](d, x0 + w0 - 96, y0 + 8, 76, story["color"])
        head_w = w0 - 48
    else:
        head_w = w0 - 44
    headline = story.get("tile_headline", story["headline"])
    y = block(d, (tx, y0 + 48), headline, font(30, True), ink,
              head_w, 34, max_lines=2)
    sub = story["sub"] if wide else story["tile_sub"]
    y2 = block(d, (tx, y + 4), sub, font(20), muted, w0 - 44, 23, max_lines=3)
    if y2 > y0 + h0 - 2:
        raise ValueError(f"tile overflow in variant A: {story['cat']} ends {y2} > {y0 + h0 - 2}")


# ---------------------------------------------------------------- variant B
# Newspaper front page: cream paper, black ink, hairline rules, columns.

def variant_b():
    paper = (247, 241, 227)
    ink = (24, 24, 24)
    muted = (84, 78, 66)
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    M = 44

    d.text((W // 2, 14), "WORLD NEWS", font=font(54, True), fill=ink, anchor="ma")
    d.line([M, 84, W - M, 84], fill=ink, width=4)
    d.line([M, 92, W - M, 92], fill=ink, width=1)
    d.text((W // 2, 102), DATE_LINE, font=font(27, True), fill=ink, anchor="ma")
    d.text((W // 2, 140), "The world's day, on one page", font=font(19), fill=muted, anchor="ma")
    d.line([M, 172, W - M, 172], fill=ink, width=2)

    # lead story, full width
    y = 186
    chip(d, (M, y), LEAD["cat"] + " \u00b7 LEAD STORY", font(20, True),
         LEAD["color"], text_color=(255, 255, 255))
    y = block(d, (M, y + 44), LEAD["headline"], font(44, True), ink, 700, 50, max_lines=3)
    icon_bridge(d, W - M - 176, 244, 158, (60, 90, 140), water=(90, 130, 180))
    y = block(d, (M, y + 8), LEAD["sub_b"], font(21), muted, 700, 28, max_lines=2)
    lead_end = y + 16
    d.line([M, lead_end, W - M, lead_end], fill=ink, width=2)

    # three columns
    cols = 3
    gap = 28
    cw2 = (W - 2 * M - (cols - 1) * gap) // cols
    cy = lead_end + 16
    row_h = 246
    for i, story in enumerate(STORIES[:3]):
        x0 = M + i * (cw2 + gap)
        if i:
            d.line([x0 - gap // 2, cy, x0 - gap // 2, cy + row_h - 12], fill=muted, width=1)
        draw_story_b(d, story, x0, cy, cw2, ink, muted, story["b_sub"], row_h,
                     headline=story.get("col_headline", story["headline"]), max_head_lines=4)
    row2 = cy + row_h + 14
    d.line([M, row2 - 8, W - M, row2 - 8], fill=ink, width=1)
    # two wider columns
    cw3 = (W - 2 * M - gap) // 2
    row2_h = 956 - row2
    for i, story in enumerate(STORIES[3:]):
        x0 = M + i * (cw3 + gap)
        if i:
            d.line([x0 - gap // 2, row2, x0 - gap // 2, row2 + row2_h - 10], fill=muted, width=1)
        draw_story_b(d, story, x0, row2, cw3, ink, muted, story["b_sub"], row2_h,
                     headline=story["headline"], max_head_lines=3)

    d.line([M, 968, W - M, 968], fill=ink, width=2)
    d.text((W // 2, 978), FOOTER, font=font(19), fill=muted, anchor="ma")
    return img


def draw_story_b(d, story, x0, y0, w0, ink, muted, sub, max_h, headline=None, max_head_lines=3):
    d.rectangle([x0, y0, x0 + w0, y0 + 6], fill=story["color"])
    d.text((x0, y0 + 14), story["cat"], font=font(19, True), fill=story["color"])
    y = block(d, (x0, y0 + 44), headline or story["headline"], font(30, True), ink, w0, 36, max_lines=max_head_lines)
    y2 = block(d, (x0, y + 5), sub, font(20), muted, w0, 25, max_lines=4)
    if y2 > y0 + max_h:
        raise ValueError(f"column overflow in variant B: {story['cat']} ends {y2} > {y0 + max_h}")


# ---------------------------------------------------------------- variant C
# One huge lead, then a compact numbered list of the other five stories.

def variant_c():
    bg = (16, 16, 20)
    ink = (245, 245, 242)
    muted = (178, 178, 170)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    M = 40

    d.rectangle([0, 0, W, 92], fill=(255, 209, 102))
    d.text((M, 22), "WORLD NEWS", font=font(44, True), fill=(16, 16, 20))
    d.text((W - M, 30), DATE_LINE, font=font(28, True), fill=(16, 16, 20), anchor="ra")

    # lead
    y = 118
    chip(d, (M, y), LEAD["cat"] + " \u00b7 LEAD STORY", font(21, True),
         LEAD["color"], text_color=(255, 255, 255))
    y = block(d, (M, y + 52), LEAD["headline"], font(58, True), ink, 760, 68, max_lines=3)
    icon_bridge(d, W - M - 188, 196, 176, (140, 190, 255))
    y = block(d, (M, y + 12), LEAD["sub"], font(24), muted, W - 2 * M, 32, max_lines=3)
    list_y = y + 34
    d.line([M, list_y - 16, W - M, list_y - 16], fill=(255, 209, 102), width=3)

    # numbered list
    row_h = (968 - list_y) // 5
    for i, story in enumerate(STORIES):
        y0 = list_y + i * row_h
        d.ellipse([M, y0 + 4, M + 50, y0 + 54], fill=story["color"])
        d.text((M + 25, y0 + 10), str(i + 1), font=font(29, True), fill=(10, 10, 12), anchor="ma")
        tx = M + 70
        d.text((tx, y0), story["cat"], font=font(19, True), fill=story["color"])
        yy = block(d, (tx, y0 + 24), story["list_headline"], font(30, True), ink,
                   W - M - tx - 96, 35, max_lines=1)
        y2 = block(d, (tx, yy + 2), story["list_sub"], font(20), muted,
                   W - M - tx - 96, 24, max_lines=1)
        if y2 > y0 + row_h - 2:
            raise ValueError(f"list row overflow in variant C: {story['cat']}")
        ICONS[story["icon"]](d, W - M - 80, y0 + 10, 68, story["color"])
        if i < len(STORIES) - 1:
            d.line([tx, y0 + row_h - 5, W - M, y0 + row_h - 5], fill=(52, 52, 58), width=1)

    d.text((W // 2, 986), FOOTER, font=font(19), fill=muted, anchor="ma")
    return img


# ---------------------------------------------------------------- main

def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path, format="PNG", optimize=True)
    small = img.resize((512, 512), Image.LANCZOS)
    small.save(os.path.join(OUT_DIR, name.replace(".png", "_512.png")), format="PNG", optimize=True)
    print(name, os.path.getsize(path), "bytes")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    save(variant_a(), "variant_a.png")
    save(variant_b(), "variant_b.png")
    save(variant_c(), "variant_c.png")


if __name__ == "__main__":
    main()
