"""
main.py — Production Entrypoint for FinPulse Microservices & CLI
"""

import sys
import argparse
from config.settings import settings
from services import (
    get_market_indices, get_fii_dii_cash_flows,
    get_breaking_market_news, analyze_market_sentiment,
    generate_4slide_carousel, publish_to_instagram
)

def main():
    parser = argparse.ArgumentParser(description="FinPulse Daily Market Intelligence Microservices")
    parser.add_argument("--generate", action="store_true", help="Generate the 4-slide carousel & caption")
    parser.add_argument("--publish", action="store_true", help="Generate and publish directly to Instagram")
    parser.add_argument("--api", action="store_true", help="Run the FastAPI REST microservice gateway")
    parser.add_argument("--port", type=int, default=settings.PORT, help="Port to run the API on")
    args = parser.parse_args()

    if args.api:
        import uvicorn
        print(f"🚀 Launching FinPulse REST API on port {args.port}...")
        uvicorn.run("api.app:app", host="0.0.0.0", port=args.port, reload=settings.DEBUG)
        return

    if args.generate or args.publish:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  FINPULSE DAILY MARKET INTELLIGENCE (1ST POST GENERATOR) ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        print("1️⃣ Fetching market indices & cash flows...")
        indices = get_market_indices()
        fii_dii = get_fii_dii_cash_flows()
        print(f"   • NIFTY 50: {indices['nifty']['formatted_price']} ({indices['nifty']['formatted_change']})")
        print(f"   • SENSEX:   {indices['sensex']['formatted_price']} ({indices['sensex']['formatted_change']})")
        print(f"   • FII Net:  {fii_dii['fii']['formatted_net']} | DII Net: {fii_dii['dii']['formatted_net']}")
        
        print("\n2️⃣ Curating breaking market news...")
        news = get_breaking_market_news(limit=5)
        
        print("\n3️⃣ Analyzing sentiment & sector matrices...")
        sentiment = analyze_market_sentiment(indices, fii_dii, news)
        print(f"   • Sentiment Bias: {sentiment.get('market_mood')}")
        
        print("\n4️⃣ Rendering 4-Slide visual carousel...")
        slides = generate_4slide_carousel(indices, fii_dii, sentiment, news)
        print("   ✅ Slides generated:")
        for idx, s in enumerate(slides, 1):
            print(f"      [Slide {idx}] {s}")
            
        if args.publish:
            print("\n5️⃣ Publishing to Instagram @finpulse.daily...")
            caption = f"🔥 D-Street Daily Intelligence • Nifty: {indices['nifty']['formatted_price']} | Total FII/DII Net: {fii_dii['formatted_total_net']}"
            res = publish_to_instagram(slides, caption)
            if res.get("success"):
                print(f"   🎉 Published successfully! Post URL: {res.get('post_url')}")
            else:
                print(f"   ❌ Publish failed: {res.get('error')}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
