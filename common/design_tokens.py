"""
common/design_tokens.py — Brand Color Tokens, Typography & Vector Rendering Primitives
"""

import os
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from common.config import settings

SIZE = 1080

# Institutional Color Tokens
C_RED_TOP   = (185, 28, 28)    # #B91C1C
C_RED_BOT   = (69, 10, 10)     # #450A0A
C_BLUE_TOP  = (15, 23, 42)     # #0F172A (Obsidian Navy)
C_BLUE_BOT  = (2, 6, 23)       # #020617
C_TEAL_TOP  = (3, 105, 161)    # #0369A1 (Ocean Blue)
C_TEAL_BOT  = (4, 47, 46)      # #042F2E
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


def get_font(font_type: str, size: int) -> ImageFont.FreeTypeFont:
    """Safely loads system fonts with fallback."""
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


def create_gradient_canvas(color_top: Tuple[int, int, int], color_bottom: Tuple[int, int, int]) -> Image.Image:
    """Creates a smooth 1080x1080 vertical gradient canvas."""
    top_img = Image.new("RGB", (SIZE, SIZE), color_top)
    bot_img = Image.new("RGB", (SIZE, SIZE), color_bottom)
    mask = Image.new("L", (SIZE, SIZE))
    for y in range(SIZE):
        mask.paste(int((y / SIZE) * 255), (0, y, SIZE, y + 1))
    return Image.composite(bot_img, top_img, mask)


def create_cinematic_photo_canvas(photo_name: str, tint_top: Tuple[int, int, int], tint_bottom: Tuple[int, int, int], tint_opacity: float = 0.82) -> Image.Image:
    """
    Creates a rich cinematic background canvas by combining a real photo (BSE, Wall St, Trading Desk, Candlesticks)
    with a dual-tone tinted gradient overlay for maximum readability and visual aesthetic.
    """
    from PIL import ImageFilter, ImageOps
    bg_path = settings.ASSETS_DIR / "backgrounds" / photo_name
    
    gradient_overlay = create_gradient_canvas(tint_top, tint_bottom).convert("RGBA")

    if bg_path.exists():
        try:
            raw_img = Image.open(bg_path).convert("RGB")
            # Center crop to 1080x1080
            photo = ImageOps.fit(raw_img, (SIZE, SIZE), Image.Resampling.LANCZOS)
            # Apply subtle atmosphere blur for readability
            photo = photo.filter(ImageFilter.GaussianBlur(radius=1.8)).convert("RGBA")
            
            # Blend gradient scrim on top of the real financial photo
            blended = Image.blend(photo, gradient_overlay, tint_opacity)
            return blended.convert("RGB")
        except Exception as e:
            print(f"⚠️ Photo background blend fallback: {e}")

    # Fallback to gradient canvas with architectural silhouettes
    im = create_gradient_canvas(tint_top, tint_bottom)
    add_architectural_silhouettes(im, (255, 255, 255), 0.15)
    return im


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
    d.text((SIZE // 2 + 15, 42), handle, fill=C_CREAM, font=get_font("din_alt", 26), anchor="mm")
