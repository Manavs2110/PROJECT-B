"""
services/visual_rendering_service/renderer_prediction.py — Full-Canvas Randomized NIFTY 50 Prediction Slides (Post #2)
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

def render_prediction_carousel(model: Dict[str, Any]) -> List[str]:
    """Generates 4 full-canvas photographic prediction slides with randomized backgrounds and clean overwrite."""
    slides = []
    
    # 4 distinct random background photos
    photos = get_random_background_photos(4)

    tech = model["technical_data"]
    derivs = model["derivatives_data"]
    pred = model["prediction"]
    pivots = tech["pivots"]
    mas = tech["moving_averages"]
    playbook = pred.get("trade_playbook", {})
    is_bull = pred.get("probability_bull_pct", 50) >= 50

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: NIFTY 50 PREDICTION (Random Background #1)
    # ═════════════════════════════════════════════════════════════════════════
    img1 = create_full_background_canvas(photos[0] if len(photos) > 0 else None, "NIFTY PREDICTION")
    d1 = ImageDraw.Draw(img1)

    d1.text((SIZE // 2, 115), "NIFTY 50 PREDICTION:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d1.text((SIZE // 2, 195), "TOMORROW'S TARGETS & EXPECTED RANGE", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    # Center Hero Glass Card
    draw_glass_panel(img1, (50, 255, SIZE - 50, 615), radius=24, bg=(15, 23, 42, 225), border=BORDER_AMBER)
    d1.text((SIZE // 2, 285), "PRIMARY PREDICTED BIAS", fill=TEXT_MUTED, font=get_font("din_cond", 34), anchor="mt")
    d1.text((SIZE // 2, 335), pred.get("predicted_trend", "BULLISH BREAKOUT"), fill=TEXT_WHITE, font=get_font("impact", 48), anchor="mt")

    prob_col = ACCENT_EMERALD if is_bull else ACCENT_ROSE
    d1.rounded_rectangle([(SIZE // 2 - 170, 415), (SIZE // 2 + 170, 465)], radius=18, fill=prob_col)
    d1.text((SIZE // 2, 440), f"CONFIDENCE: {pred.get('probability_bull_pct', 65)}% PROBABILITY", fill=TEXT_WHITE, font=get_font("din_alt", 22), anchor="mm")

    d1.line([(100, 495), (SIZE - 100, 495)], fill=(51, 65, 85), width=2)
    d1.text((SIZE // 2, 515), "EXPECTED SESSION RANGE", fill=TEXT_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((SIZE // 2, 555), pred.get("expected_trading_range", "24,000 — 24,350"), fill=ACCENT_AMBER, font=get_font("impact", 52), anchor="mt")

    # Lower Glass Pivot Card
    draw_glass_panel(img1, (50, 645, SIZE - 50, 795), radius=20, bg=(10, 15, 28, 230), border=BORDER_GLASS)
    d1.text((285, 675), "KEY MAKE-OR-BREAK PIVOT", fill=TEXT_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((285, 720), f"{pivots['pivot']:,.2f}", fill=ACCENT_AMBER, font=get_font("impact", 40), anchor="mt")
    
    d1.line([(SIZE // 2, 665), (SIZE // 2, 775)], fill=(51, 65, 85), width=2)
    
    d1.text((795, 675), "CURRENT SPOT PRICE", fill=TEXT_MUTED, font=get_font("din_cond", 30), anchor="mt")
    d1.text((795, 720), tech["formatted_price"], fill=TEXT_WHITE, font=get_font("impact", 40), anchor="mt")

    draw_glass_panel(img1, (50, 825, SIZE - 50, 915), radius=16, bg=(245, 158, 11, 235), border=BORDER_AMBER)
    d1.text((SIZE // 2, 870), "SWIPE FOR TECHNICAL BLUEPRINT & TRADE PLAYBOOK", fill=TEXT_DARK, font=get_font("impact", 28), anchor="mm")

    d1.text((SIZE // 2, 975), "FINPULSE PREDICTIVE ANALYTICS • FOLLOW @FINPULSE.DAILY", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p1 = str(settings.OUTPUT_DIR / "nifty_pred_slide_1.jpg")
    img1.save(p1, "JPEG", quality=95)
    slides.append(p1)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: TECHNICAL BLUEPRINT (Random Background #2)
    # ═════════════════════════════════════════════════════════════════════════
    img2 = create_full_background_canvas(photos[1] if len(photos) > 1 else None, "TECHNICAL LEVELS")
    d2 = ImageDraw.Draw(img2)

    d2.text((SIZE // 2, 115), "TECHNICAL BLUEPRINT:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d2.text((SIZE // 2, 195), "KEY SUPPORTS, RESISTANCES & MOVING AVERAGES", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    draw_glass_panel(img2, (50, 255, 520, 475), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d2.text((285, 280), "KEY RESISTANCES", fill=ACCENT_ROSE, font=get_font("din_cond", 36), anchor="mt")
    d2.text((285, 330), f"R1: {pivots['r1']:,.0f}", fill=TEXT_WHITE, font=get_font("impact", 42), anchor="mt")
    d2.text((285, 390), f"R2: {pivots['r2']:,.0f}", fill=ACCENT_ROSE, font=get_font("impact", 42), anchor="mt")

    draw_glass_panel(img2, (560, 255, SIZE - 50, 475), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d2.text((795, 280), "KEY SUPPORTS", fill=ACCENT_EMERALD, font=get_font("din_cond", 36), anchor="mt")
    d2.text((795, 330), f"S1: {pivots['s1']:,.0f}", fill=TEXT_WHITE, font=get_font("impact", 42), anchor="mt")
    d2.text((795, 390), f"S2: {pivots['s2']:,.0f}", fill=ACCENT_EMERALD, font=get_font("impact", 42), anchor="mt")

    draw_glass_panel(img2, (50, 505, SIZE - 50, 725), radius=22, bg=(10, 15, 28, 235), border=BORDER_GLASS)
    d2.text((SIZE // 2, 525), "MOVING AVERAGE ALIGNMENT", fill=ACCENT_AMBER, font=get_font("din_cond", 34), anchor="mt")
    d2.text((220, 580), f"20 EMA: {mas['ema_20']:,.0f}", fill=TEXT_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 580), f"50 SMA: {mas['sma_50']:,.0f}", fill=TEXT_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((860, 580), f"200 SMA: {mas['sma_200']:,.0f}", fill=TEXT_WHITE, font=get_font("impact", 32), anchor="mt")
    d2.text((SIZE // 2, 655), f"Status: {mas['alignment']}", fill=ACCENT_EMERALD if "Bullish" in mas['alignment'] else ACCENT_ROSE, font=get_font("din_alt", 24), anchor="mt")

    draw_glass_panel(img2, (50, 755, SIZE - 50, 875), radius=18, bg=(15, 23, 42, 215), border=BORDER_GLASS)
    d2.text((SIZE // 2, 780), f"RSI (14-PERIOD): {tech['oscillators']['rsi_14']} • {tech['oscillators']['rsi_status'].upper()}", fill=TEXT_WHITE, font=get_font("impact", 30), anchor="mt")
    d2.text((SIZE // 2, 825), "Healthy momentum oscillator without overbought exhaustion", fill=TEXT_MUTED, font=get_font("body", 22), anchor="mt")

    d2.text((SIZE // 2, 975), "SWIPE FOR DERIVATIVES & PCR RADAR", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p2 = str(settings.OUTPUT_DIR / "nifty_pred_slide_2.jpg")
    img2.save(p2, "JPEG", quality=95)
    slides.append(p2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: DERIVATIVES & PCR RADAR (Random Background #3)
    # ═════════════════════════════════════════════════════════════════════════
    img3 = create_full_background_canvas(photos[2] if len(photos) > 2 else None, "DERIVATIVES RADAR")
    d3 = ImageDraw.Draw(img3)

    d3.text((SIZE // 2, 115), "DERIVATIVES & PCR RADAR:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d3.text((SIZE // 2, 195), "OPTION CHAIN OPEN INTEREST & VOLATILITY", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    draw_glass_panel(img3, (50, 255, SIZE - 50, 445), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d3.text((SIZE // 2, 280), "NIFTY PUT-CALL RATIO (PCR)", fill=TEXT_MUTED, font=get_font("din_cond", 36), anchor="mt")
    d3.text((SIZE // 2, 330), f"{derivs['pcr']:.2f} ({derivs['pcr_bias'].upper()})", fill=TEXT_WHITE, font=get_font("impact", 54), anchor="mt")
    d3.text((SIZE // 2, 395), "Signals supportive put writing cushion on lower strike boundaries", fill=ACCENT_AMBER, font=get_font("body", 22), anchor="mt")

    draw_glass_panel(img3, (50, 475, 520, 685), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d3.text((285, 500), "MAJOR CALL RESISTANCE", fill=ACCENT_ROSE, font=get_font("din_cond", 34), anchor="mt")
    d3.text((285, 555), derivs["key_resistance_strike"], fill=TEXT_WHITE, font=get_font("impact", 38), anchor="mt")
    d3.text((285, 620), "Heavy Call OI Cap", fill=TEXT_MUTED, font=get_font("body", 22), anchor="mt")

    draw_glass_panel(img3, (560, 475, SIZE - 50, 685), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d3.text((795, 500), "MAJOR PUT SUPPORT", fill=ACCENT_EMERALD, font=get_font("din_cond", 34), anchor="mt")
    d3.text((795, 555), derivs["key_support_strike"], fill=TEXT_WHITE, font=get_font("impact", 38), anchor="mt")
    d3.text((795, 620), "Solid Put Writing Floor", fill=TEXT_MUTED, font=get_font("body", 22), anchor="mt")

    draw_glass_panel(img3, (50, 715, SIZE - 50, 875), radius=18, bg=(245, 158, 11, 235), border=BORDER_AMBER)
    d3.text((SIZE // 2, 740), "RECOMMENDED OPTIONS STRATEGY", fill=TEXT_DARK, font=get_font("impact", 32), anchor="mt")
    d3.text((SIZE // 2, 795), pred.get("options_strategy", "Bull Call Spread with defined risk"), fill=TEXT_DARK, font=get_font("din_cond", 36), anchor="mt")

    d3.text((SIZE // 2, 975), "SWIPE FOR ACTIONABLE TRADE PLAYBOOK", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p3 = str(settings.OUTPUT_DIR / "nifty_pred_slide_3.jpg")
    img3.save(p3, "JPEG", quality=95)
    slides.append(p3)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: ACTIONABLE TRADE PLAYBOOK (Random Background #4)
    # ═════════════════════════════════════════════════════════════════════════
    img4 = create_full_background_canvas(photos[3] if len(photos) > 3 else None, "TRADE PLAYBOOK")
    d4 = ImageDraw.Draw(img4)

    d4.text((SIZE // 2, 115), "TACTICAL TRADE PLAYBOOK:", fill=TEXT_WHITE, font=get_font("impact", 68), anchor="mt")
    d4.text((SIZE // 2, 195), "ACTIONABLE ENTRY, STOP LOSS & PROFIT TARGETS", fill=ACCENT_AMBER, font=get_font("din_cond", 42), anchor="mt")

    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    draw_glass_panel(img4, (50, 255, SIZE - 50, 515), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d4.text((80, 275), "PLAN A: BULLISH TRADE SETUP", fill=ACCENT_EMERALD, font=get_font("impact", 32))
    d4.text((80, 325), f"• Trigger: {bull_p.get('trigger', 'Buy on breakout above pivot')}", fill=TEXT_WHITE, font=get_font("body", 22))
    d4.text((80, 365), f"• Stop Loss: {bull_p.get('stop_loss', 'S1 Level')}", fill=ACCENT_ROSE, font=get_font("body", 22))
    d4.text((80, 405), f"• Targets: T1 {bull_p.get('target_1', 'R1')}  |  T2 {bull_p.get('target_2', 'R2')}", fill=ACCENT_EMERALD, font=get_font("body", 22))
    d4.text((80, 445), f"• Risk-to-Reward: {bull_p.get('risk_reward', '1 : 2.5')}", fill=ACCENT_AMBER, font=get_font("body", 22))

    draw_glass_panel(img4, (50, 545, SIZE - 50, 805), radius=22, bg=(15, 23, 42, 225), border=BORDER_GLASS)
    d4.text((80, 565), "PLAN B: BEARISH DEFENSE SETUP", fill=ACCENT_ROSE, font=get_font("impact", 32))
    d4.text((80, 615), f"• Trigger: {bear_p.get('trigger', 'Sell on breakdown below S1')}", fill=TEXT_WHITE, font=get_font("body", 22))
    d4.text((80, 655), f"• Stop Loss: {bear_p.get('stop_loss', 'Pivot Level')}", fill=ACCENT_ROSE, font=get_font("body", 22))
    d4.text((80, 695), f"• Targets: T1 {bear_p.get('target_1', 'S2')}  |  T2 {bear_p.get('target_2', 'S3')}", fill=TEXT_WHITE, font=get_font("body", 22))
    d4.text((80, 735), f"• Risk-to-Reward: {bear_p.get('risk_reward', '1 : 2.0')}", fill=ACCENT_AMBER, font=get_font("body", 22))

    draw_glass_panel(img4, (50, 835, SIZE - 50, 915), radius=16, bg=(245, 158, 11, 235), border=BORDER_AMBER)
    d4.text((SIZE // 2, 875), "SAVE THIS POST FOR TOMORROW'S SESSION • @FINPULSE.DAILY", fill=TEXT_DARK, font=get_font("impact", 28), anchor="mm")

    d4.text((SIZE // 2, 975), "FINPULSE DAILY INTELLIGENCE • ALL RIGHTS RESERVED", fill=TEXT_MUTED, font=get_font("din_alt", 20), anchor="mm")

    p4 = str(settings.OUTPUT_DIR / "nifty_pred_slide_4.jpg")
    img4.save(p4, "JPEG", quality=95)
    slides.append(p4)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 5: ENGAGEMENT & DISCUSSION CTA
    # ═════════════════════════════════════════════════════════════════════════
    cta_src = settings.ASSETS_DIR / "templates" / "engagement_slide_5.jpg"
    p5 = str(settings.OUTPUT_DIR / "nifty_pred_slide_5.jpg")
    if cta_src.exists():
        try:
            cta_img = Image.open(cta_src).convert("RGB")
            cta_img.save(p5, "JPEG", quality=98)
            slides.append(p5)
        except Exception as e:
            print(f"⚠️ Error attaching 5th slide: {e}")

    return slides
