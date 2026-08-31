#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../")))

from services import fetch_nifty_technical_data, generate_nifty_prediction_model, generate_nifty_prediction_carousel

def run():
    print("⚡ Fetching Nifty 50 technical data...")
    tech = fetch_nifty_technical_data()
    print(f"   • Spot: {tech['formatted_price']}")
    print(f"   • S1: {tech['pivots']['s1']} | R1: {tech['pivots']['r1']} | Pivot: {tech['pivots']['pivot']}")
    print(f"   • 20 EMA: {tech['moving_averages']['ema_20']} | RSI: {tech['oscillators']['rsi_14']}")

    print("\n🧠 Formulating hybrid prediction model...")
    model = generate_nifty_prediction_model()
    pred = model["prediction"]
    print(f"   • Trend: {pred.get('predicted_trend')}")
    print(f"   • Range: {pred.get('expected_trading_range')}")
    print(f"   • Bull Confidence: {pred.get('probability_bull_pct')}%")

    print("\n🎨 Generating 4-Slide Prediction Visual Carousel...")
    slides = generate_nifty_prediction_carousel(model)
    print(f"   ✅ Generated {len(slides)} slides:")
    for s in slides:
        print(f"      🖼️ {s}")

if __name__ == "__main__":
    run()
