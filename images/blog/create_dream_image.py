"""Create claude-code-dream.png blog image
   Matches the style of agenten-gedaechtnis.png:
   - 640x640, warm beige background
   - Soft, watercolor-inspired illustration
   - Brand colors: warm browns, teals, golds
   - Theme: moon/dreaming + code + memory
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

random.seed(42)

W, H = 640, 640
BG = (247, 244, 231)  # warm beige from original

# Brand palette (extracted from agenten-gedaechtnis.png)
WARM_BROWN = (139, 115, 85)
DARK_BROWN = (92, 77, 61)
TEAL = (55, 130, 135)
TEAL_LIGHT = (80, 155, 150)
GOLD = (210, 180, 100)
GOLD_DARK = (180, 150, 80)
CREAM = (240, 235, 215)
MUTED = (190, 180, 165)

OUT = os.path.join(os.path.dirname(__file__), "claude-code-dream.png")

# Work on RGBA for compositing
canvas = Image.new("RGBA", (W, H), (*BG, 255))

# ── Subtle background texture ──
texture = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(texture)
for _ in range(400):
    x, y = random.randint(0, W), random.randint(0, H)
    r = random.randint(2, 6)
    c = random.choice([WARM_BROWN, TEAL, GOLD, MUTED, DARK_BROWN])
    td.ellipse([x-r, y-r, x+r, y+r], fill=(*c, random.randint(6, 20)))
texture = texture.filter(ImageFilter.GaussianBlur(radius=3))
canvas = Image.alpha_composite(canvas, texture)

# ── Large soft crescent moon (upper area) ──
# Outer glow rings
for ri in range(6, 0, -1):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = 85 + ri * 18
    cx, cy = 320, 185
    gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*GOLD, 4 + ri))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=14))
    canvas = Image.alpha_composite(canvas, glow)

# Moon crescent: draw full circle then cut
moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
md = ImageDraw.Draw(moon)
# Full golden disc
md.ellipse([240, 110, 400, 270], fill=(*GOLD, 210))
# Cut out overlapping circle to make crescent
cut = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cut)
cd.ellipse([270, 95, 415, 260], fill=(255, 255, 255, 255))
# Use the cut as mask: set moon alpha to 0 where cut is opaque
moon_arr = list(moon.getdata())
cut_arr = list(cut.getdata())
result = []
for m, c in zip(moon_arr, cut_arr):
    if c[3] > 0:
        result.append((m[0], m[1], m[2], 0))
    else:
        result.append(m)
moon.putdata(result)
moon = moon.filter(ImageFilter.GaussianBlur(radius=0.8))
canvas = Image.alpha_composite(canvas, moon)

# ── Stars scattered ──
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stars)
star_pos = [
    (130, 95, 3.5), (195, 60, 2.5), (455, 75, 4), (515, 130, 3),
    (545, 200, 3.5), (100, 195, 2.5), (175, 270, 2), (490, 260, 2.5),
    (560, 90, 2), (80, 150, 3), (400, 55, 2.5), (550, 165, 2),
    (220, 300, 2), (485, 310, 2),
]
for sx, sy, sr in star_pos:
    a = random.randint(90, 180)
    sd.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(*GOLD_DARK, a))
    sd.ellipse([sx-sr*2.5, sy-sr*2.5, sx+sr*2.5, sy+sr*2.5], fill=(*GOLD, 15))
stars = stars.filter(ImageFilter.GaussianBlur(radius=0.8))
canvas = Image.alpha_composite(canvas, stars)

# ── Zzz sleep particles ──
zzz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
zd = ImageDraw.Draw(zzz)
try:
    fz1 = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 30)
    fz2 = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 22)
    fz3 = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 15)
except:
    fz1 = fz2 = fz3 = ImageFont.load_default()
zd.text((420, 128), "Z", fill=(*WARM_BROWN, 130), font=fz1)
zd.text((452, 98), "z", fill=(*WARM_BROWN, 100), font=fz2)
zd.text((478, 76), "z", fill=(*WARM_BROWN, 65), font=fz3)
zzz = zzz.filter(ImageFilter.GaussianBlur(radius=0.5))
canvas = Image.alpha_composite(canvas, zzz)

# ── Code editor block (left) ──
code_block = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cb = ImageDraw.Draw(code_block)
# Shadow
cb.rounded_rectangle([82, 337, 257, 517], radius=16, fill=(*DARK_BROWN, 40))
code_block_blur = code_block.filter(ImageFilter.GaussianBlur(radius=6))
canvas = Image.alpha_composite(canvas, code_block_blur)
# Body
code2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cb2 = ImageDraw.Draw(code2)
cb2.rounded_rectangle([78, 332, 252, 512], radius=14, fill=(*DARK_BROWN, 185))
# Title bar
cb2.rounded_rectangle([78, 332, 252, 358], radius=14, fill=(*DARK_BROWN, 220))
cb2.rectangle([78, 348, 252, 358], fill=(*DARK_BROWN, 220))
# Window dots
for i, dc in enumerate([(200, 75, 75), (210, 175, 55), (75, 170, 75)]):
    cb2.ellipse([90 + i*16, 338, 100 + i*16, 348], fill=(*dc, 200))
# Code lines
code_y = 368
code_lines = [
    [(GOLD, 55), (CREAM, 35)],
    [(TEAL_LIGHT, 80), (CREAM, 25)],
    [(CREAM, 45), (GOLD, 50), (TEAL_LIGHT, 20)],
    [(MUTED, 70)],
    [(GOLD, 40), (CREAM, 60)],
    [(TEAL_LIGHT, 50), (GOLD, 30)],
    [(CREAM, 90)],
]
for line in code_lines:
    x = 94
    for color, length in line:
        cb2.rounded_rectangle([x, code_y, x+length, code_y+7], radius=3, fill=(*color, 150))
        x += length + 6
    code_y += 18
canvas = Image.alpha_composite(canvas, code2)

# ── Database / memory cylinder (right) ──
db_block = Image.new("RGBA", (W, H), (0, 0, 0, 0))
db = ImageDraw.Draw(db_block)
# Shadow
db.rounded_rectangle([392, 337, 567, 517], radius=16, fill=(*TEAL, 35))
db_blur = db_block.filter(ImageFilter.GaussianBlur(radius=6))
canvas = Image.alpha_composite(canvas, db_blur)
# Body
db2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(db2)
dd.rounded_rectangle([388, 348, 562, 512], radius=14, fill=(*TEAL, 175))
# Top ellipse cap
dd.ellipse([388, 332, 562, 378], fill=(*TEAL_LIGHT, 200))
# Accent line at top
dd.ellipse([395, 338, 555, 372], fill=(*TEAL, 100))
# Data rows
for ry in range(392, 502, 22):
    dd.rounded_rectangle([404, ry, 546, ry+8], radius=3, fill=(*CREAM, 55))
    # Short segments
    seg_w = random.randint(30, 80)
    dd.rounded_rectangle([404, ry, 404+seg_w, ry+8], radius=3, fill=(*CREAM, 90))
# Small icon at bottom
dd.ellipse([458, 480, 492, 500], fill=(*TEAL_LIGHT, 120))
canvas = Image.alpha_composite(canvas, db2)

# ── Flowing connection: code → memory ──
flow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(flow)
# Dotted arc from code block to db block
for i in range(20):
    t = i / 19
    x = 260 + t * 120
    y = 420 + math.sin(t * math.pi) * (-35) + math.sin(t * math.pi * 3) * 4
    r = 2.5 + math.sin(t * math.pi) * 1
    c_interp = (
        int(DARK_BROWN[0] + (TEAL[0] - DARK_BROWN[0]) * t),
        int(DARK_BROWN[1] + (TEAL[1] - DARK_BROWN[1]) * t),
        int(DARK_BROWN[2] + (TEAL[2] - DARK_BROWN[2]) * t),
    )
    alpha = int(100 + t * 80)
    fd.ellipse([x-r, y-r, x+r, y+r], fill=(*c_interp, alpha))
# Arrowhead
fd.polygon([(382, 410), (395, 420), (382, 430)], fill=(*TEAL, 160))
flow = flow.filter(ImageFilter.GaussianBlur(radius=0.5))
canvas = Image.alpha_composite(canvas, flow)

# ── Soft floating accent nodes ──
nodes = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(nodes)
node_specs = [
    (165, 280, 14, WARM_BROWN), (480, 290, 12, GOLD_DARK),
    (320, 325, 16, GOLD), (110, 460, 10, TEAL_LIGHT),
    (545, 460, 10, WARM_BROWN), (320, 530, 10, MUTED),
]
for nx, ny, nr, nc in node_specs:
    nd.ellipse([nx-nr-6, ny-nr-6, nx+nr+6, ny+nr+6], fill=(*nc, 25))
    nd.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=(*nc, 70))
    nd.ellipse([nx-nr+3, ny-nr+3, nx+nr-3, ny+nr-3], fill=(*nc, 110))
# Faint connecting lines
nd.line([165+14, 280, 94, 420], fill=(*WARM_BROWN, 18), width=1)
nd.line([480-12, 290, 562, 420], fill=(*GOLD_DARK, 18), width=1)
nd.line([320, 325+16, 320, 380], fill=(*GOLD, 20), width=1)
nodes = nodes.filter(ImageFilter.GaussianBlur(radius=2))
canvas = Image.alpha_composite(canvas, nodes)

# ── Soft border vignette ──
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for i in range(20):
    m = i * 2
    a = max(0, 10 - i)
    vd.rounded_rectangle([m, m, W-m, H-m], radius=18, outline=(*MUTED, a), width=2)
canvas = Image.alpha_composite(canvas, vignette)

# ── Text labels ──
text = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tw = ImageDraw.Draw(text)
try:
    font_tag = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 13)
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 28)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 17)
    font_label = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 13)
except:
    font_tag = font_title = font_sub = font_label = ImageFont.load_default()

# Tag pill at top
tag = "CLAUDE CODE"
tb = tw.textbbox((0, 0), tag, font=font_tag)
tl = (W - (tb[2] - tb[0])) // 2
tw.rounded_rectangle([tl-14, 48, tl + (tb[2]-tb[0])+14, 70], radius=11, fill=(*WARM_BROWN, 190))
tw.text((tl, 51), tag, fill=(255, 255, 255, 240), font=font_tag)

# Bottom title
title = "/dream"
ttb = tw.textbbox((0, 0), title, font=font_title)
ttl = (W - (ttb[2]-ttb[0])) // 2
tw.text((ttl, 555), title, fill=(*DARK_BROWN, 235), font=font_title)

# Subtitle
sub = "Memory 2.0 für KI-Agenten"
sb = tw.textbbox((0, 0), sub, font=font_sub)
sl = (W - (sb[2]-sb[0])) // 2
tw.text((sl, 590), sub, fill=(*WARM_BROWN, 175), font=font_sub)

# Block labels
tw.text((118, 518), "Codebasis", fill=(*DARK_BROWN, 170), font=font_label)
tw.text((445, 518), "Memory", fill=(*TEAL, 170), font=font_label)

canvas = Image.alpha_composite(canvas, text)

# ── Final output ──
final = canvas.convert("RGB")
final = final.filter(ImageFilter.GaussianBlur(radius=0.4))

final.save(OUT, "PNG", quality=95)
print(f"Saved: {OUT} ({final.size[0]}x{final.size[1]})")
