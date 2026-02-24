"""
Export Vollwerk business card front & back as two PDFs (85 x 54 mm each).
Uses reportlab — no native dependencies required on Windows.

Usage:  python export_visitenkarten.py
Output: visitenkarte_front.pdf, visitenkarte_back.pdf
"""

import os
import io
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode

# ── Page size ─────────────────────────────────────────────────────────────────
W = 85 * mm
H = 54 * mm

# ── Colours ───────────────────────────────────────────────────────────────────
BROWN        = HexColor("#7C6040")
BROWN_MID    = HexColor("#9B7A52")
BROWN_LIGHT  = HexColor("#B8956A")
BROWN_PALE   = HexColor("#D4B896")
BROWN_WASH   = HexColor("#EDE3D6")
TEXT_PRIMARY  = HexColor("#2A2318")
TEXT_BODY     = HexColor("#4A4035")
TEXT_MUTED    = HexColor("#9A8E82")
BG_CARD      = HexColor("#FDFAF5")
BG_CARD_ALT  = HexColor("#F7F3EB")
BORDER_COLOR  = Color(0.486, 0.376, 0.251, alpha=0.18)

# ── Font registration ────────────────────────────────────────────────────────
# Montserrat  → substitute for DM Sans  (geometric sans-serif)
# Cormorant Infant → substitute for Cormorant Garamond (same family, elegant serif)
FONTS_DIR = "C:/Windows/Fonts"

pdfmetrics.registerFont(TTFont("Montserrat",        f"{FONTS_DIR}/Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold",   f"{FONTS_DIR}/Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Italic", f"{FONTS_DIR}/Montserrat-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-BoldItalic", f"{FONTS_DIR}/Montserrat-BoldItalic.ttf"))

pdfmetrics.registerFont(TTFont("Cormorant",         f"{FONTS_DIR}/CormorantInfant-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-Bold",    f"{FONTS_DIR}/CormorantInfant-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-Italic",  f"{FONTS_DIR}/CormorantInfant-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-BoldItalic", f"{FONTS_DIR}/CormorantInfant-BoldItalic.ttf"))

# Register font families so bold/italic selection works automatically
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Montserrat",
                   normal="Montserrat", bold="Montserrat-Bold",
                   italic="Montserrat-Italic", boldItalic="Montserrat-BoldItalic")
registerFontFamily("Cormorant",
                   normal="Cormorant", bold="Cormorant-Bold",
                   italic="Cormorant-Italic", boldItalic="Cormorant-BoldItalic")

SANS         = "Montserrat"
SANS_BOLD    = "Montserrat-Bold"
SERIF        = "Cormorant"
SERIF_BOLD   = "Cormorant-Bold"
SERIF_ITALIC = "Cormorant-Italic"


def generate_qr_image(url: str, color: str = "#7C6040"):
    """Generate a QR code as a PIL Image."""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")
    return img.get_image()


# ══════════════════════════════════════════════════════════════════════════════
#  FRONT SIDE
# ══════════════════════════════════════════════════════════════════════════════

