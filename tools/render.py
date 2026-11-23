"""Render the 22 November 2026 front page as a 1024x1024 PNG.

Reads data/stories.json and writes entry.png in the repository root.
Pillow only; fixed fonts, no network, no randomness, so every run writes
the same bytes. Usage: python3 tools/render.py
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H = 1024, 1024
MARGIN = 48
INNER = W - 2 * MARGIN

PAPER = (251, 248, 241)
INK = (20, 24, 30)
NAVY = (19, 42, 67)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (110, 110, 105)
RULE = (200, 192, 175)
BODY = (52, 56, 62)
CREAM = (245, 240, 225)
FAINT = (238, 234, 222)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, limit):
    """Break text into lines that fit within limit pixels."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= limit:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_lines(draw, x, y, lines, font, colour, lead):
    """Draw lines starting at (x, y); return the y after the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=colour)
        y += font.size + lead
    return y


class FrontPage:
    """Builds the 1024x1024 front page from the story data."""

    def __init__(self, stories):
        self.stories = stories
        self.canvas = Image.new("RGB", (W, H), PAPER)
        self.draw = ImageDraw.Draw(self.canvas)

    def masthead(self):
        d = self.draw
        d.rectangle([0, 0, W, 148], fill=NAVY)
        title_font = load_font(SERIF_B, 44)
        date_font = load_font(SANS_B, 54)
        title = self.stories["masthead"]
        date = self.stories["date"]
        tw = d.textlength(title, font=title_font)
        d.text(((W - tw) / 2, 14), title, font=title_font, fill=CREAM)
        dw = d.textlength(date, font=date_font)
        d.text(((W - dw) / 2, 68), date, font=date_font, fill=GOLD)
        for cx in (MARGIN + 10, W - MARGIN - 10):
            cy = 96
            d.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)],
                      fill=GOLD)
        d.line([0, 148, W, 148], fill=GOLD, width=4)

    def top_story(self, y):
        d = self.draw
        item = self.stories["lead"]
        kick_font = load_font(SANS_B, 21)
        d.text((MARGIN, y), item["kicker"], font=kick_font, fill=RED)
        y += 30
        head_font = load_font(SANS_B, 47)
        rows = wrap(d, item["headline"], head_font, INNER)
        y = draw_lines(d, MARGIN, y, rows, head_font, INK, 6)
        y += 6
        text_font = load_font(SANS, 25)
        rows = wrap(d, item["summary"], text_font, INNER)
        y = draw_lines(d, MARGIN, y, rows, text_font, BODY, 4)
        y += 18
        d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
        return y + 20

    def story_grid(self, top):
        d = self.draw
        cell_w = (INNER - 28) // 2
        cell_h = 208
        for i, story in enumerate(self.stories["stories"]):
            col, row = i % 2, i // 2
            x = MARGIN + col * (cell_w + 28)
            sy = top + row * cell_h
            kick_font = load_font(SANS_B, 18)
            d.text((x, sy), story["kicker"], font=kick_font, fill=RED)
            sy += 28
            head_font = load_font(SANS_B, 31)
            rows = wrap(d, story["headline"], head_font, cell_w)
            sy = draw_lines(d, x, sy, rows[:2], head_font, INK, 3)
            sy += 4
            text_font = load_font(SANS, 21)
            rows = wrap(d, story["summary"], text_font, cell_w)
            draw_lines(d, x, sy, rows[:3], text_font, BODY, 3)
        mid = MARGIN + cell_w + 14
        d.line([mid, top + 4, mid, top + 2 * cell_h - 12], fill=RULE, width=2)
        d.line([MARGIN, top + cell_h - 8, W - MARGIN, top + cell_h - 8],
               fill=RULE, width=2)
        return top + 2 * cell_h + 6

    def also_today(self, y):
        d = self.draw
        d.rectangle([0, y, W, y + 92], fill=NAVY)
        tag_font = load_font(SANS_B, 19)
        tag = "ALSO TODAY  "
        d.text((MARGIN, y + 12), tag, font=tag_font, fill=GOLD)
        lx = MARGIN + d.textlength(tag, font=tag_font)
        joined = "  \u2022  ".join(self.stories["also"])
        text_font = load_font(SANS, 19)
        rows = wrap(d, joined, text_font, W - MARGIN - lx - 8)
        cy = y + 12
        for line in rows[:3]:
            d.text((lx, cy), line, font=text_font, fill=FAINT)
            cy += 24
        foot_font = load_font(SANS, 16)
        note = self.stories["footer"]
        nw = d.textlength(note, font=foot_font)
        d.text(((W - nw) / 2, y + 92 + 12), note, font=foot_font, fill=GREY)

    def build(self):
        self.masthead()
        y = self.top_story(172)
        y = self.story_grid(y)
        self.also_today(y)
        out = os.path.join(ROOT, "entry.png")
        self.canvas.save(out, "PNG", optimize=True)
        size = os.path.getsize(out)
        print(f"wrote {out} ({self.canvas.size[0]}x{self.canvas.size[1]}, {size} bytes)")


def main():
    with open(os.path.join(ROOT, "data", "stories.json"),
              encoding="utf-8") as fh:
        stories = json.load(fh)
    FrontPage(stories).build()


if __name__ == "__main__":
    main()
