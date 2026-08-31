"""
services/visual_rendering_service/renderer_market_impact.py — Modern Glassmorphism Market Intelligence Carousel
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from PIL import Image, ImageDraw
from common.config import settings
from common.design_tokens import (
    SIZE, COLOR_WHITE, COLOR_OFFWHITE, COLOR_MUTED, COLOR_AMBER, COLOR_EMERALD, COLOR_ROSE,
    COLOR_CYAN, GLASS_BG_DARK, GLASS_BORDER, GLASS_BORDER_HI, get_font,
    create_cinematic_photo_canvas, draw_glass_card, draw_header_bar, draw_bull_badge, draw_bear_badge
)

def render_market_impact_carousel(indices: Dict[str, Any], fii_dii: Dict[str, Any], sentiment: Dict[str, Any], news: List[Dict[str, Any]]) -> List[str]:
    """Generates 4 high-conviction glassmorphic 1080×1080 slides for Post 1."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    handle = settings.PAGE_HANDLE
    slides = []

    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]

    pct = nifty["change_pct"]
    is_positive = nifty["is_positive"]
    if pct >= 1.0: hook_main, hook_sub = "BULLS ON RAMPAGE!", f"NIFTY SURGES {abs(nifty['change']):.0f}+ PTS • D-STREET RALLIES"
    elif pct > 0: hook_main, hook_sub = "MOMENTUM HOLDS FIRM!", f"NIFTY DEFENDS SUPPORT • BULLS IN CONTROL"
    elif pct <= -1.0: hook_main, hook_sub = "MARKET UNDER PRESSURE!", f"SENSEX TUMBLES {abs(sensex['change']):.0f}+ PTS AS BEARS TAKE OVER"
    else: hook_main, hook_sub = "TIGHT ROPE ON D-STREET!", f"NIFTY RANGEBOUND • KEY BREAKOUT AHEAD"

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: INDICES SCORECARD (BSE Dalal Street Photographic Background)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_cinematic_photo_canvas("bse_dalal_street.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img1, handle, "MARKET PULSE")
    d1 = ImageDraw.Draw(img1)

    # Hero Headline
    d1.text((SIZE // 2, 110), hook_main, fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d1.text((SIZE // 2, 190), hook_sub, fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # NIFTY 50 Glass Card (Left)
    draw_glass_card(img1, (65, 260, 520, 600), radius=24, bg_color=(15, 23, 42, 230), border_color=GLASS_BORDER)
    d1.text((292, 290), "NIFTY 50", fill=COLOR_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d1.text((292, 345), nifty["formatted_price"], fill=COLOR_WHITE, font=get_font("impact", 54), anchor="mt")
    
    # Change Pill
    pill_col = COLOR_EMERALD if is_positive else COLOR_ROSE
    d1.rounded_rectangle([(150, 435), (435, 485)], radius=18, fill=pill_col)
    d1.text((292, 460), nifty["formatted_change"], fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.text((292, 530), f"Stance: {nifty['bias']}", fill=pill_col, font=get_font("impact", 26), anchor="mt")

    # SENSEX Glass Card (Right)
    draw_glass_card(img1, (560, 260, SIZE - 65, 600), radius=24, bg_color=(15, 23, 42, 230), border_color=GLASS_BORDER)
    d1.text((787, 290), "BSE SENSEX", fill=COLOR_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d1.text((787, 345), sensex["formatted_price"], fill=COLOR_WHITE, font=get_font("impact", 54), anchor="mt")
    
    pill_col_s = COLOR_EMERALD if sensex["is_positive"] else COLOR_ROSE
    d1.rounded_rectangle([(645, 435), (930, 485)], radius=18, fill=pill_col_s)
    d1.text((787, 460), sensex["formatted_change"], fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.text((787, 530), f"Stance: {sensex['bias']}", fill=pill_col_s, font=get_font("impact", 26), anchor="mt")

    # Lower Glass Bar (Bank Nifty & India VIX)
    draw_glass_card(img1, (65, 630, SIZE - 65, 780), radius=20, bg_color=(10, 15, 28, 235), border_color=GLASS_BORDER)
    d1.text((292, 655), "BANK NIFTY", fill=COLOR_MUTED, font=get_font("din_cond", 28), anchor="mt")
    d1.text((292, 700), f"{bank['formatted_price']} ({bank['change_pct']:+.2f}%)", fill=COLOR_WHITE, font=get_font("impact", 36), anchor="mt")
    
    d1.line([(SIZE // 2, 650), (SIZE // 2, 760)], fill=(51, 65, 85), width=2)
    
    d1.text((787, 655), "INDIA VIX (VOLATILITY)", fill=COLOR_MUTED, font=get_font("din_cond", 28), anchor="mt")
    d1.text((787, 700), f"{vix['price']:.2f} ({vix['change_pct']:+.2f}%)", fill=COLOR_EMERALD if vix['change'] <= 0 else COLOR_ROSE, font=get_font("impact", 36), anchor="mt")

    # Bottom Banner
    draw_glass_card(img1, (65, 810, SIZE - 65, 890), radius=16, bg_color=(245, 158, 11, 230), border_color=(245, 158, 11, 255))
    d1.text((SIZE // 2, 850), f"D-STREET ACTION • SWIPE FOR FII/DII INSTITUTIONAL FLOWS", fill=(15, 23, 42), font=get_font("impact", 28), anchor="mm")

    if is_positive: draw_bull_badge(img1, 130, 960, 75)
    else: draw_bear_badge(img1, 130, 960, 75)

    p1 = str(settings.OUTPUT_DIR / f"market_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: INSTITUTIONAL CASH INFLOWS (Trading Terminal Background)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_cinematic_photo_canvas("trading_desk_charts.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img2, handle, "INSTITUTIONAL FLOWS")
    d2 = ImageDraw.Draw(img2)

    d2.text((SIZE // 2, 110), "NIFTY CASH INFLOWS:", fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d2.text((SIZE // 2, 190), f"FII / FPI & DII NET POSITIONING ({fii_dii['date']})", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # FII Battle Card
    fii_col = COLOR_EMERALD if fii_dii['fii']['net'] > 0 else COLOR_ROSE
    draw_glass_card(img2, (65, 260, 520, 560), radius=24, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d2.text((292, 290), "FOREIGN INSTITUTIONAL (FII)", fill=COLOR_MUTED, font=get_font("din_cond", 32), anchor="mt")
    d2.text((292, 350), fii_dii['fii']['formatted_net'], fill=fii_col, font=get_font("impact", 48), anchor="mt")
    d2.rounded_rectangle([(180, 445), (405, 495)], radius=16, fill=fii_col)
    d2.text((292, 470), fii_dii['fii']['bias'], fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")

    # DII Battle Card
    dii_col = COLOR_EMERALD if fii_dii['dii']['net'] > 0 else COLOR_ROSE
    draw_glass_card(img2, (560, 260, SIZE - 65, 560), radius=24, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d2.text((787, 290), "DOMESTIC INSTITUTIONAL (DII)", fill=COLOR_MUTED, font=get_font("din_cond", 32), anchor="mt")
    d2.text((787, 350), fii_dii['dii']['formatted_net'], fill=dii_col, font=get_font("impact", 48), anchor="mt")
    d2.rounded_rectangle([(675, 445), (900, 495)], radius=16, fill=dii_col)
    d2.text((787, 470), fii_dii['dii']['bias'], fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")

    # Total Net Bar
    tot_col = COLOR_EMERALD if fii_dii['total_net'] > 0 else COLOR_ROSE
    draw_glass_card(img2, (65, 590, SIZE - 65, 750), radius=22, bg_color=(10, 15, 28, 240), border_color=GLASS_BORDER_HI)
    d2.text((SIZE // 2, 615), "COMBINED NET INSTITUTIONAL CASH BALANCE", fill=COLOR_AMBER, font=get_font("din_cond", 34), anchor="mt")
    d2.text((SIZE // 2, 665), fii_dii['formatted_total_net'], fill=tot_col, font=get_font("impact", 54), anchor="mt")

    # Retail / Pro Note
    draw_glass_card(img2, (65, 780, SIZE - 65, 890), radius=18, bg_color=(15, 23, 42, 220), border_color=GLASS_BORDER)
    d2.text((SIZE // 2, 805), "RETAIL & CLIENT FLOWS: HEALTHY ABSORPTION", fill=COLOR_WHITE, font=get_font("impact", 30), anchor="mt")
    d2.text((SIZE // 2, 850), "Strong domestic SIP inflows & retail liquidity absorbing institutional selling", fill=COLOR_MUTED, font=get_font("body", 22), anchor="mt")

    p2 = str(settings.OUTPUT_DIR / f"market_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: SECTOR RADAR (Candlestick Screen Background)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_cinematic_photo_canvas("candlestick_screen.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img3, handle, "SECTOR RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((SIZE // 2, 110), "MARKET SENTIMENTS:", fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d3.text((SIZE // 2, 190), "FEAR, GREED & SECTOR IMPACT MATRIX", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # Sentiment Header Card
    draw_glass_card(img3, (65, 255, SIZE - 65, 375), radius=20, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d3.text((SIZE // 2, 275), f"OVERALL MARKET SENTIMENT: {sentiment.get('market_mood', 'BULLISH').upper()}", fill=COLOR_AMBER, font=get_font("impact", 36), anchor="mt")
    d3.text((SIZE // 2, 330), f"India VIX at {vix['price']:.2f} • {sentiment.get('vix_interpretation', 'Calm volatility environment')}", fill=COLOR_OFFWHITE, font=get_font("body", 22), anchor="mt")

    # 3 Sector Cards
    sy = 405
    for s in sentiment.get("sectors", [])[:3]:
        imp = s.get("impact", "BULLISH")
        imp_col = COLOR_ROSE if imp == "BEARISH" else COLOR_EMERALD
        draw_glass_card(img3, (65, sy, SIZE - 65, sy + 145), radius=18, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
        
        d3.text((95, sy + 18), s["sector_name"].upper(), fill=COLOR_WHITE, font=get_font("din_cond", 36))
        
        # Impact Badge
        d3.rounded_rectangle([(SIZE - 230, sy + 16), (SIZE - 95, sy + 54)], radius=12, fill=imp_col)
        d3.text((SIZE - 162, sy + 35), imp, fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")
        
        d3.text((95, sy + 62), f"Tickers: {'   •   '.join(s.get('affected_stocks', [])[:4])}", fill=COLOR_CYAN, font=get_font("impact", 28))
        d3.text((95, sy + 104), f"Catalyst: {s['catalyst'][:75]}", fill=COLOR_MUTED, font=get_font("body", 21))
        sy += 165

    # Swipe Pill
    d3.rounded_rectangle([(SIZE // 2 - 95, 935 - 24), (SIZE // 2 + 95, 935 + 24)], radius=24, fill=COLOR_AMBER)
    d3.text((SIZE // 2 - 10, 935), "SWIPE", fill=(15, 23, 42), font=get_font("din_alt", 26), anchor="mm")
    d3.polygon([(SIZE // 2 + 44, 927), (SIZE // 2 + 56, 935), (SIZE // 2 + 44, 943)], fill=(15, 23, 42))

    p3 = str(settings.OUTPUT_DIR / f"market_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: MAJOR BREAKING NEWS (Wall Street Background)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_cinematic_photo_canvas("wall_street_nyse.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img4, handle, "BREAKING NEWS")
    d4 = ImageDraw.Draw(img4)

    d4.text((SIZE // 2, 110), "MAJOR MARKET NEWS:", fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d4.text((SIZE // 2, 190), "TOP BREAKING STORIES & CATALYSTS", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    ny = 265
    for idx, art in enumerate(news[:3], 1):
        draw_glass_card(img4, (65, ny, SIZE - 65, ny + 175), radius=20, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
        title = art.get('title', '')[:65] + "..." if len(art.get('title', '')) > 68 else art.get('title', '')
        
        # Source Pill
        d4.rounded_rectangle([(95, ny + 18), (280, ny + 52)], radius=10, fill=(30, 41, 59))
        d4.text((187, ny + 35), art.get('source_name', 'News Desk').upper(), fill=COLOR_AMBER, font=get_font("din_alt", 18), anchor="mm")
        
        d4.text((95, ny + 68), f"{idx}. {title}", fill=COLOR_WHITE, font=get_font("din_cond", 34))
        d4.text((95, ny + 125), "Key macroeconomic catalyst driving market volume and sentiment.", fill=COLOR_MUTED, font=get_font("body", 21))
        ny += 195

    # Bottom CTA Banner
    draw_glass_card(img4, (65, 875, SIZE - 65, 955), radius=16, bg_color=(245, 158, 11, 230), border_color=(245, 158, 11, 255))
    d4.text((SIZE // 2, 915), "FOLLOW @FINPULSE.DAILY • READ FULL SOURCES IN CAPTION", fill=(15, 23, 42), font=get_font("impact", 28), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / f"market_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
