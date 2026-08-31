"""
image_service.py — High-Conviction 4-Slide Market Intelligence Visual Engine
Generates publication-ready 1080×1080 slides with financial backgrounds & Bull/Bear motifs.
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from config.settings import settings

SIZE = 1080

# Institutional Color Tokens
C_RED_TOP   = (185, 28, 28)    # #B91C1C
C_RED_BOT   = (69, 10, 10)     # #450A0A
C_BLUE_TOP  = (15, 23, 42)     # #0F172A (Obsidian Navy)
C_BLUE_BOT  = (2, 6, 23)       # #020617
C_TEAL_TOP  = (3, 105, 161)    # #0369A1 (Ocean Blue)
C_TEAL_BOT  = (4, 47, 46)      # #042F2E (Deep Teal)
C_GOLD_TOP  = (194, 65, 12)    # #C2410C (Warm Amber)
C_GOLD_BOT  = (124, 45, 18)    # #7C2D12

C_EMERALD   = (16, 185, 129)   # #10B981 (Bullish Green)
C_AMBER     = (245, 158, 11)   # #F59E0B (Electric Gold)
C_ROSE      = (225, 29, 72)    # #E11D48 (Bearish Red)
C_CREAM     = (254, 243, 220)  # #FEF3DC (Vintage Cream)
C_DARK      = (28, 25, 23)     # #1C1917
C_MAROON    = (122, 26, 14)    # #7A1A0E
C_WHITE     = (255, 255, 255)
C_DIVIDER   = (225, 210, 185)


def _get_font(font_type: str, size: int) -> ImageFont.FreeTypeFont:
    """Safely loads system fonts or fallbacks."""
    paths = {
        "impact": ["/System/Library/Fonts/Supplemental/Impact.ttf", "/System/Library/Fonts/Impact.ttf"],
        "din_cond": ["/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf", "/System/Library/Fonts/DIN Condensed Bold.ttf"],
        "din_alt": ["/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf", "/System/Library/Fonts/DIN Alternate Bold.ttf"],
        "body": ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Geneva.ttf"]
    }
    for p in paths.get(font_type, []):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_gradient_bg(color_top: Tuple[int, int, int], color_bottom: Tuple[int, int, int]) -> Image.Image:
    """Generates a smooth vertical gradient."""
    top_img = Image.new("RGB", (SIZE, SIZE), color_top)
    bot_img = Image.new("RGB", (SIZE, SIZE), color_bottom)
    mask = Image.new("L", (SIZE, SIZE))
    for y in range(SIZE):
        mask.paste(int((y / SIZE) * 255), (0, y, SIZE, y + 1))
    return Image.composite(bot_img, top_img, mask)


def add_architectural_silhouettes(im: Image.Image, accent: Tuple[int, int, int], opacity: float = 0.16):
    """Draws BSE Phiroze Towers & Wall St exchange silhouettes + candlestick watermark."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    col = (accent[0], accent[1], accent[2], int(255 * opacity))
    col_light = (255, 255, 255, int(255 * (opacity * 0.5)))

    # Candlestick Watermark
    candles = [
        (120, 650, 720, 600, 780), (220, 580, 680, 520, 740),
        (340, 480, 600, 420, 660), (460, 520, 640, 490, 680),
        (580, 400, 530, 360, 580), (700, 350, 480, 310, 520),
        (820, 280, 420, 240, 460), (940, 220, 350, 180, 400)
    ]
    for cx, tb, bb, hi, lo in candles:
        d.line([(cx, hi), (cx, lo)], fill=col_light, width=3)
        d.rounded_rectangle([(cx - 24, tb), (cx + 24, bb)], radius=6, fill=col)

    # Building Silhouettes (Phiroze Towers & Wall St)
    bldgs = [
        (40, 820, 180, 1080), (160, 740, 320, 1080),
        (300, 790, 440, 1080), (420, 680, 620, 1080),
        (600, 760, 740, 1080), (720, 710, 880, 1080), (860, 790, 1040, 1080)
    ]
    for x0, y0, x1, y1 in bldgs:
        d.rectangle([(x0, y0), (x1, y1)], fill=(0, 0, 0, int(255 * (opacity * 0.85))))
        for wx in range(x0 + 15, x1 - 15, 20):
            for wy in range(y0 + 20, y1 - 40, 28):
                d.rectangle([(wx, wy), (wx + 8, wy + 12)], fill=col_light)

    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_bull_motif(im: Image.Image, cx: int, cy: int, size: int = 80):
    """Draws an Emerald Charging Bull badge."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r = size // 2
    d.ellipse([(cx - r - 8, cy - r - 8), (cx + r + 8, cy + r + 8)], fill=(16, 185, 129, 60))
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(16, 24, 39, 230), outline=(16, 185, 129, 240), width=4)
    # Horns & Head
    d.arc([(cx - 30, cy - 25), (cx - 10, cy - 5)], start=160, end=340, fill=C_EMERALD, width=4)
    d.arc([(cx + 10, cy - 25), (cx + 30, cy - 5)], start=200, end=380, fill=C_EMERALD, width=4)
    d.polygon([(cx - 20, cy - 10), (cx + 20, cy - 10), (cx + 14, cy + 20), (cx, cy + 28), (cx - 14, cy + 20)], fill=C_EMERALD)
    d.ellipse([(cx - 10, cy), (cx - 4, cy + 5)], fill=(255, 255, 255))
    d.ellipse([(cx + 4, cy), (cx + 10, cy + 5)], fill=(255, 255, 255))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_bear_motif(im: Image.Image, cx: int, cy: int, size: int = 80):
    """Draws a Roaring Bear badge."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r = size // 2
    d.ellipse([(cx - r - 8, cy - r - 8), (cx + r + 8, cy + r + 8)], fill=(225, 29, 72, 60))
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(28, 15, 15, 230), outline=(225, 29, 72, 240), width=4)
    # Ears & Head
    d.ellipse([(cx - 25, cy - 24), (cx - 12, cy - 10)], fill=C_ROSE)
    d.ellipse([(cx + 12, cy - 24), (cx + 25, cy - 10)], fill=C_ROSE)
    d.ellipse([(cx - 22, cy - 16), (cx + 22, cy + 22)], fill=C_ROSE)
    d.ellipse([(cx - 10, cy + 2), (cx + 10, cy + 18)], fill=(255, 255, 255))
    d.polygon([(cx - 5, cy + 5), (cx + 5, cy + 5), (cx, cy + 11)], fill=(28, 15, 15))
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_header(im: Image.Image, d: ImageDraw.ImageDraw, handle: str):
    """Renders top FinPulse badge emblem and handle."""
    badge_path = settings.ASSETS_DIR / "finpulse_badge.png"
    if badge_path.exists():
        try:
            badge = Image.open(badge_path).convert("RGBA").resize((48, 48), Image.Resampling.LANCZOS)
            im.paste(badge, ((SIZE - 48) // 2 - 105, 32), badge)
        except Exception:
            pass
    d.text((SIZE // 2 + 15, 42), handle, fill=C_CREAM, font=_get_font("din_alt", 26), anchor="mm")


def generate_4slide_carousel(indices: Dict[str, Any], fii_dii: Dict[str, Any], sentiment: Dict[str, Any], news: List[Dict[str, Any]]) -> List[str]:
    """Generates the 4 1080×1080 JPEG slides."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    handle = settings.PAGE_HANDLE
    slides = []

    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]

    # Hook Determination
    pct = nifty["change_pct"]
    if pct >= 1.0: hook_main, hook_sub = "BULLS ON RAMPAGE!", f"NIFTY SURGES {abs(nifty['change']):.0f}+ PTS • SENSEX GAINS {abs(sensex['change']):.0f}+ PTS"
    elif pct > 0: hook_main, hook_sub = "MOMENTUM HOLDS FIRM!", f"NIFTY EDGES HIGHER • BULLS DEFEND SUPPORT"
    elif pct <= -1.0: hook_main, hook_sub = "MARKET UNDER PRESSURE!", f"SENSEX TUMBLES {abs(sensex['change']):.0f}+ PTS AS BEARS TAKE CONTROL"
    else: hook_main, hook_sub = "TIGHT ROPE ON D-STREET!", f"NIFTY RANGEBOUND • KEY BREAKOUT AHEAD"

    # ── SLIDE 1: INDICES ──
    img1 = create_gradient_bg(C_RED_TOP, C_RED_BOT)
    add_architectural_silhouettes(img1, (255, 200, 100), 0.18)
    d1 = ImageDraw.Draw(img1)
    draw_header(img1, d1, handle)

    d1.text((SIZE // 2, 105), hook_main, fill=C_CREAM, font=_get_font("impact", 76), anchor="mt")
    d1.text((SIZE // 2, 192), hook_sub, fill=C_AMBER, font=_get_font("din_cond", 48), anchor="mt")

    # Center Card
    d1.rounded_rectangle([(70, 265), (SIZE - 70, 830)], radius=28, fill=C_CREAM)
    # Nifty 50
    d1.text((310, 310), "NIFTY 50", fill=C_MAROON, font=_get_font("din_cond", 40), anchor="mt")
    d1.text((310, 370), nifty["formatted_price"], fill=C_DARK, font=_get_font("impact", 54), anchor="mt")
    d1.rounded_rectangle([(160, 455), (460, 500)], radius=20, fill=C_EMERALD if nifty["is_positive"] else C_ROSE)
    d1.text((310, 477), nifty["formatted_change"], fill=C_WHITE, font=_get_font("din_alt", 22), anchor="mm")
    d1.line([(SIZE // 2, 310), (SIZE // 2, 500)], fill=C_DIVIDER, width=2)

    # Sensex
    d1.text((770, 310), "BSE SENSEX", fill=C_MAROON, font=_get_font("din_cond", 40), anchor="mt")
    d1.text((770, 370), sensex["formatted_price"], fill=C_DARK, font=_get_font("impact", 54), anchor="mt")
    d1.rounded_rectangle([(620, 455), (920, 500)], radius=20, fill=C_EMERALD if sensex["is_positive"] else C_ROSE)
    d1.text((770, 477), sensex["formatted_change"], fill=C_WHITE, font=_get_font("din_alt", 22), anchor="mm")
    d1.line([(110, 535), (SIZE - 110, 535)], fill=C_DIVIDER, width=2)

    # Secondary Row
    d1.text((310, 565), "BANK NIFTY", fill=C_MAROON, font=_get_font("din_cond", 28), anchor="mt")
    d1.text((310, 605), f"{bank['formatted_price']} ({bank['change_pct']:+.2f}%)", fill=C_DARK, font=_get_font("impact", 36), anchor="mt")
    d1.line([(SIZE // 2, 560), (SIZE // 2, 655)], fill=C_DIVIDER, width=2)
    d1.text((770, 565), "INDIA VIX (VOLATILITY)", fill=C_MAROON, font=_get_font("din_cond", 28), anchor="mt")
    d1.text((770, 605), f"{vix['price']:.2f} ({vix['change_pct']:+.2f}%)", fill=C_EMERALD if vix['change'] <= 0 else C_ROSE, font=_get_font("impact", 36), anchor="mt")

    # Bottom Banner
    d1.rounded_rectangle([(100, 690), (SIZE - 100, 785)], radius=18, fill=C_AMBER)
    d1.text((SIZE // 2, 737), f"D-STREET ACTION • {hook_main}", fill=C_DARK, font=_get_font("impact", 34), anchor="mm")

    if nifty["is_positive"]: draw_bull_motif(img1, 140, 930, 80)
    else: draw_bear_motif(img1, 140, 930, 80)

    p1 = str(settings.OUTPUT_DIR / f"market_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ── SLIDE 2: CASH INFLOWS ──
    img2 = create_gradient_bg(C_BLUE_TOP, C_BLUE_BOT)
    add_architectural_silhouettes(img2, (56, 189, 248), 0.15)
    d2 = ImageDraw.Draw(img2)
    draw_header(img2, d2, handle)

    d2.text((SIZE // 2, 105), "NIFTY CASH INFLOWS:", fill=C_CREAM, font=_get_font("impact", 72), anchor="mt")
    d2.text((SIZE // 2, 190), "FII, DII & INSTITUTIONAL PARTICIPATION", fill=C_AMBER, font=_get_font("din_cond", 52), anchor="mt")
    
    # Date Ribbon
    d2.rounded_rectangle([(180, 255), (SIZE - 180, 315)], radius=14, fill=C_AMBER)
    d2.text((SIZE // 2, 285), f"NSE CASH SEGMENT ACTIVITY ({fii_dii['date']})", fill=C_DARK, font=_get_font("impact", 30), anchor="mm")

    # FII Card
    d2.rounded_rectangle([(70, 345), (515, 565)], radius=20, fill=C_CREAM)
    d2.text((292, 370), "FII / FPI INFLOW", fill=C_MAROON, font=_get_font("din_cond", 38), anchor="mt")
    d2.text((292, 425), fii_dii['fii']['formatted_net'], fill=C_EMERALD if fii_dii['fii']['net'] > 0 else C_ROSE, font=_get_font("impact", 48), anchor="mt")
    d2.text((292, 500), f"Stance: {fii_dii['fii']['bias']}", fill=C_DARK, font=_get_font("din_alt", 24), anchor="mt")

    # DII Card
    d2.rounded_rectangle([(565, 345), (SIZE - 70, 565)], radius=20, fill=C_CREAM)
    d2.text((787, 370), "DII (DOMESTIC) INFLOW", fill=C_MAROON, font=_get_font("din_cond", 38), anchor="mt")
    d2.text((787, 425), fii_dii['dii']['formatted_net'], fill=C_EMERALD if fii_dii['dii']['net'] > 0 else C_ROSE, font=_get_font("impact", 48), anchor="mt")
    d2.text((787, 500), f"Stance: {fii_dii['dii']['bias']}", fill=C_DARK, font=_get_font("din_alt", 24), anchor="mt")

    # Total Net
    d2.rounded_rectangle([(70, 595), (SIZE - 70, 745)], radius=20, fill=C_WHITE)
    d2.text((SIZE // 2, 615), "TOTAL COMBINED INSTITUTIONAL NET", fill=C_MAROON, font=_get_font("din_cond", 36), anchor="mt")
    d2.text((SIZE // 2, 660), fii_dii['formatted_total_net'], fill=C_EMERALD if fii_dii['total_net'] > 0 else C_ROSE, font=_get_font("impact", 56), anchor="mt")

    # Retail Summary
    d2.rounded_rectangle([(70, 775), (SIZE - 70, 895)], radius=18, fill=C_AMBER)
    d2.text((SIZE // 2, 802), "RETAIL & CLIENT FLOWS: HEALTHY ABSORPTION", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 850), "Steady retail participation & long derivative roll-overs into next series", fill=C_DARK, font=_get_font("din_alt", 22), anchor="mt")

    if fii_dii['total_net'] > 0: draw_bull_motif(img2, SIZE - 120, 670, 75)
    else: draw_bear_motif(img2, SIZE - 120, 670, 75)

    p2 = str(settings.OUTPUT_DIR / f"market_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ── SLIDE 3: SENTIMENTS ──
    img3 = create_gradient_bg(C_TEAL_TOP, C_TEAL_BOT)
    add_architectural_silhouettes(img3, (34, 211, 238), 0.16)
    d3 = ImageDraw.Draw(img3)
    draw_header(img3, d3, handle)

    d3.text((SIZE // 2, 105), "MARKET SENTIMENTS:", fill=C_CREAM, font=_get_font("impact", 72), anchor="mt")
    d3.text((SIZE // 2, 190), "FEAR, GREED & SECTOR RADAR", fill=C_AMBER, font=_get_font("din_cond", 52), anchor="mt")

    d3.rounded_rectangle([(70, 265), (SIZE - 70, 385)], radius=20, fill=C_CREAM)
    d3.text((SIZE // 2, 285), f"OVERALL MARKET SENTIMENT: {sentiment.get('market_mood', 'BULLISH').upper()}", fill=C_MAROON, font=_get_font("impact", 36), anchor="mt")
    d3.text((SIZE // 2, 338), f"India VIX: {vix['price']:.2f} • {sentiment.get('vix_interpretation', 'Calm volatility')}", fill=C_DARK, font=_get_font("body", 22), anchor="mt")

    sy = 415
    for s in sentiment.get("sectors", [])[:3]:
        imp = s.get("impact", "BULLISH")
        d3.rounded_rectangle([(70, sy), (SIZE - 70, sy + 148)], radius=20, fill=C_CREAM)
        d3.text((105, sy + 18), s["sector_name"].upper(), fill=C_MAROON, font=_get_font("din_cond", 36))
        d3.rounded_rectangle([(SIZE - 230, sy + 16), (SIZE - 100, sy + 54)], radius=12, fill=C_ROSE if imp == "BEARISH" else C_EMERALD)
        d3.text((SIZE - 165, sy + 35), imp, fill=C_WHITE, font=_get_font("din_alt", 22), anchor="mm")
        d3.text((105, sy + 62), f"Tickers: {'   •   '.join(s.get('affected_stocks', [])[:4])}", fill=C_DARK, font=_get_font("impact", 30))
        d3.text((105, sy + 104), f"Catalyst: {s['catalyst'][:75]}", fill=C_MAROON, font=_get_font("body", 21))
        sy += 168

    # Swipe Pill
    d3.rounded_rectangle([(SIZE // 2 - 95, 935 - 24), (SIZE // 2 + 95, 935 + 24)], radius=24, fill=C_CREAM)
    d3.text((SIZE // 2 - 10, 935), "SWIPE", fill=C_DARK, font=_get_font("din_alt", 26), anchor="mm")
    d3.polygon([(SIZE // 2 + 44, 927), (SIZE // 2 + 56, 935), (SIZE // 2 + 44, 943)], fill=C_DARK)

    p3 = str(settings.OUTPUT_DIR / f"market_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ── SLIDE 4: MAJOR NEWS ──
    img4 = create_gradient_bg(C_GOLD_TOP, C_GOLD_BOT)
    add_architectural_silhouettes(img4, (254, 240, 138), 0.18)
    d4 = ImageDraw.Draw(img4)
    draw_header(img4, d4, handle)

    d4.rounded_rectangle([(70, 115), (SIZE - 70, 895)], radius=28, fill=C_CREAM)
    d4.text((SIZE // 2, 145), "MAJOR MARKET NEWS:", fill=C_MAROON, font=_get_font("impact", 54), anchor="mt")
    d4.text((SIZE // 2, 215), "TOP BREAKING STORIES & CATALYSTS", fill=C_DARK, font=_get_font("din_cond", 40), anchor="mt")

    ny = 285
    for idx, art in enumerate(news[:3], 1):
        d4.rounded_rectangle([(100, ny), (SIZE - 100, ny + 155)], radius=18, fill=C_WHITE)
        title = art.get('title', '')[:62] + "..." if len(art.get('title', '')) > 65 else art.get('title', '')
        d4.text((125, ny + 16), f"{idx}. {title}", fill=C_DARK, font=_get_font("din_cond", 32))
        d4.text((125, ny + 58), "Key macroeconomic development impacting broader equities.", fill=C_MAROON, font=_get_font("body", 20))
        d4.text((125, ny + 112), f"SOURCE: {art.get('source_name', 'News Desk').upper()}", fill=C_DARK, font=_get_font("din_alt", 20))
        ny += 175

    d4.rounded_rectangle([(100, 815), (SIZE - 100, 870)], radius=14, fill=C_AMBER)
    d4.text((SIZE // 2, 842), "FOLLOW @FINPULSE.DAILY • READ FULL LINKS IN CAPTION", fill=C_DARK, font=_get_font("impact", 28), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / f"market_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
