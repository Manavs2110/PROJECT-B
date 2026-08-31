"""
news.py — Market & Stock News Endpoints
"""

from fastapi import APIRouter, Query
from services.news_service import get_breaking_market_news, get_stock_news_24h

router = APIRouter(prefix="/api/v1/news", tags=["News"])

@router.get("/breaking")
def breaking_news(limit: int = Query(5, ge=1, le=20)):
    """Returns top breaking market news stories."""
    return {"count": limit, "items": get_breaking_market_news(limit)}

@router.get("/stock/{ticker}")
def stock_news(ticker: str, limit: int = Query(5, ge=1, le=20)):
    """Returns past 24-hour news for any stock ticker."""
    return get_stock_news_24h(ticker, limit)
