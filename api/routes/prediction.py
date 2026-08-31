"""
prediction.py — Nifty 50 Technical & Sentimental Prediction Endpoints
"""

from fastapi import APIRouter
from services.technical_analysis_service import fetch_nifty_technical_data
from services.nifty_prediction_service import generate_nifty_prediction_model
from services.prediction_image_service import generate_nifty_prediction_carousel

router = APIRouter(prefix="/api/v1/prediction", tags=["Nifty 50 Prediction"])

@router.get("/technical")
def get_technical_indicators():
    """Returns calculated technical indicators (Pivots, RSI, 20 EMA, 50 SMA, 200 SMA) for Nifty 50."""
    return fetch_nifty_technical_data()

@router.get("/model")
def get_prediction_model():
    """Returns the full Nifty 50 prediction model with probability, derivatives & trade plan."""
    return generate_nifty_prediction_model()

@router.post("/generate-post")
def generate_prediction_post():
    """1-Click generation of the 4-slide NIFTY 50 Prediction carousel and structured caption."""
    model = generate_nifty_prediction_model()
    slides = generate_nifty_prediction_carousel(model)

    tech = model["technical_data"]
    derivs = model["derivatives_data"]
    pred = model["prediction"]
    playbook = pred.get("trade_playbook", {})
    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    caption = f"""🎯 NIFTY 50 PREDICTION: TOMORROW'S TARGETS & LEVELS 🚀

🔮 1. PREDICTED BIAS & TARGET RANGE:
• Predicted Trend: {pred.get('predicted_trend', 'BULLISH ACCUMULATION')}
• Expected Trading Range: {pred.get('expected_trading_range', '24,000 — 24,350')}
• Confidence Probability: {pred.get('probability_bull_pct', 65)}%
• Key Make-or-Break Pivot: {tech['pivots']['pivot']:,.2f}

📊 2. TECHNICAL BLUEPRINT (SUPPORTS & RESISTANCES):
• Resistance R1: {tech['pivots']['r1']:,.0f} | R2: {tech['pivots']['r2']:,.0f}
• Support S1: {tech['pivots']['s1']:,.0f} | S2: {tech['pivots']['s2']:,.0f}
• 20 EMA: {tech['moving_averages']['ema_20']:,.0f} (Key Trend Decider)
• 50 SMA: {tech['moving_averages']['sma_50']:,.0f} | 200 SMA: {tech['moving_averages']['sma_200']:,.0f}
• RSI (14): {tech['oscillators']['rsi_14']} ({tech['oscillators']['rsi_status']})

⚡ 3. DERIVATIVES & PCR RADAR:
• Put-Call Ratio (PCR): {derivs['pcr']:.2f} ({derivs['pcr_bias']})
• Max Pain Strike: {derivs['max_pain']}
• Key Put Floor: {derivs['key_support_strike']}
• Major Call Ceiling: {derivs['key_resistance_strike']}

🎯 4. TACTICAL ACTION PLAYBOOK:
🟢 PLAN A (BULLISH ENTRY):
• Trigger: {bull_p.get('trigger')}
• Stop Loss: {bull_p.get('stop_loss')}
• Targets: T1 {bull_p.get('target_1')} | T2 {bull_p.get('target_2')}
• Risk-to-Reward: {bull_p.get('risk_reward')}

🔴 PLAN B (BEARISH DEFENSE):
• Trigger: {bear_p.get('trigger')}
• Stop Loss: {bear_p.get('stop_loss')}
• Targets: T1 {bear_p.get('target_1')} | T2 {bear_p.get('target_2')}

💡 OPTIONS STRATEGY:
{pred.get('options_strategy')}

⚠️ Disclaimer: Educational market analysis, not SEBI registered financial advice. Trade with strict risk management!

💬 What is your prediction for Nifty tomorrow? Drop your target below! 👇

#Nifty50 #NiftyPrediction #TechnicalAnalysis #OptionChain #StockMarketIndia #FinPulse #TradingStrategy"""

    return {
        "success": True,
        "slide_count": len(slides),
        "slides": slides,
        "caption": caption,
        "model": model
    }