def draw_front(c: canvas.Canvas):
    # Background
    c.setFillColor(BG_CARD)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Dot grid (top-left, decorative)
    c.saveState()
    c.setFillColor(Color(0.72, 0.58, 0.42, alpha=0.35))
    for row in range(5):
        for col in range(5):
            cx = 2*mm + col * 2.5*mm
            cy = H - 2*mm - row * 2.5*mm
            c.circle(cx, cy, 0.4*mm, fill=1, stroke=0)
    c.restoreState()

    # Warm wash circle (bottom-right)
    c.saveState()
    c.setFillColor(Color(0.929, 0.890, 0.839, alpha=0.35))
    c.circle(W + 2*mm, -2*mm, 18*mm, fill=1, stroke=0)
    c.restoreState()

    # Top accent bar (3-segment gradient)
    bar_h = 0.8*mm
    bar_y = H - bar_h
    for x1, x2, col in [(0, W*0.45, BROWN), (W*0.45, W*0.75, BROWN_LIGHT),
                         (W*0.75, W, BROWN_PALE)]:
        c.setFillColor(col)
        c.rect(x1, bar_y, x2-x1, bar_h, fill=1, stroke=0)

    # ── Logo "Vollwerk AI" ──
    x0 = 7*mm
    y_logo = H - 13*mm

    c.setFont(SERIF_BOLD, 22)
    c.setFillColor(TEXT_PRIMARY)
    voll_w = c.stringWidth("Voll", SERIF_BOLD, 22)
    c.drawString(x0, y_logo, "Voll")

    c.setFillColor(BROWN)
    werk_w = c.stringWidth("werk", SERIF_BOLD, 22)
    c.drawString(x0 + voll_w, y_logo, "werk")

    # AI badge
    ai_x = x0 + voll_w + werk_w + 2*mm
    ai_fs = 8
    ai_tw = c.stringWidth("AI", SANS_BOLD, ai_fs)
    badge_w = ai_tw + 3*mm
    badge_h = 3.8*mm
    c.setFillColor(BROWN)
    c.roundRect(ai_x, y_logo - 0.3*mm, badge_w, badge_h, 1*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(SANS_BOLD, ai_fs)
    c.drawString(ai_x + 1.5*mm, y_logo + 1*mm, "AI")

    # Tagline
    c.setFillColor(TEXT_MUTED)
    c.setFont(SANS, 5.5)
    c.drawString(x0, y_logo - 4.5*mm, "KI-PROJEKTE  ·  VOLLSTÄNDIG GELIEFERT")

    # ── Credential pill (top-right) ──
    pill_text = "20+ JAHRE FINANCE IT"
    pill_fs = 5.5
    pill_tw = c.stringWidth(pill_text, SANS_BOLD, pill_fs)
    pill_w = pill_tw + 6*mm
    pill_h = 4*mm
    pill_x = W - 7*mm - pill_w
    pill_y = H - 10*mm

    c.setFillColor(BROWN_WASH)
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 2*mm, fill=1, stroke=1)

    c.setFillColor(BROWN)
    c.circle(pill_x + 2.5*mm, pill_y + pill_h/2, 0.65*mm, fill=1, stroke=0)

    c.setFont(SANS_BOLD, pill_fs)
    c.drawString(pill_x + 4.5*mm, pill_y + 1*mm, pill_text)

    # ── Divider line (5 mm tall, centred between name/contact blocks) ──
    div_x = 51*mm
    div_mid = 10*mm          # vertical midpoint of the bottom row
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.25)
    c.line(div_x, div_mid - 2.5*mm, div_x, div_mid + 2.5*mm)

    # ── Person block (bottom-left) ──
    c.setFillColor(TEXT_PRIMARY)
    c.setFont(SANS_BOLD, 11)
    c.drawString(x0, 14*mm, "Adil El Madbouh")

    c.setFillColor(BROWN_MID)
    c.setFont(SANS, 5.5)
    c.drawString(x0, 10*mm, "GRÜNDER")
    c.drawString(x0, 6.5*mm, "AI CONSULTANT & DELIVERY MANAGER")

    # ── Contact block (bottom-right) ──
    rx = W - 7*mm
    c.setFillColor(TEXT_MUTED)
    c.setFont(SANS, 6)
    c.drawRightString(rx, 12*mm, "adil@vollwerk.de")
    c.drawRightString(rx, 8.5*mm, "+49 176 6343 1659")
    c.drawRightString(rx, 5*mm, "vollwerk.de")


# ══════════════════════════════════════════════════════════════════════════════
#  BACK SIDE
# ══════════════════════════════════════════════════════════════════════════════

