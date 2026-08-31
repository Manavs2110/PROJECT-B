"""
services/visual_rendering_service/renderer_market_impact.py — Photo-First Editorial Market Intelligence Slides
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from PIL import Image, ImageDraw
from common.config import settings
from common.design_tokens import (
    SIZE, BG_DARK, BG_CARD, TEXT_WHITE, TEXT_MUTED, TEXT_DARK,
    ACCENT_AMBER, ACCENT_EMERALD, ACCENT_ROSE, ACCENT_CYAN, BORDER_SUBTLE,
    get_font, create_photo_editorial_canvas, draw_stat_pill
)

def render_market_impact_carousel(indices: Dict[str, Any], fii_dii: Dict[str, Any], sentiment: Dict[str, Any], news: List[Dict[str, Any]]) -> List[str]:
    """Generates 4 modern photo-first editorial slides for Post #1."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slides = []

    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]

    is_positive = nifty["is_positive"]
    hook_main = f"NIFTY {abs(nifty['change']):.0f}+ PTS MOVE • D-STREET PULSE" if is_positive else f"SENSEX TUMBLES {abs(sensex['change']):.0f}+ PTS AS BEARS TAKE CONTROL"
    hook_sub = "Bulls defend key moving average support levels" if is_positive else "Heavy institutional selling creates volatility near critical zones"

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: INDICES SCORECARD (Photo-First: BSE Dalal Street Photo)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_photo_editorial_canvas("bse_dalal_street.jpg", "MARKET PULSE")
    d1 = ImageDraw.Draw(img1)

    # Headline & Subtitle in Lower Panel
    d1.text((50, 645), hook_main.upper(), fill=TEXT_WHITE, font=get_font("impact", 44))
    d1.text((50, 705), hook_sub, fill=ACCENT_AMBER, font=get_font("body", 22))

    # 4 Stat Pills Grid (2x2)
    draw_stat_pill(d1, (50, 755, 520, 835), "NIFTY 50", f"{nifty['formatted_price']} ({nifty['change_pct']:+.2f}%)", nifty["is_positive"])
    draw_stat_pill(d1, (560, 755, SIZE - 50, 835), "BSE SENSEX", f"{sensex['formatted_price']} ({sensex['change_pct']:+.2f}%)", sensex["is_positive"])
    
    draw_stat_pill(d1, (50, 855, 520, 935), "BANK NIFTY", f"{bank['formatted_price']} ({bank['change_pct']:+.2f}%)", bank["is_positive"])
    draw_stat_pill(d1, (560, 855, SIZE - 50, 935), "INDIA VIX", f"{vix['price']:.2f} ({vix['change_pct']:+.2f}%)", vix['change'] <= 0)

    # Bottom Swipe Pill
    d1.text((50, 990), "SWIPE FOR INSTITUTIONAL CASH FLOWS", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d1.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d1.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p1 = str(settings.OUTPUT_DIR / f"market_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: INSTITUTIONAL CASH FLOWS (Photo-First: Trading Terminal)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_photo_editorial_canvas("trading_desk_charts.jpg", "INSTITUTIONAL FLOWS")
    d2 = ImageDraw.Draw(img2)

    d2.text((50, 645), "INSTITUTIONAL CASH ACTIVITY (FII & DII)", fill=TEXT_WHITE, font=get_font("impact", 44))
    d2.text((50, 705), f"Official NSE Cash Market Segment Data • {fii_dii['date']}", fill=ACCENT_AMBER, font=get_font("body", 22))

    # Flow Cards
    draw_stat_pill(d2, (50, 755, 520, 845), "FII / FPI NET FLOW", fii_dii['fii']['formatted_net'], fii_dii['fii']['net'] > 0)
    draw_stat_pill(d2, (560, 755, SIZE - 50, 845), "DII DOMESTIC NET FLOW", fii_dii['dii']['formatted_net'], fii_dii['dii']['net'] > 0)
    
    # Combined Net Balance Full Width
    draw_stat_pill(d2, (50, 865, SIZE - 50, 945), "TOTAL INSTITUTIONAL BALANCE", f"{fii_dii['formatted_total_net']} ({fii_dii['sentiment']})", fii_dii['total_net'] > 0)

    d2.text((50, 990), "SWIPE FOR SECTOR SENTIMENTS & HEATMAP", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d2.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d2.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p2 = str(settings.OUTPUT_DIR / f"market_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: SECTOR RADAR (Photo-First: Candlestick Chart Screen)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_photo_editorial_canvas("candlestick_screen.jpg", "SECTOR RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((50, 645), f"SECTOR ROTATION • {sentiment.get('market_mood', 'BULLISH').upper()}", fill=TEXT_WHITE, font=get_font("impact", 44))
    d3.text((50, 705), f"India VIX at {vix['price']:.2f} • Tactical: {sentiment.get('tactical_strategy', 'Buy leading sectors on pullbacks')}", fill=ACCENT_AMBER, font=get_font("body", 21))

    # 3 Sector Rows
    sy = 750
    for s in sentiment.get("sectors", [])[:3]:
        imp = s.get("impact", "BULLISH")
        imp_col = ACCENT_ROSE if imp == "BEARISH" else ACCENT_EMERALD
        d3.rounded_rectangle([(50, sy), (SIZE - 50, sy + 62)], radius=12, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
        d3.rounded_rectangle([(50, sy), (56, sy + 62)], radius=4, fill=imp_col)
        d3.text((70, sy + 18), s["sector_name"].upper(), fill=TEXT_WHITE, font=get_font("din_cond", 28))
        d3.text((360, sy + 20), f"({', '.join(s.get('affected_stocks', [])[:3])})", fill=ACCENT_CYAN, font=get_font("body", 18))
        
        d3.rounded_rectangle([(SIZE - 180, sy + 12), (SIZE - 68, sy + 50)], radius=10, fill=imp_col)
        d3.text((SIZE - 124, sy + 31), imp, fill=TEXT_WHITE, font=get_font("din_alt", 18), anchor="mm")
        sy += 74

    d3.text((50, 990), "SWIPE FOR TOP BREAKING HEADLINES", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d3.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d3.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p3 = str(settings.OUTPUT_DIR / f"market_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: MAJOR NEWS STORIES (Photo-First: Wall Street NYSE)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_photo_editorial_canvas("wall_street_nyse.jpg", "BREAKING NEWS")
    d4 = ImageDraw.Draw(img4)

    d4.text((50, 645), "TOP BREAKING MARKET STORIES", fill=TEXT_WHITE, font=get_font("impact", 44))
    d4.text((50, 705), "Key macroeconomic catalysts impacting broader Indian equities", fill=ACCENT_AMBER, font=get_font("body", 22))

    ny = 750
    for idx, art in enumerate(news[:3], 1):
        title = art.get('title', '')[:58] + "..." if len(art.get('title', '')) > 60 else art.get('title', '')
        d4.rounded_rectangle([(50, ny), (SIZE - 50, ny + 62)], radius=12, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
        d4.text((68, ny + 18), f"{idx}.", fill=ACCENT_AMBER, font=get_font("impact", 24))
        d4.text((100, ny + 18), title, fill=TEXT_WHITE, font=get_font("din_cond", 28))
        d4.text((SIZE - 70, ny + 20), art.get('source_name', 'News Desk')[:12].upper(), fill=ACCENT_CYAN, font=get_font("din_alt", 18), anchor="rm")
        ny += 74

    d4.text((50, 990), "FOLLOW @FINPULSE.DAILY • READ FULL SOURCES IN CAPTION", fill=ACCENT_AMBER, font=get_font("impact", 22))

    p4 = str(settings.OUTPUT_DIR / f"market_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
