"""
services/visual_rendering_service/renderer_market_impact.py — Daily Market Intelligence 4-Slide Generator (Post 1)
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from PIL import Image, ImageDraw
from common.config import settings
from common.design_tokens import (
    SIZE, C_RED_TOP, C_RED_BOT, C_BLUE_TOP, C_BLUE_BOT, C_TEAL_TOP, C_TEAL_BOT,
    C_GOLD_TOP, C_GOLD_BOT, C_EMERALD, C_AMBER, C_ROSE, C_CREAM, C_DARK, C_MAROON,
    C_WHITE, C_DIVIDER, get_font, create_gradient_canvas, add_architectural_silhouettes,
    draw_bull_motif, draw_bear_motif, draw_header
)

def render_market_impact_carousel(indices: Dict[str, Any], fii_dii: Dict[str, Any], sentiment: Dict[str, Any], news: List[Dict[str, Any]]) -> List[str]:
    """Generates the 4 1080×1080 JPEG slides for Post 1 (Market Intelligence)."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    handle = settings.PAGE_HANDLE
    slides = []

    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]

    pct = nifty["change_pct"]
    if pct >= 1.0: hook_main, hook_sub = "BULLS ON RAMPAGE!", f"NIFTY SURGES {abs(nifty['change']):.0f}+ PTS • SENSEX GAINS {abs(sensex['change']):.0f}+ PTS"
    elif pct > 0: hook_main, hook_sub = "MOMENTUM HOLDS FIRM!", f"NIFTY EDGES HIGHER • BULLS DEFEND SUPPORT"
    elif pct <= -1.0: hook_main, hook_sub = "MARKET UNDER PRESSURE!", f"SENSEX TUMBLES {abs(sensex['change']):.0f}+ PTS AS BEARS TAKE CONTROL"
    else: hook_main, hook_sub = "TIGHT ROPE ON D-STREET!", f"NIFTY RANGEBOUND • KEY BREAKOUT AHEAD"

    # Slide 1: Indices
    img1 = create_gradient_canvas(C_RED_TOP, C_RED_BOT)
    add_architectural_silhouettes(img1, (255, 200, 100), 0.18)
    d1 = ImageDraw.Draw(img1)
    draw_header(img1, d1, handle)

    d1.text((SIZE // 2, 105), hook_main, fill=C_CREAM, font=get_font("impact", 76), anchor="mt")
    d1.text((SIZE // 2, 192), hook_sub, fill=C_AMBER, font=get_font("din_cond", 48), anchor="mt")

    d1.rounded_rectangle([(70, 265), (SIZE - 70, 830)], radius=28, fill=C_CREAM)
    d1.text((310, 310), "NIFTY 50", fill=C_MAROON, font=get_font("din_cond", 40), anchor="mt")
    d1.text((310, 370), nifty["formatted_price"], fill=C_DARK, font=get_font("impact", 54), anchor="mt")
    d1.rounded_rectangle([(160, 455), (460, 500)], radius=20, fill=C_EMERALD if nifty["is_positive"] else C_ROSE)
    d1.text((310, 477), nifty["formatted_change"], fill=C_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.line([(SIZE // 2, 310), (SIZE // 2, 500)], fill=C_DIVIDER, width=2)

    d1.text((770, 310), "BSE SENSEX", fill=C_MAROON, font=get_font("din_cond", 40), anchor="mt")
    d1.text((770, 370), sensex["formatted_price"], fill=C_DARK, font=get_font("impact", 54), anchor="mt")
    d1.rounded_rectangle([(620, 455), (920, 500)], radius=20, fill=C_EMERALD if sensex["is_positive"] else C_ROSE)
    d1.text((770, 477), sensex["formatted_change"], fill=C_WHITE, font=get_font("din_alt", 22), anchor="mm")
    d1.line([(110, 535), (SIZE - 110, 535)], fill=C_DIVIDER, width=2)

    d1.text((310, 565), "BANK NIFTY", fill=C_MAROON, font=get_font("din_cond", 28), anchor="mt")
    d1.text((310, 605), f"{bank['formatted_price']} ({bank['change_pct']:+.2f}%)", fill=C_DARK, font=get_font("impact", 36), anchor="mt")
    d1.line([(SIZE // 2, 560), (SIZE // 2, 655)], fill=C_DIVIDER, width=2)
    d1.text((770, 565), "INDIA VIX (VOLATILITY)", fill=C_MAROON, font=get_font("din_cond", 28), anchor="mt")
    d1.text((770, 605), f"{vix['price']:.2f} ({vix['change_pct']:+.2f}%)", fill=C_EMERALD if vix['change'] <= 0 else C_ROSE, font=get_font("impact", 36), anchor="mt")

    d1.rounded_rectangle([(100, 690), (SIZE - 100, 785)], radius=18, fill=C_AMBER)
    d1.text((SIZE // 2, 737), f"D-STREET ACTION • {hook_main}", fill=C_DARK, font=get_font("impact", 34), anchor="mm")

    if nifty["is_positive"]: draw_bull_motif(img1, 140, 930, 80)
    else: draw_bear_motif(img1, 140, 930, 80)

    p1 = str(settings.OUTPUT_DIR / f"market_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # Slide 2: Cash Inflows
    img2 = create_gradient_canvas(C_BLUE_TOP, C_BLUE_BOT)
    add_architectural_silhouettes(img2, (56, 189, 248), 0.15)
    d2 = ImageDraw.Draw(img2)
    draw_header(img2, d2, handle)

    d2.text((SIZE // 2, 105), "NIFTY CASH INFLOWS:", fill=C_CREAM, font=get_font("impact", 72), anchor="mt")
    d2.text((SIZE // 2, 190), "FII, DII & INSTITUTIONAL PARTICIPATION", fill=C_AMBER, font=get_font("din_cond", 52), anchor="mt")
    
    d2.rounded_rectangle([(180, 255), (SIZE - 180, 315)], radius=14, fill=C_AMBER)
    d2.text((SIZE // 2, 285), f"NSE CASH SEGMENT ACTIVITY ({fii_dii['date']})", fill=C_DARK, font=get_font("impact", 30), anchor="mm")

    d2.rounded_rectangle([(70, 345), (515, 565)], radius=20, fill=C_CREAM)
    d2.text((292, 370), "FII / FPI INFLOW", fill=C_MAROON, font=get_font("din_cond", 38), anchor="mt")
    d2.text((292, 425), fii_dii['fii']['formatted_net'], fill=C_EMERALD if fii_dii['fii']['net'] > 0 else C_ROSE, font=get_font("impact", 48), anchor="mt")
    d2.text((292, 500), f"Stance: {fii_dii['fii']['bias']}", fill=C_DARK, font=get_font("din_alt", 24), anchor="mt")

    d2.rounded_rectangle([(565, 345), (SIZE - 70, 565)], radius=20, fill=C_CREAM)
    d2.text((787, 370), "DII (DOMESTIC) INFLOW", fill=C_MAROON, font=get_font("din_cond", 38), anchor="mt")
    d2.text((787, 425), fii_dii['dii']['formatted_net'], fill=C_EMERALD if fii_dii['dii']['net'] > 0 else C_ROSE, font=get_font("impact", 48), anchor="mt")
    d2.text((787, 500), f"Stance: {fii_dii['dii']['bias']}", fill=C_DARK, font=get_font("din_alt", 24), anchor="mt")

    d2.rounded_rectangle([(70, 595), (SIZE - 70, 745)], radius=20, fill=C_WHITE)
    d2.text((SIZE // 2, 615), "TOTAL COMBINED INSTITUTIONAL NET", fill=C_MAROON, font=get_font("din_cond", 36), anchor="mt")
    d2.text((SIZE // 2, 660), fii_dii['formatted_total_net'], fill=C_EMERALD if fii_dii['total_net'] > 0 else C_ROSE, font=get_font("impact", 56), anchor="mt")

    d2.rounded_rectangle([(70, 775), (SIZE - 70, 895)], radius=18, fill=C_AMBER)
    d2.text((SIZE // 2, 802), "RETAIL & CLIENT FLOWS: HEALTHY ABSORPTION", fill=C_DARK, font=get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 850), "Steady retail participation & long derivative roll-overs into next series", fill=C_DARK, font=get_font("din_alt", 22), anchor="mt")

    if fii_dii['total_net'] > 0: draw_bull_motif(img2, SIZE - 120, 670, 75)
    else: draw_bear_motif(img2, SIZE - 120, 670, 75)

    p2 = str(settings.OUTPUT_DIR / f"market_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # Slide 3: Sentiments
    img3 = create_gradient_canvas(C_TEAL_TOP, C_TEAL_BOT)
    add_architectural_silhouettes(img3, (34, 211, 238), 0.16)
    d3 = ImageDraw.Draw(img3)
    draw_header(img3, d3, handle)

    d3.text((SIZE // 2, 105), "MARKET SENTIMENTS:", fill=C_CREAM, font=get_font("impact", 72), anchor="mt")
    d3.text((SIZE // 2, 190), "FEAR, GREED & SECTOR RADAR", fill=C_AMBER, font=get_font("din_cond", 52), anchor="mt")

    d3.rounded_rectangle([(70, 265), (SIZE - 70, 385)], radius=20, fill=C_CREAM)
    d3.text((SIZE // 2, 285), f"OVERALL MARKET SENTIMENT: {sentiment.get('market_mood', 'BULLISH').upper()}", fill=C_MAROON, font=get_font("impact", 36), anchor="mt")
    d3.text((SIZE // 2, 338), f"India VIX: {vix['price']:.2f} • {sentiment.get('vix_interpretation', 'Calm volatility')}", fill=C_DARK, font=get_font("body", 22), anchor="mt")

    sy = 415
    for s in sentiment.get("sectors", [])[:3]:
        imp = s.get("impact", "BULLISH")
        d3.rounded_rectangle([(70, sy), (SIZE - 70, sy + 148)], radius=20, fill=C_CREAM)
        d3.text((105, sy + 18), s["sector_name"].upper(), fill=C_MAROON, font=get_font("din_cond", 36))
        d3.rounded_rectangle([(SIZE - 230, sy + 16), (SIZE - 100, sy + 54)], radius=12, fill=C_ROSE if imp == "BEARISH" else C_EMERALD)
        d3.text((SIZE - 165, sy + 35), imp, fill=C_WHITE, font=get_font("din_alt", 22), anchor="mm")
        d3.text((105, sy + 62), f"Tickers: {'   •   '.join(s.get('affected_stocks', [])[:4])}", fill=C_DARK, font=get_font("impact", 30))
        d3.text((105, sy + 104), f"Catalyst: {s['catalyst'][:75]}", fill=C_MAROON, font=get_font("body", 21))
        sy += 168

    d3.rounded_rectangle([(SIZE // 2 - 95, 935 - 24), (SIZE // 2 + 95, 935 + 24)], radius=24, fill=C_CREAM)
    d3.text((SIZE // 2 - 10, 935), "SWIPE", fill=C_DARK, font=get_font("din_alt", 26), anchor="mm")
    d3.polygon([(SIZE // 2 + 44, 927), (SIZE // 2 + 56, 935), (SIZE // 2 + 44, 943)], fill=C_DARK)

    p3 = str(settings.OUTPUT_DIR / f"market_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # Slide 4: Major News
    img4 = create_gradient_canvas(C_GOLD_TOP, C_GOLD_BOT)
    add_architectural_silhouettes(img4, (254, 240, 138), 0.18)
    d4 = ImageDraw.Draw(img4)
    draw_header(img4, d4, handle)

    d4.rounded_rectangle([(70, 115), (SIZE - 70, 895)], radius=28, fill=C_CREAM)
    d4.text((SIZE // 2, 145), "MAJOR MARKET NEWS:", fill=C_MAROON, font=get_font("impact", 54), anchor="mt")
    d4.text((SIZE // 2, 215), "TOP BREAKING STORIES & CATALYSTS", fill=C_DARK, font=get_font("din_cond", 40), anchor="mt")

    ny = 285
    for idx, art in enumerate(news[:3], 1):
        d4.rounded_rectangle([(100, ny), (SIZE - 100, ny + 155)], radius=18, fill=C_WHITE)
        title = art.get('title', '')[:62] + "..." if len(art.get('title', '')) > 65 else art.get('title', '')
        d4.text((125, ny + 16), f"{idx}. {title}", fill=C_DARK, font=get_font("din_cond", 32))
        d4.text((125, ny + 58), "Key macroeconomic development impacting broader equities.", fill=C_MAROON, font=get_font("body", 20))
        d4.text((125, ny + 112), f"SOURCE: {art.get('source_name', 'News Desk').upper()}", fill=C_DARK, font=get_font("din_alt", 20))
        ny += 175

    d4.rounded_rectangle([(100, 815), (SIZE - 100, 870)], radius=14, fill=C_AMBER)
    d4.text((SIZE // 2, 842), "FOLLOW @FINPULSE.DAILY • READ FULL LINKS IN CAPTION", fill=C_DARK, font=get_font("impact", 28), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / f"market_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
