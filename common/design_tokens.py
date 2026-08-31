"""
common/design_tokens.py — Modern Photo-First Editorial Design System (Morning Brew / Bloomberg Style)
"""

import os
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from common.config import settings

SIZE = 1080
PHOTO_HEIGHT = 620  # Top ~58% for high-res real photography/charts

# Modern Editorial Palette
BG_DARK          = (11, 15, 25)       # #0B0F19 (Deep Obsidian Base)
BG_CARD          = (18, 26, 44)       # #121A2C (Subtle Card Background)
TEXT_WHITE       = (255, 255, 255)
TEXT_MUTED       = (148, 163, 184)   # #94A3B8
TEXT_DARK        = (15, 23, 42)

ACCENT_AMBER     = (245, 158, 11)    # #F59E0B
ACCENT_EMERALD   = (16, 185, 129)   # #10B981
ACCENT_ROSE      = (225, 29, 72)     # #E11D48
ACCENT_CYAN      = (6, 182, 212)     # #06B6D4

BORDER_SUBTLE    = (30, 41, 59)


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


def create_photo_editorial_canvas(photo_name: str, category_tag: str = "MARKET PULSE") -> Image.Image:
    """
    Builds a Photo-First Editorial Canvas:
      • Top 58% (0 to 620px): High-res real photo/chart with seamless gradient blend at bottom.
      • Top Left/Right: Sleek @finpulse.daily watermark & category pill.
      • Bottom 42% (620 to 1080px): Deep obsidian panel for typography & stats.
    """
    canvas = Image.new("RGB", (SIZE, SIZE), BG_DARK)
    bg_path = settings.ASSETS_DIR / "backgrounds" / photo_name

    if bg_path.exists():
        try:
            raw = Image.open(bg_path).convert("RGB")
            # Crop photo to fill top 640px
            photo = ImageOps.fit(raw, (SIZE, 640), Image.Resampling.LANCZOS).convert("RGBA")
            
            # Bottom fade mask on photo
            fade_mask = Image.new("L", (SIZE, 640), 255)
            fdraw = ImageDraw.Draw(fade_mask)
            for y in range(480, 640):
                alpha = int(255 * (1 - ((y - 480) / 160)))
                fdraw.line([(0, y), (SIZE, y)], fill=alpha)
            
            photo.putalpha(fade_mask)
            canvas.paste(photo, (0, 0), photo)
        except Exception as e:
            print(f"⚠️ Photo load error: {e}")

    # Top Navigation Glass Pill
    top_overlay = Image.new("RGBA", (SIZE, 100), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(top_overlay)
    
    tdraw.rounded_rectangle([(40, 28), (SIZE - 40, 76)], radius=24, fill=(11, 15, 25, 210), outline=(51, 65, 85, 160), width=1)
    
    # Badge Icon
    badge_path = settings.ASSETS_DIR / "finpulse_badge.png"
    if badge_path.exists():
        try:
            badge = Image.open(badge_path).convert("RGBA").resize((32, 32), Image.Resampling.LANCZOS)
            top_overlay.paste(badge, (56, 36), badge)
        except Exception:
            pass

    tdraw.text((98, 52), "@finpulse.daily", fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="lm")
    tdraw.text((SIZE - 60, 52), category_tag.upper(), fill=ACCENT_AMBER, font=get_font("impact", 20), anchor="rm")
    
    canvas.paste(Image.alpha_composite(canvas.crop((0, 0, SIZE, 100)).convert("RGBA"), top_overlay).convert("RGB"), (0, 0))
    return canvas


def draw_stat_pill(d: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], label: str, value: str, is_positive: bool = True):
    """Draws a sleek, modern stat pill with label and highlighted value."""
    color = ACCENT_EMERALD if is_positive else ACCENT_ROSE
    d.rounded_rectangle(box, radius=12, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    # Left indicator notch
    d.rounded_rectangle([(box[0], box[1]), (box[0] + 6, box[3])], radius=4, fill=color)
    d.text((box[0] + 16, (box[1] + box[3]) // 2 - 12), label.upper(), fill=TEXT_MUTED, font=get_font("din_cond", 20))
    d.text((box[0] + 16, (box[1] + box[3]) // 2 + 10), value, fill=color, font=get_font("impact", 24))
