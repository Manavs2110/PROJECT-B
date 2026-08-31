"""
services/visual_rendering_service/renderer_prediction.py — Modern Glassmorphism NIFTY 50 Prediction Carousel
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

def render_prediction_carousel(model: Dict[str, Any]) -> List[str]:
    """Generates 4 high-conviction glassmorphic 1080×1080 slides for Post 2."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    handle = settings.PAGE_HANDLE
    slides = []

    tech = model["technical_data"]
    derivs = model["derivatives_data"]
    pred = model["prediction"]
    pivots = tech["pivots"]
    mas = tech["moving_averages"]
    playbook = pred.get("trade_playbook", {})
    is_bull = pred.get("probability_bull_pct", 50) >= 50

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: NIFTY 50 PREDICTION & TARGETS (Candlestick Depth Chart Background)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_cinematic_photo_canvas("candlestick_screen.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img1, handle, "NIFTY 50 TARGETS")
    d1 = ImageDraw.Draw(img1)

    d1.text((SIZE // 2, 110), "NIFTY 50 PREDICTION:", fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d1.text((SIZE // 2, 190), "TOMORROW'S TARGETS & EXPECTED RANGE", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # Center Hero Glass Card
    draw_glass_card(img1, (65, 260, SIZE - 65, 620), radius=24, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER_HI)
    d1.text((SIZE // 2, 290), "PRIMARY PREDICTED BIAS", fill=COLOR_MUTED, font=get_font("din_cond", 34), anchor="mt")
    d1.text((SIZE // 2, 340), pred.get("predicted_trend", "BULLISH BREAKOUT"), fill=COLOR_WHITE, font=get_font("impact", 48), anchor="mt")

    # Probability Pill
    prob_col = COLOR_EMERALD if is_bull else COLOR_ROSE
    d1.rounded_rectangle([(SIZE // 2 - 170, 425), (SIZE // 2 + 170, 475)], radius=18, fill=prob_col)
    d1.text((SIZE // 2, 450), f"CONFIDENCE: {pred.get('probability_bull_pct', 65)}% PROBABILITY", fill=COLOR_WHITE, font=get_font("din_alt", 22), anchor="mm")

    d1.line([(110, 505), (SIZE - 110, 505)], fill=(51, 65, 85), width=2)
    d1.text((SIZE // 2, 525), "EXPECTED SESSION RANGE", fill=COLOR_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((SIZE // 2, 560), pred.get("expected_trading_range", "24,000 — 24,350"), fill=COLOR_AMBER, font=get_font("impact", 54), anchor="mt")

    # Lower Glass Pivot Card
    draw_glass_card(img1, (65, 650, SIZE - 65, 790), radius=20, bg_color=(10, 15, 28, 235), border_color=GLASS_BORDER)
    d1.text((292, 675), "KEY MAKE-OR-BREAK PIVOT", fill=COLOR_MUTED, font=get_font("din_cond", 28), anchor="mt")
    d1.text((292, 715), f"{pivots['pivot']:,.2f}", fill=COLOR_AMBER, font=get_font("impact", 42), anchor="mt")
    
    d1.line([(SIZE // 2, 670), (SIZE // 2, 770)], fill=(51, 65, 85), width=2)
    
    d1.text((787, 675), "CURRENT SPOT PRICE", fill=COLOR_MUTED, font=get_font("din_cond", 28), anchor="mt")
    d1.text((787, 715), tech["formatted_price"], fill=COLOR_WHITE, font=get_font("impact", 42), anchor="mt")

    # Bottom Swipe Banner
    draw_glass_card(img1, (65, 820, SIZE - 65, 900), radius=16, bg_color=(245, 158, 11, 230), border_color=(245, 158, 11, 255))
    d1.text((SIZE // 2, 860), "SWIPE FOR TECHNICAL BLUEPRINT & TRADE PLAYBOOK", fill=(15, 23, 42), font=get_font("impact", 28), anchor="mm")

    if is_bull: draw_bull_badge(img1, 130, 960, 75)
    else: draw_bear_badge(img1, 130, 960, 75)

    p1 = str(settings.OUTPUT_DIR / f"nifty_pred_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: TECHNICAL BLUEPRINT (Trading Desk Charts Background)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_cinematic_photo_canvas("trading_desk_charts.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img2, handle, "TECHNICAL LEVELS")
    d2 = ImageDraw.Draw(img2)

    d2.text((SIZE // 2, 110), "TECHNICAL BLUEPRINT:", fill=COLOR_WHITE, font=get_font("impact", 72), anchor="mt")
    d2.text((SIZE // 2, 190), "KEY SUPPORTS, RESISTANCES & MOVING AVERAGES", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # Resistances Card
    draw_glass_card(img2, (65, 260, 520, 480), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d2.text((292, 285), "KEY RESISTANCES", fill=COLOR_ROSE, font=get_font("din_cond", 36), anchor="mt")
    d2.text((292, 335), f"R1: {pivots['r1']:,.0f}", fill=COLOR_WHITE, font=get_font("impact", 42), anchor="mt")
    d2.text((292, 395), f"R2: {pivots['r2']:,.0f}", fill=COLOR_ROSE, font=get_font("impact", 42), anchor="mt")

    # Supports Card
    draw_glass_card(img2, (560, 260, SIZE - 65, 480), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d2.text((787, 285), "KEY SUPPORTS", fill=COLOR_EMERALD, font=get_font("din_cond", 36), anchor="mt")
    d2.text((787, 335), f"S1: {pivots['s1']:,.0f}", fill=COLOR_WHITE, font=get_font("impact", 42), anchor="mt")
    d2.text((787, 395), f"S2: {pivots['s2']:,.0f}", fill=COLOR_EMERALD, font=get_font("impact", 42), anchor="mt")

    # Moving Averages Dashboard
    draw_glass_card(img2, (65, 510, SIZE - 65, 730), radius=22, bg_color=(10, 15, 28, 240), border_color=GLASS_BORDER)
    d2.text((SIZE // 2, 530), "MOVING AVERAGE ALIGNMENT", fill=COLOR_AMBER, font=get_font("din_cond", 34), anchor="mt")
    d2.text((220, 585), f"20 EMA: {mas['ema_20']:,.0f}", fill=COLOR_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 585), f"50 SMA: {mas['sma_50']:,.0f}", fill=COLOR_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((860, 585), f"200 SMA: {mas['sma_200']:,.0f}", fill=COLOR_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 660), f"Status: {mas['alignment']}", fill=COLOR_EMERALD if "Bullish" in mas['alignment'] else COLOR_ROSE, font=get_font("din_alt", 24), anchor="mt")

    # RSI Oscillator Bar
    draw_glass_card(img2, (65, 760, SIZE - 65, 880), radius=18, bg_color=(15, 23, 42, 220), border_color=GLASS_BORDER)
    d2.text((SIZE // 2, 785), f"RSI (14-PERIOD): {tech['oscillators']['rsi_14']} • {tech['oscillators']['rsi_status'].upper()}", fill=COLOR_WHITE, font=get_font("impact", 30), anchor="mt")
    d2.text((SIZE // 2, 830), "Healthy momentum oscillator without overbought exhaustion", fill=COLOR_MUTED, font=get_font("body", 22), anchor="mt")

    p2 = str(settings.OUTPUT_DIR / f"nifty_pred_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: DERIVATIVES & PCR RADAR (Financial District Background)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_cinematic_photo_canvas("financial_district.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img3, handle, "DERIVATIVES RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((SIZE // 2, 110), "DERIVATIVES & PCR RADAR:", fill=COLOR_WHITE, font=get_font("impact", 70), anchor="mt")
    d3.text((SIZE // 2, 190), "OPTION CHAIN OPEN INTEREST & VOLATILITY", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    # PCR Card
    draw_glass_card(img3, (65, 260, SIZE - 65, 450), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d3.text((SIZE // 2, 285), "NIFTY PUT-CALL RATIO (PCR)", fill=COLOR_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d3.text((SIZE // 2, 335), f"{derivs['pcr']:.2f} ({derivs['pcr_bias'].upper()})", fill=COLOR_WHITE, font=get_font("impact", 54), anchor="mt")
    d3.text((SIZE // 2, 400), "Signals supportive put writing cushion on lower strike boundaries", fill=COLOR_AMBER, font=get_font("body", 22), anchor="mt")

    # Call & Put Strike Boundaries
    draw_glass_card(img3, (65, 480, 520, 690), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d3.text((292, 505), "MAJOR CALL RESISTANCE", fill=COLOR_ROSE, font=get_font("din_cond", 34), anchor="mt")
    d3.text((292, 560), derivs["key_resistance_strike"], fill=COLOR_WHITE, font=get_font("impact", 36), anchor="mt")
    d3.text((292, 625), "Heavy Call OI Cap", fill=COLOR_MUTED, font=get_font("body", 22), anchor="mt")

    draw_glass_card(img3, (560, 480, SIZE - 65, 690), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d3.text((787, 505), "MAJOR PUT SUPPORT", fill=COLOR_EMERALD, font=get_font("din_cond", 34), anchor="mt")
    d3.text((787, 560), derivs["key_support_strike"], fill=COLOR_WHITE, font=get_font("impact", 36), anchor="mt")
    d3.text((787, 625), "Solid Put Writing Floor", fill=COLOR_MUTED, font=get_font("body", 22), anchor="mt")

    # Options Strategy Banner
    draw_glass_card(img3, (65, 720, SIZE - 65, 880), radius=18, bg_color=(245, 158, 11, 230), border_color=(245, 158, 11, 255))
    d3.text((SIZE // 2, 745), "RECOMMENDED OPTIONS STRATEGY", fill=(15, 23, 42), font=get_font("impact", 32), anchor="mt")
    d3.text((SIZE // 2, 800), pred.get("options_strategy", "Bull Call Spread with defined risk"), fill=(15, 23, 42), font=get_font("din_cond", 36), anchor="mt")

    p3 = str(settings.OUTPUT_DIR / f"nifty_pred_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: ACTIONABLE TRADE PLAYBOOK (Wall Street NYSE Background)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_cinematic_photo_canvas("wall_street_nyse.jpg", vignette_color=(15, 23, 42), darken_factor=0.6)
    draw_header_bar(img4, handle, "TRADE PLAYBOOK")
    d4 = ImageDraw.Draw(img4)

    d4.text((SIZE // 2, 110), "TACTICAL TRADE PLAYBOOK:", fill=COLOR_WHITE, font=get_font("impact", 68), anchor="mt")
    d4.text((SIZE // 2, 190), "ACTIONABLE ENTRY, STOP LOSS & PROFIT TARGETS", fill=COLOR_AMBER, font=get_font("din_cond", 44), anchor="mt")

    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    # Plan A: Bull Setup
    draw_glass_card(img4, (65, 260, SIZE - 65, 520), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d4.text((95, 280), "PLAN A: BULLISH TRADE SETUP", fill=COLOR_EMERALD, font=get_font("impact", 32))
    d4.text((95, 330), f"• Trigger: {bull_p.get('trigger', 'Buy on breakout above pivot')}", fill=COLOR_WHITE, font=get_font("body", 22))
    d4.text((95, 370), f"• Stop Loss: {bull_p.get('stop_loss', 'S1 Level')}", fill=COLOR_ROSE, font=get_font("body", 22))
    d4.text((95, 410), f"• Targets: T1 {bull_p.get('target_1', 'R1')}  |  T2 {bull_p.get('target_2', 'R2')}", fill=COLOR_EMERALD, font=get_font("body", 22))
    d4.text((95, 450), f"• Risk-to-Reward: {bull_p.get('risk_reward', '1 : 2.5')}", fill=COLOR_AMBER, font=get_font("body", 22))

    # Plan B: Bear Setup
    draw_glass_card(img4, (65, 550, SIZE - 65, 810), radius=22, bg_color=(15, 23, 42, 235), border_color=GLASS_BORDER)
    d4.text((95, 570), "PLAN B: BEARISH DEFENSE SETUP", fill=COLOR_ROSE, font=get_font("impact", 32))
    d4.text((95, 620), f"• Trigger: {bear_p.get('trigger', 'Sell on breakdown below S1')}", fill=COLOR_WHITE, font=get_font("body", 22))
    d4.text((95, 660), f"• Stop Loss: {bear_p.get('stop_loss', 'Pivot Level')}", fill=COLOR_ROSE, font=get_font("body", 22))
    d4.text((95, 700), f"• Targets: T1 {bear_p.get('target_1', 'S2')}  |  T2 {bear_p.get('target_2', 'S3')}", fill=COLOR_WHITE, font=get_font("body", 22))
    d4.text((95, 740), f"• Risk-to-Reward: {bear_p.get('risk_reward', '1 : 2.0')}", fill=COLOR_AMBER, font=get_font("body", 22))

    # Bottom CTA Banner
    draw_glass_card(img4, (65, 840, SIZE - 65, 920), radius=16, bg_color=(245, 158, 11, 230), border_color=(245, 158, 11, 255))
    d4.text((SIZE // 2, 880), "SAVE THIS POST FOR TOMORROW'S SESSION • @FINPULSE.DAILY", fill=(15, 23, 42), font=get_font("impact", 28), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / f"nifty_pred_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
