#!/usr/bin/env python3
"""Builds the "Navy Gold" Forge skin.

Usage: python3 make_navy_gold.py <forge folder> [output folder]
The output folder defaults to <forge folder>/res/skins/navy_gold.

A skin's sprite_icons.png is read two ways: single pixels at x=70 give the UI
colors, and any icon area left transparent falls back to the default skin's
icon. So the sprite here is transparent apart from the color swatches.
"""
import os
import random
import shutil
import sys

from PIL import Image, ImageDraw, ImageFilter

if len(sys.argv) < 2:
    sys.exit(__doc__)
FORGE = os.path.abspath(sys.argv[1])
DEFAULT = os.path.join(FORGE, "res", "skins", "default")
OUT = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(FORGE, "res", "skins", "navy_gold")

# (x=70, y) swatches, in FSkinProp order
COLORS = [
    (15, 24, 42, 224),     # CLR_THEME
    (217, 168, 67, 110),   # CLR_BORDERS
    (24, 40, 67, 255),     # CLR_ZEBRA
    (52, 78, 120, 255),    # CLR_HOVER
    (46, 84, 140, 255),    # CLR_ACTIVE
    (34, 42, 58, 255),     # CLR_INACTIVE
    (233, 237, 245, 255),  # CLR_TEXT
    (70, 130, 200, 255),   # CLR_PHASE_INACTIVE_ENABLED
    (44, 52, 68, 255),     # CLR_PHASE_INACTIVE_DISABLED
    (217, 168, 67, 255),   # CLR_PHASE_ACTIVE_ENABLED
    (150, 125, 70, 255),   # CLR_PHASE_ACTIVE_DISABLED
    (10, 17, 32, 255),     # CLR_THEME2
    (0, 0, 0, 172),        # CLR_OVERLAY
    (0, 0, 0, 0),          # CLR_COMBAT_TARGETING_ARROW (0 alpha = Forge's built-in color)
    (0, 0, 0, 0),          # CLR_NORMAL_TARGETING_ARROW
    (255, 255, 255, 0),    # CLR_PWATTK_TARGETING_ARROW
]

NAVY_DEEP = (10, 17, 32)
NAVY_MID = (23, 42, 75)


def sprite():
    size = Image.open(os.path.join(DEFAULT, "sprite_icons.png")).size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    for i, rgba in enumerate(COLORS):
        img.putpixel((70, 10 + 20 * i), rgba)
    img.save(os.path.join(OUT, "sprite_icons.png"))


def noise(img, amount, seed):
    rnd = random.Random(seed)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            n = rnd.randint(-amount, amount)
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img


def radial(w, h, inner, outer, cx=0.42, cy=0.45):
    img = Image.new("RGB", (w, h), outer)
    draw = ImageDraw.Draw(img)
    steps = 90
    max_r = int((w ** 2 + h ** 2) ** 0.5 * 0.62)
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(max_r * t)
        col = tuple(int(inner[k] + (outer[k] - inner[k]) * t) for k in range(3))
        draw.ellipse([cx * w - r, cy * h - r * 0.8, cx * w + r, cy * h + r * 0.8], fill=col)
    return img.filter(ImageFilter.GaussianBlur(24))


def backgrounds():
    match = radial(1920, 1080, NAVY_MID, NAVY_DEEP)
    noise(match, 3, 1).save(os.path.join(OUT, "bg_match.jpg"), quality=92)

    tex = Image.new("RGB", (512, 512), (14, 23, 41))
    draw = ImageDraw.Draw(tex)
    for x in range(-512, 1024, 24):  # faint diagonal weave
        draw.line([(x, 0), (x + 512, 512)], fill=(17, 28, 49), width=1)
    noise(tex, 4, 2).save(os.path.join(OUT, "bg_texture.jpg"), quality=92)


def main():
    os.makedirs(OUT, exist_ok=True)
    sprite()
    backgrounds()
    for name in ("bg_splash.png", "font1.ttf"):
        shutil.copyfile(os.path.join(DEFAULT, name), os.path.join(OUT, name))
    print("Navy Gold skin written to", OUT)


if __name__ == "__main__":
    main()
