"""
common/design_tokens.py — Elite Institutional Visual Design System & Glassmorphic Canvas
"""

import os
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from common.config import settings

SIZE = 1080

# Modern Institutional Color Palette
COLOR_BG_DARK    = (11, 15, 25)       # #0B0F19 (Deep Slate Canvas)
COLOR_WHITE      = (255, 255, 255)
COLOR_OFFWHITE   = (241, 245, 249)   # #F1F5F9 (Text Primary)
COLOR_MUTED      = (148, 163, 184)   # #94A3B8 (Text Secondary)
COLOR_DARK_TEXT  = (15, 23, 42)

# Vibrant Accent Colors
COLOR_AMBER      = (245, 158, 11)    # #F59E0B (Electric Gold)
COLOR_AMBER_BG   = (245, 158, 11, 40)
COLOR_EMERALD    = (16, 185, 129)   # #10B981 (Neon Green)
COLOR_EMERALD_BG = (16, 185, 129, 45)
COLOR_ROSE       = (225, 29, 72)     # #E11D48 (Crimson Red)
COLOR_ROSE_BG    = (225, 29, 72, 45)
COLOR_CYAN       = (6, 182, 212)     # #06B6D4 (Cyan Blue)

# Glassmorphism Card Colors (RGBA)
GLASS_BG_DARK    = (15, 23, 42, 215)   # #0F172A with 84% opacity
GLASS_BG_LIGHT   = (255, 255, 255, 240) # Bright contrast card
GLASS_BORDER     = (51, 65, 85, 180)  # #334155
GLASS_BORDER_HI  = (245, 158, 11, 180)


def get_font(font_type: str, size: int) -> ImageFont.FreeTypeFont:
    """Safely loads premium system fonts with clean fallbacks."""
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


def create_cinematic_photo_canvas(photo_name: str, vignette_color: Tuple[int, int, int] = (11, 15, 25), darken_factor: float = 0.55) -> Image.Image:
    """
    Creates a full-bleed cinematic photographic canvas where the real financial photo
    (BSE Dalal St, Wall St, Trading Desk, Candlesticks) is prominently visible,
    with a dark gradient vignette for superior readability.
    """
    bg_path = settings.ASSETS_DIR / "backgrounds" / photo_name
    
    if bg_path.exists():
        try:
            raw_img = Image.open(bg_path).convert("RGB")
            photo = ImageOps.fit(raw_img, (SIZE, SIZE), Image.Resampling.LANCZOS)
            
            # Create Dark Gradient Vignette Overlay
            overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            
            # Top-to-bottom dark gradient + edge vignette
            for y in range(SIZE):
                # Top header darken
                if y < 220:
                    alpha = int(210 - (y / 220) * 80)
                # Bottom cards darken
                else:
                    alpha = int(140 + ((y - 220) / (SIZE - 220)) * 95)
                odraw.line([(0, y), (SIZE, y)], fill=(vignette_color[0], vignette_color[1], vignette_color[2], min(245, alpha)))

            # Composite photo with vignette
            result = Image.alpha_composite(photo.convert("RGBA"), overlay)
            return result.convert("RGB")
        except Exception as e:
            print(f"⚠️ Photo canvas error: {e}")

    # Fallback to dark canvas
    return Image.new("RGB", (SIZE, SIZE), COLOR_BG_DARK)


def draw_glass_card(im: Image.Image, box: Tuple[int, int, int, int], radius: int = 24, bg_color: Tuple[int, int, int, int] = GLASS_BG_DARK, border_color: Tuple[int, int, int, int] = GLASS_BORDER, border_width: int = 2):
    """Draws a sleek translucent glassmorphism card with rounded corners and high-contrast border."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(box, radius=radius, fill=bg_color, outline=border_color, width=border_width)
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_header_bar(im: Image.Image, handle: str = "@finpulse.daily", category_badge: str = "MARKET INTELLIGENCE"):
    """Renders top institutional header with FinPulse emblem badge and category pill."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    # Top Glass Pill
    d.rounded_rectangle([(SIZE // 2 - 240, 32), (SIZE // 2 + 240, 78)], radius=23, fill=(15, 23, 42, 220), outline=(245, 158, 11, 140), width=1)
    
    # Badge
    badge_path = settings.ASSETS_DIR / "finpulse_badge.png"
    if badge_path.exists():
        try:
            badge = Image.open(badge_path).convert("RGBA").resize((32, 32), Image.Resampling.LANCZOS)
            overlay.paste(badge, (SIZE // 2 - 220, 39), badge)
        except Exception:
            pass
            
    d.text((SIZE // 2 - 170, 55), handle, fill=COLOR_OFFWHITE, font=get_font("din_alt", 22), anchor="lm")
    d.text((SIZE // 2 + 220, 55), category_badge, fill=COLOR_AMBER, font=get_font("impact", 20), anchor="rm")
    
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_bull_badge(im: Image.Image, cx: int, cy: int, size: int = 70):
    """Draws a glowing neon emerald bull badge."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r = size // 2
    d.ellipse([(cx - r - 6, cy - r - 6), (cx + r + 6, cy + r + 6)], fill=(16, 185, 129, 60))
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(11, 15, 25, 240), outline=COLOR_EMERALD, width=3)
    d.polygon([(cx - 16, cy - 8), (cx + 16, cy - 8), (cx + 10, cy + 16), (cx, cy + 22), (cx - 10, cy + 16)], fill=COLOR_EMERALD)
    d.arc([(cx - 24, cy - 20), (cx - 8, cy - 4)], start=160, end=340, fill=COLOR_EMERALD, width=3)
    d.arc([(cx + 8, cy - 20), (cx + 24, cy - 4)], start=200, end=380, fill=COLOR_EMERALD, width=3)
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))


def draw_bear_badge(im: Image.Image, cx: int, cy: int, size: int = 70):
    """Draws a glowing crimson roaring bear badge."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r = size // 2
    d.ellipse([(cx - r - 6, cy - r - 6), (cx + r + 6, cy + r + 6)], fill=(225, 29, 72, 60))
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(11, 15, 25, 240), outline=COLOR_ROSE, width=3)
    d.ellipse([(cx - 20, cy - 18), (cx - 10, cy - 8)], fill=COLOR_ROSE)
    d.ellipse([(cx + 10, cy - 18), (cx + 20, cy - 8)], fill=COLOR_ROSE)
    d.ellipse([(cx - 18, cy - 12), (cx + 18, cy + 18)], fill=COLOR_ROSE)
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))
