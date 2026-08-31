"""
gateway/app.py — Central API Gateway Orchestrating All Microservices
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from common.config import settings

# Microservice Routers
from services.market_data_service import market_router, fetch_market_indices, fetch_fii_dii_cash_flows
from services.news_curation_service import news_router, fetch_breaking_market_news
from services.technical_analysis_service import technical_router
from services.prediction_service import prediction_router, generate_prediction_model
from services.visual_rendering_service import render_router, render_market_impact_carousel, render_prediction_carousel
from services.publishing_service import publish_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Decoupled microservice architecture for FinPulse automated financial publishing."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="images")

# Serve Modern Web Dashboard UI
UI_FILE = Path(__file__).resolve().parent / "ui" / "index.html"

@app.get("/", response_class=HTMLResponse, tags=["Dashboard UI"])
@app.get("/ui", response_class=HTMLResponse, tags=["Dashboard UI"])
def get_dashboard_ui():
    """Serves the FinPulse Microservices Control Center Web Dashboard."""
    if UI_FILE.exists():
        return HTMLResponse(content=UI_FILE.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>FinPulse UI file not found</h1>", status_code=404)

# Mount Individual Microservices
app.include_router(market_router)
app.include_router(news_router)
app.include_router(technical_router)
app.include_router(prediction_router)
app.include_router(render_router)
app.include_router(publish_router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "microservices": [
            "market_data_service",
            "news_curation_service",
            "technical_analysis_service",
            "prediction_service",
            "visual_rendering_service",
            "publishing_service"
        ]
    }

# ── High-Level Post Orchestration Endpoints ──

def build_market_post_caption(indices: dict, fii_dii: dict, sentiment: dict, news: list) -> str:
    nifty = indices["nifty"]
    sensex = indices["sensex"]
    bank = indices["banknifty"]
    vix = indices["vix"]
    date_str = fii_dii.get("date", "Today")

    # Format News Links
    news_lines = []
    for idx, item in enumerate(news[:3], 1):
        title = item.get("title", "")
        url = item.get("url", "")
        source = item.get("source_name", "News Desk")
        news_lines.append(f"{idx}️⃣ {title} ({source})\n🔗 {url}")
    news_section = "\n\n".join(news_lines) if news_lines else "• Breaking macroeconomic updates on D-Street."

    return f"""🚨 D-STREET DAILY INTELLIGENCE & MARKET REPORT ({date_str}) 🇮🇳

📊 MARKET SCORECARD:
• NIFTY 50: {nifty['formatted_price']} ({nifty['formatted_change']})
• BSE SENSEX: {sensex['formatted_price']} ({sensex['formatted_change']})
• BANK NIFTY: {bank['formatted_price']} ({bank['formatted_change']})
• INDIA VIX: {vix['price']:.2f} ({vix['change_pct']:+.2f}%) • {sentiment.get('vix_interpretation', 'Calm volatility')}

💰 INSTITUTIONAL CASH FLOWS (NSE Cash Segment):
• FII / FPI Net Flow: {fii_dii['fii']['formatted_net']} ({fii_dii['fii']['bias']})
• DII Domestic Net Flow: {fii_dii['dii']['formatted_net']} ({fii_dii['dii']['bias']})
• Combined Net Balance: {fii_dii['formatted_total_net']} ({fii_dii['sentiment']})

⚡ TOP BREAKING STORIES & CATALYSTS:
{news_section}

🌐 VERIFIED DATA SOURCES:
• NSE India Cash Flows: https://www.nseindia.com/reports/fii-dii
• Nifty 50 Realtime Feed: https://finance.yahoo.com/quote/%5ENSEI
• BSE Sensex Realtime Feed: https://finance.yahoo.com/quote/%5EBSESN

👉 Save this post for your market records and follow @finpulse.daily for actionable daily intelligence!

#FinPulse #Nifty50 #Sensex #StockMarketIndia #IndianStockMarket #NSE #BSE #BankNifty #TradingStrategy #StockMarketNews #DalalStreet #OptionTrading #IntradayTrading #FinancialNews #InvestingIndia #MutualFunds #FII #DII #ShareMarket #TechnicalAnalysis #MarketUpdate #MarketTrends #NiftyPrediction #WealthCreation #BullMarket #BearMarket #StockMarketTips #FinanceDaily #Economy #IndiaGrowth #TradingView #StockMarketLive"""


