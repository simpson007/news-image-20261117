#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Run: python3 render.py  -> writes entry.png beside this file.
Deterministic: fixed text, fixed geometry, no time, no randomness, no network.
Only the Python standard library + Pillow are used to render; the entry
program itself (main.ts) only copies the finished entry.png.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (16, 38, 63)
NAVY2 = (24, 56, 90)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
TEAL = (14, 77, 92)
TEAL_DK = (9, 52, 64)
GRAY = (88, 88, 88)
SKY = (223, 232, 238)
WHITE = (255, 255, 255)
ORANGE = (232, 120, 30)
YELLOW = (245, 196, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, maxw, lh):
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def burst(d, cx, cy, r_outer, r_inner, n, fill):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def hline(d, x0, x1, y, fill, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_sea(d, x, y, w, h):
    """Strait of Hormuz at night: dark sea, a tanker, an explosion."""
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(TEAL_DK[k] + (TEAL[k] - TEAL_DK[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # moon
    d.ellipse([x + w - 78, y + 16, x + w - 38, y + 56], fill=(240, 230, 190))
    # ship: hull + containers + funnel
    hx, hy = x + 36, y + h - 78
    d.polygon([(hx, hy), (hx + 250, hy), (hx + 228, hy + 34),
               (hx + 18, hy + 34)], fill=(10, 26, 40))
    for i, col in enumerate([(178, 52, 44), (201, 162, 39), (40, 90, 110),
                             (178, 52, 44), (201, 162, 39)]):
        d.rectangle([hx + 22 + i * 42, hy - 30, hx + 58 + i * 42, hy - 2],
                    fill=col)
    d.rectangle([hx + 238, hy - 52, hx + 262, hy - 2], fill=(10, 26, 40))
    # explosion above the ship
    ex, ey = x + 330, y + 78
    burst(d, ex, ey, 52, 22, 10, ORANGE)
    burst(d, ex, ey, 30, 13, 10, YELLOW)
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 240, 180))
    # smoke puffs
    for sx, sy, sr in [(ex - 58, ey - 30, 20), (ex + 52, ey - 42, 24),
                       (ex + 78, ey - 6, 17)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 125, 130))
    # waves
    for wy in (y + h - 22, y + h - 10):
        for wx in range(x + 8, x + w - 30, 46):
            d.arc([wx, wy, wx + 34, wy + 14], 180, 360, fill=(160, 200, 210),
                  width=2)
    # alert label
    d.text((x + 12, y + 12), "STRAIT OF HORMUZ", font=SANS_B(17), fill=WHITE)


def draw_bridge(d, x, y, w, h):
    """A suspension bridge under a drone sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 140, 160))
    for wy in (y + h - 18, y + h - 8):
        for wx in range(x + 6, x + w - 24, 38):
            d.arc([wx, wy, wx + 28, wy + 10], 180, 360, fill=(220, 235, 240),
                  width=2)
    # towers
    for tx in (x + 90, x + w - 118):
        d.rectangle([tx, y + 12, tx + 22, y + h - 26], fill=(60, 60, 66))
    # deck + cables
    d.rectangle([x, y + h - 52, x + w, y + h - 44], fill=(40, 40, 46))
    for cx in range(x + 10, x + w - 10, 34):
        d.line([(x + 101, y + 14), (cx, y + h - 50)], fill=(110, 110, 116),
               width=1)
        d.line([(x + w - 107, y + 14), (cx, y + h - 50)], fill=(110, 110, 116),
               width=1)
    # drones: small dark diamonds
    for dx, dy in [(x + 30, y + 16), (x + 70, y + 30), (x + 170, y + 12),
                   (x + 300, y + 22), (x + 380, y + 10), (x + 430, y + 32)]:
        d.polygon([(dx, dy - 5), (dx + 5, dy), (dx, dy + 5), (dx - 5, dy)],
                  fill=(30, 30, 34))
    # blast on the deck
    bx, by = x + w // 2, y + h - 58
    burst(d, bx, by, 26, 11, 8, ORANGE)
    burst(d, bx, by, 14, 6, 8, YELLOW)


def draw_skyline(d, x, y, w, h):
    """Manila at dusk: skyline silhouettes and a low sun."""
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int((250 - 60 * t)) if k == 0 else
                  int((190 - 90 * t)) if k == 1 else
                  int((120 + 40 * t)) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(245, 196, 60))
    heights = [34, 52, 40, 62, 46, 56, 38, 50]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, y + h - bh, bx + bw - 2, y + h], fill=(40, 36, 54))
        for wy in range(y + h - bh + 6, y + h - 6, 12):
            for wx in range(bx + 6, bx + bw - 8, 12):
                if (wx + wy) % 24 < 12:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 210, 90))


def draw_chart(d, x, y, w, h):
    """A falling market line."""
    pts = [(x + i * w / 9, y + h * (0.15 + 0.75 * i / 9) +
            (6 if i % 3 else -6)) for i in range(10)]
    d.line(pts, fill=GOLD_LT, width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 14, pts[-1][1] - 16),
               (pts[-1][0] - 2, pts[-1][1] - 2)], fill=(220, 60, 50))
    d.text((x, y - 2), "", font=SANS_B(10), fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=SERIF_B(54),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 74), "TUESDAY  ·  17 NOVEMBER 2026", font=SANS_B(28),
           fill=GOLD_LT, anchor="ma")
    hline(d, 0, W, 118, GOLD, 4)

    # ---- lead story ----------------------------------------------------
    d.text((40, 134), "THE GULF  —  WAR AT SEA", font=SANS_B(21), fill=RED)
    d.text((40, 160), "US AND IRAN TRADE BLOWS", font=SANS_B(40), fill=INK)
    d.text((40, 202), "AS A TANKER BURNS IN HORMUZ", font=SANS_B(40),
           fill=INK)
    draw_sea(d, 40, 248, 560, 216)
    lx = 624
    y = para(d, lx, 252,
             "Bahrain said its defences shot down several Iranian drones "
             "aimed at a US radar site — the third such attempt in five days.",
             SANS(19), INK, 360, 24)
    y = para(d, lx, y + 8,
             "US warplanes then hit a missile launch site on Qeshm Island.",
             SANS(19), INK, 360, 24)
    para(d, lx, y + 8,
         "A tanker was hit by a mine off Oman: 24 crew evacuated, "
         "two hurt, one sailor missing.",
         SANS(19), INK, 360, 24)
    hline(d, 40, 984, 480, (200, 192, 170), 2)

    # ---- middle row: Ukraine + Manila ----------------------------------
    # Ukraine, left column
    draw_bridge(d, 40, 494, 452, 74)
    d.text((40, 578), "UKRAINE", font=SANS_B(20), fill=RED)
    d.text((40, 602), "KYIV'S 1,300 DRONES HIT", font=SANS_B(26), fill=INK)
    d.text((40, 632), "THE CRIMEA BRIDGE", font=SANS_B(26), fill=INK)
    para(d, 40, 666,
         "Traffic halted on the bridge to Crimea; Russia struck bridges "
         "in Kyiv in reply.", SANS(18), (60, 60, 60), 452, 22)
    # Manila, right column
    draw_skyline(d, 532, 494, 452, 74)
    d.text((532, 578), "MANILA  —  ASEAN & THE QUAD", font=SANS_B(20),
           fill=RED)
    d.text((532, 602), "TRUMP MEETS MODI", font=SANS_B(26), fill=INK)
    d.text((532, 632), "AT THE QUAD", font=SANS_B(26), fill=INK)
    para(d, 532, 666,
         "Trump called Modi “a tough man”, vowed the US would catch up "
         "with China on rare earths, and said he may meet Kim Jong Un "
         "in China.", SANS(18), (60, 60, 60), 452, 22)
    hline(d, 40, 984, 732, (200, 192, 170), 2)

    # ---- markets strip ---------------------------------------------------
    d.rectangle([0, 742, W, 832], fill=NAVY)
    d.text((40, 754), "MARKETS TUMBLE", font=SANS_B(26), fill=GOLD_LT)
    draw_chart(d, 330, 752, 180, 66)
    d.text((530, 754),
           "Nasdaq −2.5% · S&P −1.9% · Dow −1.4%",
           font=SANS_B(20), fill=WHITE)
    d.text((530, 788),
           "Brent −3.6% to $92.44  ·  Gold −0.8% to $3,848",
           font=SANS(19), fill=(200, 210, 220))
    d.text((40, 782), "Nasdaq enters correction", font=SANS(19),
           fill=(200, 210, 220))

    # ---- bottom row: four short stories ---------------------------------
    cards = [
        ("CLIMATE — COP31", RED,
         "Draft deal urges a faster exit from fossil fuels"),
        ("EUROPE", (14, 90, 60),
         "Five EU states plan a Rwanda hub for asylum claims"),
        ("JAPAN", (90, 60, 120),
         "Jets scrambled as Russian planes enter its airspace"),
        ("GAZA", (120, 70, 20),
         "West presses Israel to open crossings as illness spreads"),
    ]
    cx = 40
    for kicker, color, head in cards:
        d.rectangle([cx, 844, cx + 226, 850], fill=color)
        d.text((cx, 860), kicker, font=SANS_B(17), fill=color)
        para(d, cx, 884, head, SANS_B(20), INK, 226, 25)
        cx += 238
    hline(d, 40, 984, 972, (200, 192, 170), 2)

    # ---- footer ----------------------------------------------------------
    d.text((W // 2, 984),
           "ALSO: Pattinson is the new James Bond  ·  Amazon loses 40 "
           "satellites  ·  Delhi chokes in smog",
           font=SANS(16), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
