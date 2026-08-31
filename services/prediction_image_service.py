"""
prediction_image_service.py — 4-Slide NIFTY 50 Prediction Visual Engine
Renders high-impact 1080×1080 technical and sentimental prediction carousels.
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont
from config.settings import settings
from services.image_service import (
    SIZE, C_RED_TOP, C_RED_BOT, C_BLUE_TOP, C_BLUE_BOT, C_TEAL_TOP, C_TEAL_BOT,
    C_GOLD_TOP, C_GOLD_BOT, C_EMERALD, C_AMBER, C_ROSE, C_CREAM, C_DARK, C_MAROON,
    C_WHITE, C_DIVIDER, _get_font, create_gradient_bg, add_architectural_silhouettes,
    draw_bull_motif, draw_bear_motif, draw_header
)

def generate_nifty_prediction_carousel(model: Dict[str, Any]) -> List[str]:
    """Generates the 4 1080×1080 NIFTY 50 Prediction slides."""
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
    # SLIDE 1: NIFTY 50 PREDICTION & EXPECTED RANGE (HERO TARGETS)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_gradient_bg(C_RED_TOP, C_RED_BOT)
    add_architectural_silhouettes(img1, (255, 200, 100), 0.18)
    d1 = ImageDraw.Draw(img1)
    draw_header(img1, d1, handle)

    d1.text((SIZE // 2, 105), "NIFTY 50 PREDICTION:", fill=C_CREAM, font=_get_font("impact", 72), anchor="mt")
    d1.text((SIZE // 2, 190), "TOMORROW'S TARGETS & EXPECTED RANGE", fill=C_AMBER, font=_get_font("din_cond", 48), anchor="mt")

    # Center Hero Card
    d1.rounded_rectangle([(70, 265), (SIZE - 70, 830)], radius=28, fill=C_CREAM)
    
    # Primary Predicted Bias
    d1.text((SIZE // 2, 300), "PRIMARY MARKET BIAS", fill=C_MAROON, font=_get_font("din_cond", 36), anchor="mt")
    d1.text((SIZE // 2, 345), pred.get("predicted_trend", "BULLISH BREAKOUT"), fill=C_DARK, font=_get_font("impact", 44), anchor="mt")

    # Probability Pill
    prob_col = C_EMERALD if is_bull else C_ROSE
    d1.rounded_rectangle([(SIZE // 2 - 160, 415), (SIZE // 2 + 160, 465)], radius=16, fill=prob_col)
    d1.text((SIZE // 2, 440), f"CONFIDENCE: {pred.get('probability_bull_pct', 65)}% PROBABILITY", fill=C_WHITE, font=_get_font("din_alt", 22), anchor="mm")

    # Horizontal Divider
    d1.line([(110, 495), (SIZE - 110, 495)], fill=C_DIVIDER, width=2)

    # Expected Range Box
    d1.text((SIZE // 2, 520), "EXPECTED SESSION RANGE", fill=C_MAROON, font=_get_font("din_cond", 34), anchor="mt")
    d1.text((SIZE // 2, 565), pred.get("expected_trading_range", "24,000 — 24,350"), fill=C_DARK, font=_get_font("impact", 56), anchor="mt")

    # Make or Break Pivot
    d1.line([(110, 650), (SIZE - 110, 650)], fill=C_DIVIDER, width=2)
    d1.text((310, 675), "KEY MAKE-OR-BREAK PIVOT", fill=C_MAROON, font=_get_font("din_cond", 28), anchor="mt")
    d1.text((310, 715), f"{pivots['pivot']:,.2f}", fill=C_DARK, font=_get_font("impact", 38), anchor="mt")

    d1.line([(SIZE // 2, 670), (SIZE // 2, 770)], fill=C_DIVIDER, width=2)

    d1.text((770, 675), "CURRENT NIFTY SPOT", fill=C_MAROON, font=_get_font("din_cond", 28), anchor="mt")
    d1.text((770, 715), tech["formatted_price"], fill=C_DARK, font=_get_font("impact", 38), anchor="mt")

    # Bottom Mascot
    if is_bull: draw_bull_motif(img1, 140, 930, 80)
    else: draw_bear_motif(img1, 140, 930, 80)

    p1 = str(settings.OUTPUT_DIR / f"nifty_pred_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: TECHNICAL BREAKDOWN (PIVOTS, MOVING AVERAGES & RSI)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_gradient_bg(C_TEAL_TOP, C_TEAL_BOT)
    add_architectural_silhouettes(img2, (34, 211, 238), 0.16)
    d2 = ImageDraw.Draw(img2)
    draw_header(img2, d2, handle)

    d2.text((SIZE // 2, 105), "TECHNICAL BLUEPRINT:", fill=C_CREAM, font=_get_font("impact", 72), anchor="mt")
    d2.text((SIZE // 2, 190), "KEY SUPPORTS, RESISTANCES & MOVING AVERAGES", fill=C_AMBER, font=_get_font("din_cond", 46), anchor="mt")

    # Support & Resistance Cards
    # Resistances
    d2.rounded_rectangle([(70, 265), (515, 475)], radius=20, fill=C_CREAM)
    d2.text((292, 285), "KEY RESISTANCES", fill=C_ROSE, font=_get_font("din_cond", 36), anchor="mt")
    d2.text((292, 335), f"R1: {pivots['r1']:,.0f}", fill=C_DARK, font=_get_font("impact", 40), anchor="mt")
    d2.text((292, 395), f"R2: {pivots['r2']:,.0f}", fill=C_ROSE, font=_get_font("impact", 40), anchor="mt")

    # Supports
    d2.rounded_rectangle([(565, 265), (SIZE - 70, 475)], radius=20, fill=C_CREAM)
    d2.text((787, 285), "KEY SUPPORTS", fill=C_EMERALD, font=_get_font("din_cond", 36), anchor="mt")
    d2.text((787, 335), f"S1: {pivots['s1']:,.0f}", fill=C_DARK, font=_get_font("impact", 40), anchor="mt")
    d2.text((787, 395), f"S2: {pivots['s2']:,.0f}", fill=C_EMERALD, font=_get_font("impact", 40), anchor="mt")

    # Moving Averages Dashboard
    d2.rounded_rectangle([(70, 505), (SIZE - 70, 725)], radius=20, fill=C_WHITE)
    d2.text((SIZE // 2, 525), "MOVING AVERAGE ALIGNMENT", fill=C_MAROON, font=_get_font("din_cond", 34), anchor="mt")
    d2.text((220, 580), f"20 EMA: {mas['ema_20']:,.0f}", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 580), f"50 SMA: {mas['sma_50']:,.0f}", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d2.text((860, 580), f"200 SMA: {mas['sma_200']:,.0f}", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 655), f"Status: {mas['alignment']}", fill=C_EMERALD if "Bullish" in mas['alignment'] else C_MAROON, font=_get_font("din_alt", 24), anchor="mt")

    # RSI Oscillator Bar
    d2.rounded_rectangle([(70, 755), (SIZE - 70, 875)], radius=18, fill=C_AMBER)
    d2.text((SIZE // 2, 780), f"RSI (14-PERIOD): {tech['oscillators']['rsi_14']} • {tech['oscillators']['rsi_status'].upper()}", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 828), "Healthy momentum oscillator without overbought exhaustion", fill=C_DARK, font=_get_font("din_alt", 22), anchor="mt")

    p2 = str(settings.OUTPUT_DIR / f"nifty_pred_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: DERIVATIVES, OPTION CHAIN & SENTIMENT RADAR
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_gradient_bg(C_BLUE_TOP, C_BLUE_BOT)
    add_architectural_silhouettes(img3, (56, 189, 248), 0.15)
    d3 = ImageDraw.Draw(img3)
    draw_header(img3, d3, handle)

    d3.text((SIZE // 2, 105), "DERIVATIVES & PCR RADAR:", fill=C_CREAM, font=_get_font("impact", 70), anchor="mt")
    d3.text((SIZE // 2, 190), "OPTION CHAIN OPEN INTEREST & VOLATILITY", fill=C_AMBER, font=_get_font("din_cond", 48), anchor="mt")

    # Put-Call Ratio Card
    d3.rounded_rectangle([(70, 265), (SIZE - 70, 445)], radius=20, fill=C_CREAM)
    d3.text((SIZE // 2, 290), "NIFTY PUT-CALL RATIO (PCR)", fill=C_MAROON, font=_get_font("din_cond", 36), anchor="mt")
    d3.text((SIZE // 2, 340), f"{derivs['pcr']:.2f} ({derivs['pcr_bias'].upper()})", fill=C_DARK, font=_get_font("impact", 52), anchor="mt")
    d3.text((SIZE // 2, 405), "Signals supportive put writing cushion on lower boundaries", fill=C_MAROON, font=_get_font("body", 22), anchor="mt")

    # Key OI Strike Cards
    d3.rounded_rectangle([(70, 475), (515, 685)], radius=20, fill=C_WHITE)
    d3.text((292, 500), "MAJOR CALL RESISTANCE", fill=C_ROSE, font=_get_font("din_cond", 34), anchor="mt")
    d3.text((292, 555), derivs["key_resistance_strike"], fill=C_DARK, font=_get_font("impact", 36), anchor="mt")
    d3.text((292, 620), "Heavy Call OI Cap", fill=C_MAROON, font=_get_font("body", 22), anchor="mt")

    d3.rounded_rectangle([(565, 475), (SIZE - 70, 685)], radius=20, fill=C_WHITE)
    d3.text((787, 500), "MAJOR PUT SUPPORT", fill=C_EMERALD, font=_get_font("din_cond", 34), anchor="mt")
    d3.text((787, 555), derivs["key_support_strike"], fill=C_DARK, font=_get_font("impact", 36), anchor="mt")
    d3.text((787, 620), "Solid Put Writing Floor", fill=C_MAROON, font=_get_font("body", 22), anchor="mt")

    # Options Strategy Banner
    d3.rounded_rectangle([(70, 715), (SIZE - 70, 875)], radius=18, fill=C_AMBER)
    d3.text((SIZE // 2, 740), "RECOMMENDED OPTIONS STRATEGY", fill=C_DARK, font=_get_font("impact", 32), anchor="mt")
    d3.text((SIZE // 2, 795), pred.get("options_strategy", "Bull Call Spread with defined risk"), fill=C_DARK, font=_get_font("din_cond", 34), anchor="mt")

    p3 = str(settings.OUTPUT_DIR / f"nifty_pred_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: ACTIONABLE TRADE PLAYBOOK (BULL & BEAR TACTICAL PLANS)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_gradient_bg(C_GOLD_TOP, C_GOLD_BOT)
    add_architectural_silhouettes(img4, (254, 240, 138), 0.18)
    d4 = ImageDraw.Draw(img4)
    draw_header(img4, d4, handle)

    # Main Card
    d4.rounded_rectangle([(70, 115), (SIZE - 70, 895)], radius=28, fill=C_CREAM)
    d4.text((SIZE // 2, 140), "TACTICAL TRADE PLAYBOOK:", fill=C_MAROON, font=_get_font("impact", 54), anchor="mt")
    d4.text((SIZE // 2, 210), "ACTIONABLE ENTRY, STOP LOSS & PROFIT TARGETS", fill=C_DARK, font=_get_font("din_cond", 40), anchor="mt")

    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    # Plan A: Bull Setup
    d4.rounded_rectangle([(100, 275), (SIZE - 100, 520)], radius=18, fill=C_WHITE)
    d4.text((130, 295), "PLAN A: BULLISH TRADE SETUP", fill=C_EMERALD, font=_get_font("impact", 32))
    d4.text((130, 345), f"• Trigger: {bull_p.get('trigger', 'Buy on breakout above pivot')}", fill=C_DARK, font=_get_font("body", 22))
    d4.text((130, 385), f"• Stop Loss: {bull_p.get('stop_loss', 'S1 Level')}", fill=C_ROSE, font=_get_font("body", 22))
    d4.text((130, 425), f"• Targets: T1 {bull_p.get('target_1', 'R1')}  |  T2 {bull_p.get('target_2', 'R2')}", fill=C_EMERALD, font=_get_font("body", 22))
    d4.text((130, 465), f"• Risk-to-Reward: {bull_p.get('risk_reward', '1 : 2.5')}", fill=C_MAROON, font=_get_font("body", 22))

    # Plan B: Bear Setup
    d4.rounded_rectangle([(100, 545), (SIZE - 100, 790)], radius=18, fill=C_WHITE)
    d4.text((130, 565), "PLAN B: BEARISH DEFENSE SETUP", fill=C_ROSE, font=_get_font("impact", 32))
    d4.text((130, 615), f"• Trigger: {bear_p.get('trigger', 'Sell on breakdown below S1')}", fill=C_DARK, font=_get_font("body", 22))
    d4.text((130, 655), f"• Stop Loss: {bear_p.get('stop_loss', 'Pivot Level')}", fill=C_ROSE, font=_get_font("body", 22))
    d4.text((130, 695), f"• Targets: T1 {bear_p.get('target_1', 'S2')}  |  T2 {bear_p.get('target_2', 'S3')}", fill=C_DARK, font=_get_font("body", 22))
    d4.text((130, 735), f"• Risk-to-Reward: {bear_p.get('risk_reward', '1 : 2.0')}", fill=C_MAROON, font=_get_font("body", 22))

    # Bottom CTA Banner
    d4.rounded_rectangle([(100, 815), (SIZE - 100, 870)], radius=14, fill=C_AMBER)
    d4.text((SIZE // 2, 842), "SAVE THIS POST FOR TOMORROW'S SESSION • @FINPULSE.DAILY", fill=C_DARK, font=_get_font("impact", 26), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / f"nifty_pred_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
