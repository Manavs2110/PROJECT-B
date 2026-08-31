"""
services/visual_rendering_service/renderer_prediction.py — Photo-First Editorial NIFTY 50 Prediction Slides
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

def render_prediction_carousel(model: Dict[str, Any]) -> List[str]:
    """Generates 4 modern photo-first editorial slides for Post #2."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slides = []

    tech = model["technical_data"]
    derivs = model["derivatives_data"]
    pred = model["prediction"]
    pivots = tech["pivots"]
    mas = tech["moving_averages"]
    playbook = pred.get("trade_playbook", {})
    is_bull = pred.get("probability_bull_pct", 50) >= 50

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: NIFTY 50 TARGETS (Photo-First: Candlestick Screen)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_photo_editorial_canvas("candlestick_screen.jpg", "NIFTY PREDICTION")
    d1 = ImageDraw.Draw(img1)

    d1.text((50, 645), f"NIFTY 50: {pred.get('predicted_trend', 'BULLISH BREAKOUT')}", fill=TEXT_WHITE, font=get_font("impact", 44))
    d1.text((50, 705), f"Expected Session Range: {pred.get('expected_trading_range', '24,000 — 24,350')} • Spot: {tech['formatted_price']}", fill=ACCENT_AMBER, font=get_font("body", 22))

    draw_stat_pill(d1, (50, 755, 520, 835), "PREDICTED BIAS", f"{pred.get('probability_bull_pct', 65)}% CONFIDENCE", is_bull)
    draw_stat_pill(d1, (560, 755, SIZE - 50, 835), "KEY PIVOT LEVEL", f"{pivots['pivot']:,.2f}", True)

    draw_stat_pill(d1, (50, 855, 520, 935), "EXPECTED RANGE LOW", f"S1: {pivots['s1']:,.0f}", True)
    draw_stat_pill(d1, (560, 855, SIZE - 50, 935), "EXPECTED RANGE HIGH", f"R1: {pivots['r1']:,.0f}", False)

    d1.text((50, 990), "SWIPE FOR TECHNICAL BLUEPRINT & PIVOTS", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d1.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d1.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p1 = str(settings.OUTPUT_DIR / f"nifty_pred_s1_{ts}.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: TECHNICAL BLUEPRINT (Photo-First: Trading Terminal)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_photo_editorial_canvas("trading_desk_charts.jpg", "TECHNICAL LEVELS")
    d2 = ImageDraw.Draw(img2)

    d2.text((50, 645), "NIFTY TECHNICAL BLUEPRINT", fill=TEXT_WHITE, font=get_font("impact", 44))
    d2.text((50, 705), f"Moving Averages: {mas['alignment']} • RSI (14): {tech['oscillators']['rsi_14']}", fill=ACCENT_AMBER, font=get_font("body", 22))

    draw_stat_pill(d2, (50, 755, 520, 835), "RESISTANCE (R1 / R2)", f"{pivots['r1']:,.0f} / {pivots['r2']:,.0f}", False)
    draw_stat_pill(d2, (560, 755, SIZE - 50, 835), "SUPPORT (S1 / S2)", f"{pivots['s1']:,.0f} / {pivots['s2']:,.0f}", True)

    draw_stat_pill(d2, (50, 855, 520, 935), "20 EMA (TREND PIVOT)", f"{mas['ema_20']:,.0f}", True)
    draw_stat_pill(d2, (560, 855, SIZE - 50, 935), "50 SMA / 200 SMA", f"{mas['sma_50']:,.0f} / {mas['sma_200']:,.0f}", True)

    d2.text((50, 990), "SWIPE FOR DERIVATIVES & PCR RADAR", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d2.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d2.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p2 = str(settings.OUTPUT_DIR / f"nifty_pred_s2_{ts}.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: DERIVATIVES & OPTION CHAIN (Photo-First: Financial District)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_photo_editorial_canvas("financial_district.jpg", "DERIVATIVES RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((50, 645), f"OPTION CHAIN & PCR RADAR ({derivs['pcr']:.2f})", fill=TEXT_WHITE, font=get_font("impact", 44))
    d3.text((50, 705), f"Sentiment: {derivs['pcr_bias']} • Max Pain Strike: {derivs['max_pain']}", fill=ACCENT_AMBER, font=get_font("body", 22))

    draw_stat_pill(d3, (50, 755, 520, 845), "CALL CEILING (RESISTANCE)", derivs["key_resistance_strike"], False)
    draw_stat_pill(d3, (560, 755, SIZE - 50, 845), "PUT FLOOR (SUPPORT)", derivs["key_support_strike"], True)

    draw_stat_pill(d3, (50, 865, SIZE - 50, 945), "OPTIONS STRATEGY", pred.get("options_strategy", "Bull Call Spread with defined risk"), True)

    d3.text((50, 990), "SWIPE FOR ACTIONABLE TRADE PLAYBOOK", fill=TEXT_MUTED, font=get_font("din_alt", 22))
    d3.rounded_rectangle([(SIZE - 170, 970), (SIZE - 50, 1015)], radius=20, fill=ACCENT_AMBER)
    d3.text((SIZE - 110, 992), "SWIPE", fill=TEXT_DARK, font=get_font("impact", 20), anchor="mm")

    p3 = str(settings.OUTPUT_DIR / f"nifty_pred_s3_{ts}.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: TRADE PLAYBOOK (Photo-First: Wall Street NYSE)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_photo_editorial_canvas("wall_street_nyse.jpg", "TRADE PLAYBOOK")
    d4 = ImageDraw.Draw(img4)

    d4.text((50, 645), "ACTIONABLE TRADE PLAYBOOK", fill=TEXT_WHITE, font=get_font("impact", 44))
    d4.text((50, 705), "Plan A & Plan B Execution Rules with Defined Risk Management", fill=ACCENT_AMBER, font=get_font("body", 22))

    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    # Plan A Pill
    d4.rounded_rectangle([(50, 750), (SIZE - 50, 835)], radius=12, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    d4.rounded_rectangle([(50, 750), (56, 835)], radius=4, fill=ACCENT_EMERALD)
    d4.text((70, 765), "PLAN A (BULLISH ENTRY):", fill=ACCENT_EMERALD, font=get_font("impact", 24))
    d4.text((70, 798), f"Trigger: {bull_p.get('trigger')} • SL: {bull_p.get('stop_loss')} • Targets: T1 {bull_p.get('target_1')} / T2 {bull_p.get('target_2')}", fill=TEXT_WHITE, font=get_font("body", 19))

    # Plan B Pill
    d4.rounded_rectangle([(50, 855), (SIZE - 50, 940)], radius=12, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    d4.rounded_rectangle([(50, 855), (56, 940)], radius=4, fill=ACCENT_ROSE)
    d4.text((70, 870), "PLAN B (BEARISH DEFENSE):", fill=ACCENT_ROSE, font=get_font("impact", 24))
    d4.text((70, 903), f"Trigger: {bear_p.get('trigger')} • SL: {bear_p.get('stop_loss')} • Target: {bear_p.get('target_1')}", fill=TEXT_WHITE, font=get_font("body", 19))

    d4.text((50, 990), "SAVE THIS POST FOR TOMORROW'S SESSION • @FINPULSE.DAILY", fill=ACCENT_AMBER, font=get_font("impact", 22))

    p4 = str(settings.OUTPUT_DIR / f"nifty_pred_s4_{ts}.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    return slides
