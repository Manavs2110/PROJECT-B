"""
services/visual_rendering_service/renderer_engagement.py — Native Programmatic 5th Engagement Slide Generator
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw
from common.config import settings
from common.design_tokens import (
    SIZE, BG_GLASS, BG_GLASS_HI, TEXT_WHITE, TEXT_MUTED, TEXT_DARK,
    ACCENT_AMBER, ACCENT_EMERALD, ACCENT_ROSE, ACCENT_CYAN,
    BORDER_GLASS, BORDER_AMBER,
    get_font, create_full_background_canvas, draw_glass_panel
)

def render_engagement_slide(photo_path: Optional[Path] = None, output_filename: str = "market_slide_5.jpg") -> str:
    """Renders a pixel-perfect, native 5th Engagement & Discussion CTA slide with transparent logo and perfect alignment."""
    img = create_full_background_canvas(photo_path, "COMMUNITY")
    d = ImageDraw.Draw(img)

    # 1. Floating Center Chat Bubble Emblem
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    cx, cy = SIZE // 2, 190
    r = 50
    # Gradient/glow circle
    odraw.ellipse([(cx - r - 6, cy - r - 6), (cx + r + 6, cy + r + 6)], fill=(16, 185, 129, 60))
    odraw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(6, 182, 212, 230), outline=(16, 185, 129, 255), width=3)
    
    # Message bubble icon
    odraw.rounded_rectangle([(cx - 24, cy - 16), (cx + 24, cy + 14)], radius=8, fill=TEXT_WHITE)
    odraw.polygon([(cx - 10, cy + 14), (cx - 20, cy + 24), (cx - 2, cy + 14)], fill=TEXT_WHITE)
    # Chat dots
    for dot_x in [cx - 12, cx, cx + 12]:
        odraw.ellipse([(dot_x - 3, cy - 3), (dot_x + 3, cy + 3)], fill=(15, 23, 42, 255))
        
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    d = ImageDraw.Draw(img)

    # 2. Main Hero Typography
    d.text((SIZE // 2, 260), "SHARE YOUR", fill=TEXT_WHITE, font=get_font("impact", 72), anchor="mt")
    d.text((SIZE // 2, 335), "VIEWS", fill=ACCENT_EMERALD, font=get_font("impact", 76), anchor="mt")

    # 3. Glowing Divider with Center Emerald Bead
    d.line([(SIZE // 2 - 140, 435), (SIZE // 2 + 140, 435)], fill=(51, 65, 85), width=2)
    d.ellipse([(SIZE // 2 - 5, 435 - 5), (SIZE // 2 + 5, 435 + 5)], fill=ACCENT_EMERALD)

    # 4. Subtitle Paragraph
    d.text((SIZE // 2, 465), "I check all the comments and would love to discuss", fill=TEXT_WHITE, font=get_font("body", 24), anchor="mt")
    d.text((SIZE // 2, 500), "your thoughts on today's market moves.", fill=TEXT_MUTED, font=get_font("body", 22), anchor="mt")

    # 5. Three Floating Discussion Cards (Side-by-Side)
    cards = [
        {"title": "Bullish or Bearish?", "sub": "Vote your stance", "color": ACCENT_EMERALD, "icon_type": "chart"},
        {"title": "Your top pick today?", "sub": "Share your best setup", "color": ACCENT_AMBER, "icon_type": "trophy"},
        {"title": "What's your strategy?", "sub": "Intraday or Positional?", "color": ACCENT_CYAN, "icon_type": "brain"}
    ]

    card_w = 300
    gap = 30
    start_x = 55
    card_y1, card_y2 = 560, 780

    for i, c in enumerate(cards):
        x1 = start_x + i * (card_w + gap)
        x2 = x1 + card_w
        
        # Glass card
        draw_glass_panel(img, (x1, card_y1, x2, card_y2), radius=22, bg=(15, 23, 42, 230), border=BORDER_GLASS)
        
        # Icon Pill at top of card
        d.rounded_rectangle([(x1 + card_w // 2 - 28, card_y1 + 25), (x1 + card_w // 2 + 28, card_y1 + 75)], radius=14, fill=(20, 30, 55))
        
        # Vector icons
        icx, icy = x1 + card_w // 2, card_y1 + 50
        if c["icon_type"] == "chart":
            d.polygon([(icx - 14, icy + 8), (icx - 4, icy - 4), (icx + 4, icy + 2), (icx + 14, icy - 10)], outline=ACCENT_EMERALD, width=3)
            d.polygon([(icx + 8, icy - 10), (icx + 14, icy - 10), (icx + 14, icy - 4)], fill=ACCENT_EMERALD)
        elif c["icon_type"] == "trophy":
            d.rounded_rectangle([(icx - 12, icy - 12), (icx + 12, icy + 2)], radius=4, outline=ACCENT_AMBER, width=3)
            d.line([(icx, icy + 2), (icx, icy + 10)], fill=ACCENT_AMBER, width=3)
            d.line([(icx - 10, icy + 10), (icx + 10, icy + 10)], fill=ACCENT_AMBER, width=3)
        elif c["icon_type"] == "brain":
            d.ellipse([(icx - 12, icy - 10), (icx + 12, icy + 10)], outline=ACCENT_CYAN, width=3)
            d.line([(icx, icy - 6), (icx, icy + 6)], fill=ACCENT_CYAN, width=2)

        # Card Title
        d.text((x1 + card_w // 2, card_y1 + 105), c["title"], fill=TEXT_WHITE, font=get_font("din_cond", 30), anchor="mt")
        d.text((x1 + card_w // 2, card_y1 + 150), c["sub"], fill=c["color"], font=get_font("body", 18), anchor="mt")

    # 6. Bottom Action / Social Bar
    draw_glass_panel(img, (50, 825, SIZE - 50, 930), radius=20, bg=(10, 15, 28, 235), border=BORDER_GLASS)
    
    # Left Callout
    d.text((80, 855), "DROP A COMMENT BELOW", fill=TEXT_MUTED, font=get_font("din_cond", 24))
    d.text((80, 888), "@finpulse.daily", fill=ACCENT_EMERALD, font=get_font("impact", 26))

    # Right Action Badges (Like, Save, Share)
    btn_w = 90
    actions = [("LIKE", ACCENT_ROSE), ("SAVE", ACCENT_AMBER), ("SHARE", ACCENT_CYAN)]
    for idx, (act, col) in enumerate(actions):
        bx2 = (SIZE - 80) - (2 - idx) * (btn_w + 14)
        bx1 = bx2 - btn_w
        d.rounded_rectangle([(bx1, 850), (bx2, 905)], radius=14, fill=(20, 30, 55), outline=(51, 65, 85), width=1)
        d.text(((bx1 + bx2) // 2, 877), act, fill=col, font=get_font("impact", 20), anchor="mm")

    # Footer Watermark
    d.text((SIZE // 2, 975), "JOIN THE CONVERSATION • ALL MARKET OPINIONS WELCOME", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    # Save
    out_path = str(settings.OUTPUT_DIR / output_filename)
    img.save(out_path, "JPEG", quality=96)
    return out_path
