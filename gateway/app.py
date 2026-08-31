"""
gateway/app.py — Central API Gateway Orchestrating All Microservices
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    return {"success": True, "post_type": "daily_market_intelligence", "slide_count": len(slides), "slides": slides}


@app.post("/api/v1/posts/nifty-prediction-post", tags=["Post Orchestrations"])
def orchestrate_nifty_prediction_post():
    """1-Click Generation of Post 2 (NIFTY 50 Prediction & Technical Analysis)."""
    model = generate_prediction_model()
    slides = render_prediction_carousel(model)
    return {"success": True, "post_type": "nifty_prediction", "slide_count": len(slides), "slides": slides, "model": model}
