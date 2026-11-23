"""Draw the 22 November 2026 front page (1024x1024 PNG).

Source data lives in data/stories.json; the picture lands in entry.png at
the repository root. Pillow is the only third-party import, and the drawing
is fully fixed: same fonts, same numbers, no network, no dice rolls, so
re-running this script always writes the same bytes.

Run: python3 tools/render.py
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CANVAS_W, CANVAS_H = 1024, 1024
SIDE = 48
TEXT_W = CANVAS_W - 2 * SIDE

STYLE = {
    "paper": (251, 248, 241),
    "ink": (20, 24, 30),
    "navy": (19, 42, 67),
    "red": (178, 34, 34),
    "gold": (201, 162, 39),
    "grey": (110, 110, 105),
    "rule": (200, 192, 175),
    "body": (52, 56, 62),
    "cream": (245, 240, 225),
    "faint": (238, 234, 222),
}

FONT_FILES = {
    "serif_bold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "sans_bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
}

_cache = {}


def typeface(kind, size):
    """Return a cached Liberation font of the given kind and size."""
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_FILES[kind], size)
    return _cache[key]


def split_lines(draw, text, font, max_w):
    """Greedy word wrap: lines that fit inside max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        attempt = (cur + " " + word).strip()
        if draw.textlength(attempt, font=font) <= max_w:
            cur = attempt
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put_lines(draw, x, y, lines, font, colour, spacing):
    """Paint a list of lines from (x, y); return the y below the last one."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=colour)
        y += font.size + spacing
    return y


def draw_masthead(draw, data):
    """Navy band: paper name over the date, gold rule underneath."""
    draw.rectangle([0, 0, CANVAS_W, 148], fill=STYLE["navy"])
    name_font = typeface("serif_bold", 44)
    date_font = typeface("sans_bold", 54)
    name = data["masthead"]
    date = data["date"]
    name_w = draw.textlength(name, font=name_font)
    draw.text(((CANVAS_W - name_w) / 2, 14), name, font=name_font,
              fill=STYLE["cream"])
    date_w = draw.textlength(date, font=date_font)
    draw.text(((CANVAS_W - date_w) / 2, 68), date, font=date_font,
              fill=STYLE["gold"])
    for cx in (SIDE + 10, CANVAS_W - SIDE - 10):
        cy = 96
        draw.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)],
                     fill=STYLE["gold"])
    draw.line([0, 148, CANVAS_W, 148], fill=STYLE["gold"], width=4)


def draw_lead(draw, data, y):
    """Lead story: red kicker, big headline, summary, then a rule."""
    item = data["lead"]
    kick = typeface("sans_bold", 21)
    draw.text((SIDE, y), item["kicker"], font=kick, fill=STYLE["red"])
    y += 30
    head = typeface("sans_bold", 47)
    rows = split_lines(draw, item["headline"], head, TEXT_W)
    y = put_lines(draw, SIDE, y, rows, head, STYLE["ink"], 6)
    y += 6
    body = typeface("sans", 25)
    rows = split_lines(draw, item["summary"], body, TEXT_W)
    y = put_lines(draw, SIDE, y, rows, body, STYLE["body"], 4)
    y += 18
    draw.line([SIDE, y, CANVAS_W - SIDE, y], fill=STYLE["rule"], width=2)
    return y + 20


def draw_grid(draw, data, top):
    """Four secondary stories in a 2x2 grid with column and row rules."""
    cell_w = (TEXT_W - 28) // 2
    cell_h = 208
    for idx, story in enumerate(data["stories"]):
        col, row = idx % 2, idx // 2
        x = SIDE + col * (cell_w + 28)
        sy = top + row * cell_h
        kick = typeface("sans_bold", 18)
        draw.text((x, sy), story["kicker"], font=kick, fill=STYLE["red"])
        sy += 28
        head = typeface("sans_bold", 31)
        rows = split_lines(draw, story["headline"], head, cell_w)
        sy = put_lines(draw, x, sy, rows[:2], head, STYLE["ink"], 3)
        sy += 4
        body = typeface("sans", 21)
        rows = split_lines(draw, story["summary"], body, cell_w)
        put_lines(draw, x, sy, rows[:3], body, STYLE["body"], 3)
    mid = SIDE + cell_w + 14
    draw.line([mid, top + 4, mid, top + 2 * cell_h - 12], fill=STYLE["rule"],
              width=2)
    draw.line([SIDE, top + cell_h - 8, CANVAS_W - SIDE, top + cell_h - 8],
              fill=STYLE["rule"], width=2)
    return top + 2 * cell_h + 6


def draw_also(draw, data, y):
    """Navy 'also today' band, then the centred footer line."""
    draw.rectangle([0, y, CANVAS_W, y + 92], fill=STYLE["navy"])
    tag_font = typeface("sans_bold", 19)
    tag = "ALSO TODAY  "
    draw.text((SIDE, y + 12), tag, font=tag_font, fill=STYLE["gold"])
    lx = SIDE + draw.textlength(tag, font=tag_font)
    joined = "  \u2022  ".join(data["also"])
    body = typeface("sans", 19)
    rows = split_lines(draw, joined, body, CANVAS_W - SIDE - lx - 8)
    cy = y + 12
    for line in rows[:3]:
        draw.text((lx, cy), line, font=body, fill=STYLE["faint"])
        cy += 24
    foot = typeface("sans", 16)
    note = data["footer"]
    note_w = draw.textlength(note, font=foot)
    draw.text(((CANVAS_W - note_w) / 2, y + 92 + 12), note, font=foot,
              fill=STYLE["grey"])


def render():
    with open(os.path.join(ROOT, "data", "stories.json"),
              encoding="utf-8") as fh:
        data = json.load(fh)
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), STYLE["paper"])
    draw = ImageDraw.Draw(img)
    draw_masthead(draw, data)
    y = draw_lead(draw, data, 172)
    y = draw_grid(draw, data, y)
    draw_also(draw, data, y)
    out = os.path.join(ROOT, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]}, {size} bytes)")


if __name__ == "__main__":
    render()
