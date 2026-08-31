#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../")))

from services import get_market_indices, get_fii_dii_cash_flows, get_breaking_market_news, analyze_market_sentiment, generate_4slide_carousel, publish_to_instagram

def run():
    print("⚡ Fetching live market indices...")
    indices = get_market_indices()
    print(f"   • Nifty 50: {indices['nifty']['formatted_price']} ({indices['nifty']['formatted_change']})")
    print(f"   • Sensex:   {indices['sensex']['formatted_price']} ({indices['sensex']['formatted_change']})")

    print("\n💰 Fetching official NSE FII/DII cash flows...")
    fii_dii = get_fii_dii_cash_flows()
    print(f"   • FII Net:  {fii_dii['fii']['formatted_net']}")
    print(f"   • DII Net:  {fii_dii['dii']['formatted_net']}")
    print(f"   • Total:    {fii_dii['formatted_total_net']}")

    print("\n📰 Curating breaking market news...")
    news = get_breaking_market_news(limit=5)
    for n in news[:3]:
        print(f"   • {n['title']} ({n['source_name']})")

    print("\n🧠 Analyzing sentiment with AI...")
    sentiment = analyze_market_sentiment(indices, fii_dii, news)
    print(f"   • Mood: {sentiment.get('market_mood')}")
    print(f"   • Strategy: {sentiment.get('tactical_strategy')}")

    print("\n🎨 Generating 4-Slide visual carousel...")
    slides = generate_4slide_carousel(indices, fii_dii, sentiment, news)
    print(f"   ✅ Generated {len(slides)} slides:")
    for s in slides:
        print(f"      🖼️ {s}")

if __name__ == "__main__":
    run()