def draw_back(c: canvas.Canvas):
    # Background
    c.setFillColor(BG_CARD_ALT)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle horizontal rules
    c.saveState()
    c.setStrokeColor(Color(0.486, 0.376, 0.251, alpha=0.05))
    c.setLineWidth(0.2)
    y = 7*mm
    while y < H:
        c.line(0, y, W, y)
        y += 7*mm
    c.restoreState()

    # Bottom accent bar
    bar_h = 0.8*mm
    for x1, x2, col in [(0, W*0.25, BG_CARD_ALT), (W*0.25, W*0.55, BROWN_PALE),
                         (W*0.55, W*0.80, BROWN), (W*0.80, W, BROWN_LIGHT)]:
        c.setFillColor(col)
        c.rect(x1, 0, x2-x1, bar_h, fill=1, stroke=0)

    # Warm wash (top-right)
    c.saveState()
    c.setFillColor(Color(0.929, 0.890, 0.839, alpha=0.30))
    c.circle(W + 5*mm, H + 5*mm, 16*mm, fill=1, stroke=0)
    c.restoreState()

    # QR column divider
    qr_col_x = W - 22*mm
    c.setStrokeColor(Color(0.486, 0.376, 0.251, alpha=0.10))
    c.setLineWidth(0.25)
    c.line(qr_col_x, 3*mm, qr_col_x, H - 3*mm)

    # ── Back logo (top-left) ──
    lx = 5*mm
    ly = H - 5.5*mm

    c.setFont(SERIF_BOLD, 10)
    c.setFillColor(TEXT_PRIMARY)
    vw = c.stringWidth("Voll", SERIF_BOLD, 10)
    c.drawString(lx, ly, "Voll")
    c.setFillColor(BROWN)
    ww = c.stringWidth("werk", SERIF_BOLD, 10)
    c.drawString(lx + vw, ly, "werk")

    aix = lx + vw + ww + 1*mm
    c.setFillColor(BROWN)
    c.roundRect(aix, ly - 0.2*mm, 5*mm, 3*mm, 0.7*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(SANS_BOLD, 5.5)
    c.drawString(aix + 1*mm, ly + 0.4*mm, "AI")

    # ── Value propositions ──
    vp_data = [
        ("KI-PROJEKTE — VON A BIS Z",
         "Strategie, Umsetzung & Betrieb aus einer Hand"),
        ("AUTOMATISIERUNG >70%",
         "Bei hochkomplexen & Routineaufgaben"),
        ("4 KLARE SCHRITTE ZUM ZIEL",
         "Beratung > Umsetzung > Training > Betrieb"),
    ]

    vp_y_start = H - 14*mm
    vp_gap = 8.5*mm

    for i, (title, sub) in enumerate(vp_data):
        vy = vp_y_start - i * vp_gap

        c.setFillColor(BROWN)
        c.circle(lx + 0.65*mm, vy + 1*mm, 0.65*mm, fill=1, stroke=0)

        c.setFillColor(TEXT_PRIMARY)
        c.setFont(SANS_BOLD, 6)
        c.drawString(lx + 3.5*mm, vy + 0.5*mm, title)

        c.setFillColor(TEXT_BODY)
        c.setFont(SERIF_ITALIC, 7.5)
        c.drawString(lx + 3.5*mm, vy - 3*mm, sub)

    # ── Stats row ──
    stats_top_y = 11*mm
    stats_y = 4.5*mm

    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.25)
    c.line(lx, stats_top_y, qr_col_x - 3*mm, stats_top_y)

    stats = [("20+", "JAHRE IT"), (">70%", "AUTOMATISIERUNG"), ("4", "SCHRITTE")]
    stat_area_w = qr_col_x - 3*mm - lx
    stat_w = stat_area_w / 3

    for i, (num, label) in enumerate(stats):
        sx = lx + i * stat_w + stat_w / 2

        c.setFillColor(BROWN)
        c.setFont(SERIF_BOLD, 14)
        c.drawCentredString(sx, stats_y + 2*mm, num)

        c.setFillColor(TEXT_MUTED)
        c.setFont(SANS, 4.5)
        c.drawCentredString(sx, stats_y - 1*mm, label)

        if i < 2:
            sep_x = lx + (i + 1) * stat_w
            c.setStrokeColor(BORDER_COLOR)
            c.line(sep_x, stats_y - 1*mm, sep_x, stats_y + 5.5*mm)

    # ── QR Code ──
    qr_center_x = qr_col_x + (W - qr_col_x) / 2
    qr_size = 14.5*mm
    qr_y = H / 2 + 1*mm

    frame_pad = 1.5*mm
    frame_size = qr_size + 2 * frame_pad
    frame_x = qr_center_x - frame_size / 2
    frame_y = qr_y - frame_size / 2

    c.setFillColor(white)
    c.setStrokeColor(BROWN_PALE)
    c.setLineWidth(0.4)
    c.roundRect(frame_x, frame_y, frame_size, frame_size, 1.7*mm, fill=1, stroke=1)

    qr_img = generate_qr_image("https://vollwerk.de", "#7C6040")
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), qr_center_x - qr_size/2, qr_y - qr_size/2,
                qr_size, qr_size, mask="auto")

    c.setFillColor(TEXT_MUTED)
    c.setFont(SANS_BOLD, 5)
    c.drawCentredString(qr_center_x, frame_y - 3*mm, "SCAN")

    c.setFillColor(BROWN)
    c.setFont(SANS_BOLD, 5.5)
    c.drawCentredString(qr_center_x, frame_y - 6*mm, "vollwerk.de")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    front_path = os.path.join(out_dir, "visitenkarte_front.pdf")
    c = canvas.Canvas(front_path, pagesize=(W, H))
    c.setTitle("Vollwerk AI — Visitenkarte Vorderseite")
    c.setAuthor("Adil El Madbouh")
    draw_front(c)
    c.showPage()
    c.save()
    print(f"  OK  Front: {front_path}")

    back_path = os.path.join(out_dir, "visitenkarte_back.pdf")
    c = canvas.Canvas(back_path, pagesize=(W, H))
    c.setTitle("Vollwerk AI — Visitenkarte Rueckseite")
    c.setAuthor("Adil El Madbouh")
    draw_back(c)
    c.showPage()
    c.save()
    print(f"  OK  Back:  {back_path}")

    print(f"\nDone — 2 PDFs at 85 x 54 mm in:\n  {out_dir}")


if __name__ == "__main__":
    main()
