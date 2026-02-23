from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# Base directory — fonts/ lives next to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")


def get_font(style, size):
    """Load font from bundled fonts/ directory, fall back to PIL default."""
    font_files = {
        "bold":         "DejaVuSans-Bold.ttf",
        "regular":      "DejaVuSans.ttf",
        "caladea_bold": "DejaVuSerif-Bold.ttf",
    }
    filename = font_files.get(style, "DejaVuSans.ttf")
    path = os.path.join(FONTS_DIR, filename)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        # Hard fallback — PIL's built-in bitmap font (no size support)
        return ImageFont.load_default()


TOWN_CONFIG = {
    "cashiers":  {"town_color": (120, 40,  35),  "town_color_light": (160, 70,  60),  "accent_color": (27, 120, 60),  "accent_light": (72, 180, 100)},
    "highlands": {"town_color": (70,  100, 150),  "town_color_light": (110, 140, 185), "accent_color": (27, 120, 60),  "accent_light": (72, 180, 100)},
    "sylva":     {"town_color": (35,  100, 50),   "town_color_light": (65,  150, 80),  "accent_color": (27, 120, 60),  "accent_light": (72, 180, 100)},
    "franklin":  {"town_color": (180, 80,  25),   "town_color_light": (215, 120, 60),  "accent_color": (35, 100, 50),  "accent_light": (65, 150, 80)},
}


def make_image(town, title, date):
    cfg = TOWN_CONFIG.get(town.lower(), TOWN_CONFIG["cashiers"])

    w, h = 2000, 1429
    canvas = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    font_bold    = get_font("bold",         130)
    font_regular = get_font("regular",       85)
    font_label   = get_font("bold",          58)
    font_url     = get_font("regular",       52)
    rt_font      = get_font("caladea_bold", 115)
    nc_font      = get_font("caladea_bold",  62)

    ac = cfg["accent_color"]
    al = cfg["accent_light"]
    tc = cfg["town_color"]
    tl = cfg["town_color_light"]

    # ── Header label ──────────────────────────────────────────────────────────
    label = "WNC MARKET REPORT"
    lb = draw.textbbox((0, 0), label, font=font_label)
    draw.text(((w - (lb[2] - lb[0])) // 2, 75), label, fill=al, font=font_label)
    draw.rectangle([(w // 2 - 220, 162), (w // 2 + 220, 170)], fill=al)

    # ── Title lines ───────────────────────────────────────────────────────────
    lines = [title, "Market Update", date]
    y = 210
    for i, line in enumerate(lines):
        f = font_bold if i != 1 else font_regular
        bbox = draw.textbbox((0, 0), line, font=f)
        lw2 = bbox[2] - bbox[0]
        color = ac if i % 2 == 0 else al
        extra = 30 if i == 1 else 0
        draw.text(((w - lw2) // 2, y + extra), line, fill=color, font=f)
        y += bbox[3] - bbox[1] + 25 + (30 if i == 1 else 0)

    # ── Large town name with engraved effect ──────────────────────────────────
    tu = town.upper()
    rb = draw.textbbox((0, 0), tu, font=rt_font)
    rx = (w - (rb[2] - rb[0])) // 2
    ry = 1000
    draw.text((rx + 3, ry + 3), tu, fill=tuple(max(0, c - 50) for c in tc), font=rt_font)
    draw.text((rx - 1, ry - 1), tu, fill=tl, font=rt_font)
    draw.text((rx,     ry),     tu, fill=tc,  font=rt_font)

    # ── "· N C ·" below town name ─────────────────────────────────────────────
    nc = "· N C ·"
    nb = draw.textbbox((0, 0), nc, font=nc_font)
    nx = (w - (nb[2] - nb[0])) // 2
    ny = ry + 125
    draw.text((nx + 2, ny + 2), nc, fill=tuple(max(0, c - 50) for c in tc), font=nc_font)
    draw.text((nx - 1, ny - 1), nc, fill=tl, font=nc_font)
    draw.text((nx,     ny),     nc, fill=tc,  font=nc_font)

    # ── Bottom URL bar ────────────────────────────────────────────────────────
    draw.rectangle([(80, h - 115), (w - 80, h - 105)], fill=ac)
    url = "wncmarketreport.com"
    ub = draw.textbbox((0, 0), url, font=font_url)
    draw.text(((w - (ub[2] - ub[0])) // 2, h - 88), url, fill=ac, font=font_url)

    buf = io.BytesIO()
    canvas.save(buf, format='PNG')
    buf.seek(0)
    return buf


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    data = request.get_json() if request.method == 'POST' else request.args
    town  = data.get('town',  'cashiers')
    title = data.get('title', 'Real Estate Market Update')
    date  = data.get('date',  '2026')
    return send_file(
        make_image(town, title, date),
        mimetype='image/png',
        download_name=f'{town.lower()}-featured.png'
    )


@app.route('/health')
def health():
    return {'status': 'ok'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
