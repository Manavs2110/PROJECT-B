"""
main.py — FinPulse Microservices Orchestrator & CLI
"""

import sys
import argparse
from common.config import settings

# Microservice Imports
from services.market_data_service import fetch_market_indices, fetch_fii_dii_cash_flows
from services.news_curation_service import fetch_breaking_market_news, fetch_stock_news_24h
from services.technical_analysis_service import compute_nifty_technicals, compute_option_metrics
from services.prediction_service import generate_prediction_model
from services.visual_rendering_service import render_market_impact_carousel, render_prediction_carousel
from services.publishing_service import publish_carousel_to_instagram

def main():
    parser = argparse.ArgumentParser(description="FinPulse Financial Microservices Orchestrator")
    parser.add_argument("--post1", "--generate", action="store_true", help="Generate Post 1: Daily Market Intelligence Carousel")
    parser.add_argument("--post2", "--prediction", action="store_true", help="Generate Post 2: Nifty 50 Prediction & Technical Analysis Carousel")
    parser.add_argument("--publish", action="store_true", help="Publish generated carousel directly to Instagram")
    parser.add_argument("--api", action="store_true", help="Run the Central FastAPI Microservices Gateway")
    parser.add_argument("--port", type=int, default=settings.PORT, help="Port to run the API Gateway on")
    args = parser.parse_args()

    if args.api:
        import uvicorn
        print(f"🚀 Launching FinPulse Microservices Gateway on port {args.port}...")
        uvicorn.run("gateway.app:app", host="0.0.0.0", port=args.port, reload=settings.DEBUG)
        return

    if args.post1:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  FINPULSE POST #1: DAILY MARKET INTELLIGENCE & FLOWS     ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        print("1️⃣ [market_data_service] Fetching live indices & flows...")
        indices = fetch_market_indices()
        fii_dii = fetch_fii_dii_cash_flows()
        print(f"   • NIFTY 50: {indices['nifty']['formatted_price']} ({indices['nifty']['formatted_change']})")
        print(f"   • SENSEX:   {indices['sensex']['formatted_price']} ({indices['sensex']['formatted_change']})")
        print(f"   • FII Net:  {fii_dii['fii']['formatted_net']} | DII Net: {fii_dii['dii']['formatted_net']}")

        print("\n2️⃣ [news_curation_service] Curating market news catalysts...")
        news = fetch_breaking_market_news(limit=5)

        print("\n3️⃣ [visual_rendering_service] Generating 4-Slide Market Impact Carousel...")
        sentiment = {
            "market_mood": "Bullish Momentum" if indices["nifty"]["is_positive"] else "Consolidation",
            "vix_interpretation": f"India VIX at {indices['vix']['price']:.2f} signals calm volatility",
            "sectors": [
                {"sector_name": "Banking & Financials", "impact": "BULLISH", "catalyst": "Private lenders credit growth.", "affected_stocks": ["HDFCBANK", "ICICIBANK", "SBIN"]},
                {"sector_name": "IT & AI", "impact": "BULLISH", "catalyst": "Global enterprise AI momentum.", "affected_stocks": ["TCS", "INFY", "HCLTECH"]},
                {"sector_name": "Energy & Oil", "impact": "BEARISH", "catalyst": "Downstream margin adjustments.", "affected_stocks": ["RELIANCE", "ONGC"]}
            ],
            "tactical_strategy": "Accumulate leading private banks & IT leaders on pullbacks."
        }
        slides = render_market_impact_carousel(indices, fii_dii, sentiment, news)
        print("   ✅ Post #1 Slides generated:")
        for idx, s in enumerate(slides, 1):
            print(f"      [Slide {idx}] {s}")

        if args.publish:
            print("\n4️⃣ [publishing_service] Publishing to Instagram @finpulse.daily...")
            caption = f"🔥 D-Street Daily Intelligence • Nifty: {indices['nifty']['formatted_price']} | Total FII/DII Net: {fii_dii['formatted_total_net']}"
            res = publish_carousel_to_instagram(slides, caption)
            if res.get("success"):
                print(f"   🎉 Published successfully! Post URL: {res.get('post_url')}")
            else:
                print(f"   ❌ Publish failed: {res.get('error')}")
        return

    if args.post2:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  FINPULSE POST #2: NIFTY 50 PREDICTION & TECHNICALS      ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        print("1️⃣ [technical_analysis_service & prediction_service] Running models...")
        model = generate_prediction_model()
        tech = model["technical_data"]
        pred = model["prediction"]
        print(f"   • Nifty Spot:      {tech['formatted_price']}")
        print(f"   • Predicted Trend: {pred.get('predicted_trend')}")
        print(f"   • Target Range:    {pred.get('expected_trading_range')}")
        print(f"   • Probability:     {pred.get('probability_bull_pct')}%")

        print("\n2️⃣ [visual_rendering_service] Generating 4-Slide Prediction Carousel...")
        slides = render_prediction_carousel(model)
        print("   ✅ Post #2 Slides generated:")
        for idx, s in enumerate(slides, 1):
            print(f"      [Slide {idx}] {s}")

        if args.publish:
            print("\n3️⃣ [publishing_service] Publishing to Instagram @finpulse.daily...")
            caption = f"🎯 Nifty 50 Prediction: Targets {pred.get('expected_trading_range')} • Trend: {pred.get('predicted_trend')}"
            res = publish_carousel_to_instagram(slides, caption)
            if res.get("success"):
                print(f"   🎉 Published successfully! Post URL: {res.get('post_url')}")
            else:
                print(f"   ❌ Publish failed: {res.get('error')}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
