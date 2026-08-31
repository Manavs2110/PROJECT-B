"""
post.py — Daily Market Intelligence Post Generation & Publishing Endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.market_data_service import get_market_indices, get_fii_dii_cash_flows
from services.news_service import get_breaking_market_news
from services.sentiment_service import analyze_market_sentiment
from services.image_service import generate_4slide_carousel
from services.publisher_service import publish_to_instagram

router = APIRouter(prefix="/api/v1/post", tags=["Post Operations"])

class PublishRequest(BaseModel):
    slides: List[str]
    caption: str
    verification_code: Optional[str] = None

@router.post("/generate")
def generate_post():
    """
    1-Click orchestration to fetch live market data, analyze sentiment,
    render the 4 visual slides, and compose the structured AI caption.
    """
    indices = get_market_indices()
    fii_dii = get_fii_dii_cash_flows()
    news = get_breaking_market_news(limit=5)
    sentiment = analyze_market_sentiment(indices, fii_dii, news)
    slides = generate_4slide_carousel(indices, fii_dii, sentiment, news)

    # Caption Assembly
    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]
    hook_main = "TIGHT ROPE ON D-STREET!" if abs(nifty["change_pct"]) < 0.5 else ("BULLS ON RAMPAGE!" if nifty["is_positive"] else "BEARS TAKE CONTROL!")

    caption = f"""🔥 {hook_main} D-Street Daily Intelligence 🚀

📈 1. NIFTY & SENSEX MOVEMENT:
• NIFTY 50: {nifty['formatted_price']} ({nifty['formatted_change']})
• BSE SENSEX: {sensex['formatted_price']} ({sensex['formatted_change']})
• BANK NIFTY: {bank['formatted_price']} ({bank['formatted_change']})
• INDIA VIX: {vix['price']:.2f} ({vix['formatted_change']} — Volatility Cooling)

💰 2. CASH INFLOWS & INSTITUTIONAL PARTICIPATION ({fii_dii['date']}):
• FII / FPI Net Flow: {fii_dii['fii']['formatted_net']} ({fii_dii['fii']['bias']})
• DII (Domestic) Net: {fii_dii['dii']['formatted_net']} ({fii_dii['dii']['bias']})
• Total Institutional Net: {fii_dii['formatted_total_net']} ({fii_dii['sentiment']})
• Retail & Pro: Steady participation with liquidity absorption

🌡️ 3. MARKET SENTIMENTS & SECTOR RADAR:
• Market Sentiment: {sentiment.get('market_mood', 'BULLISH')}
• Tactical Strategy: {sentiment.get('tactical_strategy', '')}
"""
    for s in sentiment.get("sectors", []):
        icon = "🟢" if s["impact"] == "BULLISH" else "🔴"
        caption += f"\n{icon} {s['sector_name'].upper()} ({s['impact']})\n"
        caption += f"• Catalyst: {s['catalyst']}\n"
        caption += f"• Tickers: {', '.join(s.get('affected_stocks', [])[:4])}\n"

    caption += "\n📰 4. MAJOR BREAKING NEWS & SOURCES:\n"
    for idx, art in enumerate(news[:3], 1):
        caption += f"{idx}️⃣ {art.get('title')}\n"
        caption += f"   • Source: {art.get('source_name')}\n"
        caption += f"   • Link: {art.get('url')}\n"

    caption += "\n💬 What is your view for the next trading session? Drop your target below! 👇\n\n#Nifty #Sensex #StockMarket #FIIDII #FinPulse #Trading"

    return {
        "success": True,
        "slide_count": len(slides),
        "slides": slides,
        "caption": caption,
        "indices": indices,
        "fii_dii": fii_dii,
        "sentiment": sentiment
    }

@router.post("/publish")
def publish_post(req: PublishRequest):
    """Publishes the generated 4-slide carousel to Instagram."""
    res = publish_to_instagram(req.slides, req.caption, req.verification_code)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res)
    return res
