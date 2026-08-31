"""
services/visual_rendering_service/renderer_market_impact.py — Full-Canvas Randomized Photographic Carousel (Post #1)
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from PIL import Image, ImageDraw
from common.config import settings
from common.design_tokens import (
    SIZE, BG_GLASS, BG_GLASS_HI, TEXT_WHITE, TEXT_MUTED, TEXT_DARK,
    ACCENT_AMBER, ACCENT_EMERALD, ACCENT_ROSE, ACCENT_CYAN,
    BORDER_GLASS, BORDER_AMBER,
    get_font, get_random_background_photos, create_full_background_canvas, draw_glass_panel
)

def render_market_impact_carousel(indices: Dict[str, Any], fii_dii: Dict[str, Any], sentiment: Dict[str, Any], news: List[Dict[str, Any]]) -> List[str]:
    """Generates 4 full-canvas photographic slides with randomized backgrounds and clean overwrite."""
    slides = []
    
    # 4 distinct random background photos
    photos = get_random_background_photos(4)

    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]

    pct = nifty["change_pct"]
    is_positive = nifty["is_positive"]
    if pct >= 1.0: hook_main, hook_sub = "BULLS ON RAMPAGE!", f"NIFTY SURGES {abs(nifty['change']):.0f}+ PTS • D-STREET RALLIES"
    elif pct > 0: hook_main, hook_sub = "MOMENTUM HOLDS FIRM!", f"NIFTY DEFENDS SUPPORT • BULLS IN CONTROL"
    elif pct <= -1.0: hook_main, hook_sub = "MARKET UNDER PRESSURE!", f"SENSEX TUMBLES {abs(sensex['change']):.0f}+ PTS AS BEARS TAKE CONTROL"
    else: hook_main, hook_sub = "TIGHT ROPE ON D-STREET!", f"NIFTY RANGEBOUND • KEY BREAKOUT AHEAD"

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: INDICES SCORECARD (Random Background #1)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_full_background_canvas(photos[0] if len(photos) > 0 else None, "MARKET PULSE")
    d1 = ImageDraw.Draw(img1)

    d1.text((SIZE // 2, 115), hook_main, fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d1.text((SIZE // 2, 195), hook_sub, fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    # NIFTY 50 Card
    draw_glass_panel(img1, (50, 255, 520, 615), radius=24, bg=(15, 23, 42, 220), border=BORDER_GLASS)
    d1.text((285, 285), "NIFTY 50", fill=TEXT_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d1.text((285, 340), nifty["formatted_price"], fill=TEXT_WHITE, font=get_font("impact", 56), anchor="mt")
    
    n_col = ACCENT_EMERALD if nifty["is_positive"] else ACCENT_ROSE
    d1.rounded_rectangle([(145, 435), (425, 485)], radius=18, fill=n_col)
    d1.text((285, 460), nifty["formatted_change"], fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.text((285, 535), f"Bias: {nifty['bias']}", fill=n_col, font=get_font("impact", 28), anchor="mt")

    # BSE SENSEX Card
    draw_glass_panel(img1, (560, 255, SIZE - 50, 615), radius=24, bg=(15, 23, 42, 220), border=BORDER_GLASS)
    d1.text((795, 285), "BSE SENSEX", fill=TEXT_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d1.text((795, 340), sensex["formatted_price"], fill=TEXT_WHITE, font=get_font("impact", 56), anchor="mt")
    
    s_col = ACCENT_EMERALD if sensex["is_positive"] else ACCENT_ROSE
    d1.rounded_rectangle([(655, 435), (935, 485)], radius=18, fill=s_col)
    d1.text((795, 460), sensex["formatted_change"], fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.text((795, 535), f"Bias: {sensex['bias']}", fill=s_col, font=get_font("impact", 28), anchor="mt")

    # Lower Indices Row
    draw_glass_panel(img1, (50, 645, SIZE - 50, 795), radius=20, bg=(10, 15, 28, 230), border=BORDER_GLASS)
    d1.text((285, 675), "BANK NIFTY", fill=TEXT_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((285, 720), f"{bank['formatted_price']} ({bank['change_pct']:+.2f}%)", fill=TEXT_WHITE, font=get_font("impact", 38), anchor="mt")
    
    d1.line([(SIZE // 2, 665), (SIZE // 2, 775)], fill=(51, 65, 85), width=2)
    
    d1.text((795, 675), "INDIA VIX (VOLATILITY)", fill=TEXT_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((795, 720), f"{vix['price']:.2f} ({vix['change_pct']:+.2f}%)", fill=ACCENT_EMERALD if vix['change'] <= 0 else ACCENT_ROSE, font=get_font("impact", 38), anchor="mt")

    # Bottom Full-Width Takeaway Banner
    draw_glass_panel(img1, (50, 825, SIZE - 50, 915), radius=18, bg=(245, 158, 11, 235), border=BORDER_AMBER)
    d1.text((SIZE // 2, 870), f"D-STREET ACTION • SWIPE FOR FII/DII INSTITUTIONAL FLOWS", fill=TEXT_DARK, font=get_font("impact", 28), anchor="mm")

    d1.text((SIZE // 2, 975), "FINPULSE DAILY INTELLIGENCE • FOLLOW @FINPULSE.DAILY", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p1 = str(settings.OUTPUT_DIR / "market_slide_1.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: INSTITUTIONAL CASH INFLOWS (Random Background #2)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_full_background_canvas(photos[1] if len(photos) > 1 else None, "INSTITUTIONAL FLOWS")
    d2 = ImageDraw.Draw(img2)

    d2.text((SIZE // 2, 115), "NIFTY CASH INFLOWS:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d2.text((SIZE // 2, 195), f"FII / FPI & DII NET POSITIONING ({fii_dii['date']})", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    # FII & DII Cards
    fii_col = ACCENT_EMERALD if fii_dii['fii']['net'] > 0 else ACCENT_ROSE
    draw_glass_panel(img2, (50, 255, 520, 575), radius=24, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d2.text((285, 285), "FOREIGN INSTITUTIONAL (FII)", fill=TEXT_MUTED, font=get_font("din_cond", 34), anchor="mt")
    d2.text((285, 345), fii_dii['fii']['formatted_net'], fill=fii_col, font=get_font("impact", 52), anchor="mt")
    d2.rounded_rectangle([(175, 440), (395, 490)], radius=16, fill=fii_col)
    d2.text((285, 465), fii_dii['fii']['bias'], fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")

    dii_col = ACCENT_EMERALD if fii_dii['dii']['net'] > 0 else ACCENT_ROSE
    draw_glass_panel(img2, (560, 255, SIZE - 50, 575), radius=24, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d2.text((795, 285), "DOMESTIC INSTITUTIONAL (DII)", fill=TEXT_MUTED, font=get_font("din_cond", 34), anchor="mt")
    d2.text((795, 345), fii_dii['dii']['formatted_net'], fill=dii_col, font=get_font("impact", 52), anchor="mt")
    d2.rounded_rectangle([(685, 440), (905, 490)], radius=16, fill=dii_col)
    d2.text((795, 465), fii_dii['dii']['bias'], fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")

    # Combined Net Total Card
    tot_col = ACCENT_EMERALD if fii_dii['total_net'] > 0 else ACCENT_ROSE
    draw_glass_panel(img2, (50, 605, SIZE - 50, 765), radius=22, bg=(10, 15, 28, 235), border=BORDER_AMBER)
    d2.text((SIZE // 2, 630), "COMBINED NET INSTITUTIONAL CASH BALANCE", fill=ACCENT_AMBER, font=get_font("din_cond", 34), anchor="mt")
    d2.text((SIZE // 2, 680), fii_dii['formatted_total_net'], fill=tot_col, font=get_font("impact", 56), anchor="mt")

    # Retail Note Card
    draw_glass_panel(img2, (50, 795, SIZE - 50, 915), radius=18, bg=(15, 23, 42, 215), border=BORDER_GLASS)
    d2.text((SIZE // 2, 818), "RETAIL & CLIENT FLOWS: HEALTHY ABSORPTION", fill=TEXT_WHITE, font=get_font("impact", 30), anchor="mt")
    d2.text((SIZE // 2, 862), "Strong domestic SIP inflows & retail liquidity absorbing institutional selling", fill=TEXT_MUTED, font=get_font("body", 22), anchor="mt")

    d2.text((SIZE // 2, 975), "SWIPE FOR SECTOR IMPACT MATRIX & SENTIMENT RADAR", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p2 = str(settings.OUTPUT_DIR / "market_slide_2.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: SECTOR RADAR (Random Background #3)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_full_background_canvas(photos[2] if len(photos) > 2 else None, "SECTOR RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((SIZE // 2, 115), "MARKET SENTIMENTS:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d3.text((SIZE // 2, 195), "FEAR, GREED & SECTOR IMPACT MATRIX", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    draw_glass_panel(img3, (50, 255, SIZE - 50, 385), radius=20, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d3.text((SIZE // 2, 275), f"OVERALL MARKET SENTIMENT: {sentiment.get('market_mood', 'BULLISH').upper()}", fill=ACCENT_AMBER, font=get_font("impact", 36), anchor="mt")
    d3.text((SIZE // 2, 330), f"India VIX at {vix['price']:.2f} • {sentiment.get('vix_interpretation', 'Calm volatility environment')}", fill=TEXT_WHITE, font=get_font("body", 22), anchor="mt")

    sy = 415
    for s in sentiment.get("sectors", [])[:3]:
        imp = s.get("impact", "BULLISH")
        imp_col = ACCENT_ROSE if imp == "BEARISH" else ACCENT_EMERALD
        draw_glass_panel(img3, (50, sy, SIZE - 50, sy + 145), radius=18, bg=(15, 23, 42, 225), border=BORDER_GLASS)
        
        d3.text((80, sy + 18), s["sector_name"].upper(), fill=TEXT_WHITE, font=get_font("din_cond", 36))
        
        d3.rounded_rectangle([(SIZE - 220, sy + 16), (SIZE - 80, sy + 54)], radius=12, fill=imp_col)
        d3.text((SIZE - 150, sy + 35), imp, fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")
        
        d3.text((80, sy + 62), f"Tickers: {'   •   '.join(s.get('affected_stocks', [])[:4])}", fill=ACCENT_CYAN, font=get_font("impact", 28))
        d3.text((80, sy + 104), f"Catalyst: {s['catalyst'][:75]}", fill=TEXT_MUTED, font=get_font("body", 21))
        sy += 165

    d3.text((SIZE // 2, 975), "SWIPE FOR TOP BREAKING MARKET HEADLINES", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p3 = str(settings.OUTPUT_DIR / "market_slide_3.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: MAJOR BREAKING NEWS (Random Background #4)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_full_background_canvas(photos[3] if len(photos) > 3 else None, "BREAKING NEWS")
    d4 = ImageDraw.Draw(img4)

    d4.text((SIZE // 2, 115), "MAJOR MARKET NEWS:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d4.text((SIZE // 2, 195), "TOP BREAKING STORIES & CATALYSTS", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    ny = 255
    for idx, art in enumerate(news[:3], 1):
        draw_glass_panel(img4, (50, ny, SIZE - 50, ny + 175), radius=20, bg=(15, 23, 42, 225), border=BORDER_GLASS)
        title = art.get('title', '')[:65] + "..." if len(art.get('title', '')) > 68 else art.get('title', '')
        
        d4.rounded_rectangle([(80, ny + 18), (270, ny + 52)], radius=10, fill=(30, 41, 59))
        d4.text((175, ny + 35), art.get('source_name', 'News Desk').upper(), fill=ACCENT_AMBER, font=get_font("din_alt", 18), anchor="mm")
        
        d4.text((80, ny + 68), f"{idx}. {title}", fill=TEXT_WHITE, font=get_font("din_cond", 34))
        d4.text((80, ny + 125), "Key macroeconomic catalyst driving market volume and sentiment.", fill=TEXT_MUTED, font=get_font("body", 21))
        ny += 195

    draw_glass_panel(img4, (50, 875, SIZE - 50, 955), radius=16, bg=(245, 158, 11, 235), border=BORDER_AMBER)
    d4.text((SIZE // 2, 915), "FOLLOW @FINPULSE.DAILY • READ FULL SOURCES IN CAPTION", fill=TEXT_DARK, font=get_font("impact", 28), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / "market_slide_4.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