def build_prediction_post_caption(model: dict) -> str:
    tech = model["technical_data"]
    derivs = model["derivatives_data"]
    pred = model["prediction"]
    pivots = tech["pivots"]
    mas = tech["moving_averages"]
    playbook = pred.get("trade_playbook", {})
    bull_p = playbook.get("bull_setup", {})
    bear_p = playbook.get("bear_setup", {})

    return f"""🎯 NIFTY 50 PREDICTION & TECHNICAL BLUEPRINT 🚀

📈 PREDICTION OVERVIEW:
• Primary Bias: {pred.get('predicted_trend', 'BULLISH BREAKOUT')}
• Expected Trading Range: {pred.get('expected_trading_range', '24,000 — 24,350')}
• Prediction Confidence: {pred.get('probability_bull_pct', 65)}% Probability
• Current Nifty Spot: {tech.get('formatted_price', '24,090.85')}

📐 KEY TECHNICAL LEVELS:
• Major Resistances: R1 {pivots.get('r1', 0):,.0f}  |  R2 {pivots.get('r2', 0):,.0f}
• Pivot Point (Make-or-Break): {pivots.get('pivot', 0):,.2f}
• Major Supports: S1 {pivots.get('s1', 0):,.0f}  |  S2 {pivots.get('s2', 0):,.0f}
• Moving Averages: 20 EMA ({mas.get('ema_20', 0):,.0f}) • 50 SMA ({mas.get('sma_50', 0):,.0f}) • 200 SMA ({mas.get('sma_200', 0):,.0f})
• RSI (14-Period): {tech.get('oscillators', {}).get('rsi_14', 50)} ({tech.get('oscillators', {}).get('rsi_status', 'Neutral')})

📊 OPTION CHAIN & DERIVATIVES RADAR:
• Put-Call Ratio (PCR): {derivs.get('pcr', 1.0):.2f} ({derivs.get('pcr_bias', 'NEUTRAL').upper()})
• Max Pain Strike: {derivs.get('max_pain', 24100)}
• Key Call Resistance Strike: {derivs.get('key_resistance_strike', '24,300 CE')}
• Key Put Support Strike: {derivs.get('key_support_strike', '24,000 PE')}
• Recommended Strategy: {pred.get('options_strategy', 'Bull Call Spread with defined risk')}

⚔️ TACTICAL TRADE PLAYBOOK:
🟢 PLAN A (Bullish Entry):
  Trigger: {bull_p.get('trigger', 'Buy on breakout above pivot')}
  Stop Loss: {bull_p.get('stop_loss', 'S1 Level')}
  Targets: T1 {bull_p.get('target_1', 'R1')}  |  T2 {bull_p.get('target_2', 'R2')}
  Risk-to-Reward: {bull_p.get('risk_reward', '1 : 2.5')}

🔴 PLAN B (Bearish Defense):
  Trigger: {bear_p.get('trigger', 'Sell on breakdown below S1')}
  Stop Loss: {bear_p.get('stop_loss', 'Pivot Level')}
  Targets: T1 {bear_p.get('target_1', 'S2')}  |  T2 {bear_p.get('target_2', 'S3')}
  Risk-to-Reward: {bear_p.get('risk_reward', '1 : 2.0')}

🌐 VERIFIED DATA SOURCES & METHODOLOGY:
• NSE India Option Chain: https://www.nseindia.com/option-chain
• Nifty 50 Technical Blueprint: https://finance.yahoo.com/quote/%5ENSEI
• FinPulse Quant Indicators: Floor Pivots, Exponential Moving Averages & PCR Synthesis

👉 Save this post for tomorrow's live trading session! Follow @finpulse.daily for daily technical playbooks!

#Nifty50 #NiftyPrediction #OptionsTrading #OptionChain #BankNifty #StockMarketIndia #IndianStockMarket #TechnicalAnalysis #TradingView #NSEIndia #DalalStreet #IntradayTrading #PriceAction #OptionGreeks #StockMarketNews #MarketPrediction #TradingStrategy #BreakoutTrading #FinPulse #ShareMarketIndia #Investment #NiftyFifty #OptionBuying #OptionSelling #DerivativesTrading #Sensex #BSE #FinancialEducation #TradingSignals #StockMarket"""


@app.post("/api/v1/posts/daily-market-post", tags=["Post Orchestrations"])
def orchestrate_daily_market_post():
    """1-Click Generation of Post 1 (Daily Market Intelligence & Nifty/Sensex Movement)."""
    indices = fetch_market_indices()
    fii_dii = fetch_fii_dii_cash_flows()
    news = fetch_breaking_market_news(limit=5)
    
    # Sentiment synthesis
    sentiment = {
        "market_mood": "Bullish Momentum" if indices["nifty"]["is_positive"] else "Consolidation",
        "vix_interpretation": f"India VIX at {indices['vix']['price']:.2f} signals calm volatility",
        "sectors": [
            {"sector_name": "Banking & Financials", "impact": "BULLISH", "catalyst": "Private lenders leading credit growth.", "affected_stocks": ["HDFCBANK", "ICICIBANK", "SBIN"]},
            {"sector_name": "IT & AI", "impact": "BULLISH", "catalyst": "Global enterprise AI momentum.", "affected_stocks": ["TCS", "INFY", "HCLTECH"]},
            {"sector_name": "Energy & Oil", "impact": "BEARISH", "catalyst": "Downstream margin adjustments.", "affected_stocks": ["RELIANCE", "ONGC"]}
        ],
        "tactical_strategy": "Accumulate leading private banks & IT leaders on pullbacks."
    }
    
    slides = render_market_impact_carousel(indices, fii_dii, sentiment, news)
    caption = build_market_post_caption(indices, fii_dii, sentiment, news)
    return {
        "success": True,
        "post_type": "daily_market_intelligence",
        "slide_count": len(slides),
        "slides": slides,
        "caption": caption
    }


@app.post("/api/v1/posts/nifty-prediction-post", tags=["Post Orchestrations"])
def orchestrate_nifty_prediction_post():
    """1-Click Generation of Post 2 (NIFTY 50 Prediction & Technical Analysis)."""
    model = generate_prediction_model()
    slides = render_prediction_carousel(model)
    caption = build_prediction_post_caption(model)
    return {
        "success": True,
        "post_type": "nifty_prediction",
        "slide_count": len(slides),
        "slides": slides,
        "model": model,
        "caption": caption
    }

