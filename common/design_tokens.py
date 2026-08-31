"""
common/design_tokens.py — Dynamic Photographic & Glassmorphism Canvas System
"""

import os
import random
from pathlib import Path
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont, ImageOps
from common.config import settings

SIZE = 1080

# Color Tokens
BG_DARK          = (11, 15, 25)
BG_GLASS         = (15, 23, 42, 215)  # 85% opacity translucent glass
BG_GLASS_HI      = (20, 30, 55, 230)

TEXT_WHITE       = (255, 255, 255)
TEXT_MUTED       = (148, 163, 184)
TEXT_DARK        = (15, 23, 42)

ACCENT_AMBER     = (245, 158, 11)
ACCENT_EMERALD   = (16, 185, 129)
ACCENT_ROSE      = (225, 29, 72)
ACCENT_CYAN      = (6, 182, 212)

BORDER_GLASS     = (51, 65, 85, 175)
BORDER_AMBER     = (245, 158, 11, 180)


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


def get_random_background_photos(count: int = 4) -> List[Path]:
    """Returns a shuffled list of unique random financial background photos."""
    bg_dir = settings.ASSETS_DIR / "backgrounds"
    photos = list(bg_dir.glob("*.jpg")) + list(bg_dir.glob("*.png"))
    if not photos:
        return []
    random.shuffle(photos)
    # If not enough, cycle
    while len(photos) < count:
        photos.extend(photos)
    return photos[:count]


def create_full_background_canvas(photo_path: Optional[Path] = None, category_tag: str = "MARKET PULSE", tint_color: Tuple[int, int, int] = (11, 15, 25)) -> Image.Image:
    """
    Creates a full 1080x1080 photographic background canvas.
    The photo fills the entire canvas with an atmospheric dark scrim overlay.
    """
    canvas = Image.new("RGB", (SIZE, SIZE), BG_DARK)

    if photo_path and Path(photo_path).exists():
        try:
            raw = Image.open(photo_path).convert("RGB")
            photo = ImageOps.fit(raw, (SIZE, SIZE), Image.Resampling.LANCZOS).convert("RGBA")
            
            # Atmospheric dark scrim overlay
            scrim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(scrim)
            
            for y in range(SIZE):
                alpha = int(140 + (y / SIZE) * 60)
                sdraw.line([(0, y), (SIZE, y)], fill=(tint_color[0], tint_color[1], tint_color[2], alpha))
            
            canvas = Image.alpha_composite(photo, scrim).convert("RGB")
        except Exception as e:
            print(f"⚠️ Canvas photo error: {e}")

    # Top Header Pill
    top_overlay = Image.new("RGBA", (SIZE, 110), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(top_overlay)
    
    tdraw.rounded_rectangle([(40, 28), (SIZE - 40, 78)], radius=25, fill=(11, 15, 25, 220), outline=(51, 65, 85, 180), width=1)
    
    # FinPulse Logo Badge
    badge_path = settings.ASSETS_DIR / "finpulse_badge.png"
    if badge_path.exists():
        try:
            badge = Image.open(badge_path).convert("RGBA").resize((32, 32), Image.Resampling.LANCZOS)
            top_overlay.paste(badge, (56, 37), badge)
        except Exception:
            pass

    tdraw.text((98, 53), "@finpulse.daily", fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="lm")
    tdraw.text((SIZE - 60, 53), category_tag.upper(), fill=ACCENT_AMBER, font=get_font("impact", 20), anchor="rm")
    
    canvas.paste(Image.alpha_composite(canvas.crop((0, 0, SIZE, 110)).convert("RGBA"), top_overlay).convert("RGB"), (0, 0))
    return canvas


def draw_glass_panel(im: Image.Image, box: Tuple[int, int, int, int], radius: int = 20, bg: Tuple[int, int, int, int] = BG_GLASS, border: Tuple[int, int, int, int] = BORDER_GLASS, border_width: int = 1):
    """Draws a floating translucent glassmorphism container across the full-space canvas."""
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)
    im.paste(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))
