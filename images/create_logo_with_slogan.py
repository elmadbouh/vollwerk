"""Create vollwerk_logo_with_slogan.png
   The original vollwerk_gbp_logo.png already contains "vollwerk AI"
   (including the brown AI badge). This script:
   1. Removes the background → transparent
   2. Crops tightly to the content
   3. Adds the uppercase slogan below, sized to match the logo width
   4. Saves as a single PNG ready for the Word header
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

SRC = os.path.join(os.path.dirname(__file__), "vollwerk_gbp_logo.png")
DST = os.path.join(os.path.dirname(__file__), "vollwerk_logo_with_slogan.png")

# -- Colour --
TEXT_MUTED = (154, 142, 130, 255)  # #9A8E82

# 1. Load & remove background
img = Image.open(SRC).convert("RGBA")
arr = np.array(img)
bg = arr[0, 0, :3].astype(float)
diff = np.sqrt(np.sum((arr[:, :, :3].astype(float) - bg) ** 2, axis=2))
arr[:, :, 3] = np.where(diff < 30, 0, 255).astype(np.uint8)

# 2. Crop to content
alpha = arr[:, :, 3]
rows = np.where(np.any(alpha > 10, axis=1))[0]
cols = np.where(np.any(alpha > 10, axis=0))[0]
rmin, rmax = rows[0], rows[-1]
cmin, cmax = cols[0], cols[-1]
pad = 4
logo = Image.fromarray(arr).crop(
    (cmin - pad, rmin - pad, cmax + pad + 1, rmax + pad + 1)
)
lw, lh = logo.size
print(f"Cropped logo (vollwerk AI): {lw}x{lh}")

# 3. Size the slogan to exactly match the logo width
slogan = "KI-PROJEKTE  \u00b7  VOLLST\u00c4NDIG GELIEFERT"
font_path = r"C:\Windows\Fonts\calibri.ttf"

# Binary search for the font size that makes text width closest to logo width
lo, hi = 6, 80
best_size = lo
while lo <= hi:
    mid = (lo + hi) // 2
    fnt = ImageFont.truetype(font_path, mid)
    tw = fnt.getbbox(slogan)[2] - fnt.getbbox(slogan)[0]
    if tw <= lw:
        best_size = mid
        lo = mid + 1
    else:
        hi = mid - 1

fnt = ImageFont.truetype(font_path, best_size)
sbbox = fnt.getbbox(slogan)
stw = sbbox[2] - sbbox[0]
sth = sbbox[3] - sbbox[1]
print(f"Slogan: font {best_size}pt, width {stw}px (logo {lw}px), height {sth}px")

# 4. Compose final image
gap = max(4, int(lh * 0.08))
total_h = lh + gap + sth + 4
canvas = Image.new("RGBA", (lw, total_h), (0, 0, 0, 0))

# Logo at top (full width)
canvas.paste(logo, (0, 0), logo)

# Slogan centred below
draw = ImageDraw.Draw(canvas)
text_x = (lw - stw) // 2
text_y = lh + gap - sbbox[1]
draw.text((text_x, text_y), slogan, font=fnt, fill=TEXT_MUTED)

# 5. Final tight crop (remove any remaining transparent edge)
fa = np.array(canvas)[:, :, 3]
fr = np.where(np.any(fa > 5, axis=1))[0]
fc = np.where(np.any(fa > 5, axis=0))[0]
p = 2
final = canvas.crop((
    max(0, fc[0] - p), max(0, fr[0] - p),
    min(lw, fc[-1] + p + 1), min(total_h, fr[-1] + p + 1)
))

print(f"Final: {final.size}")
final.save(DST)
print(f"Saved: {DST}")
