"""
services/news_curation_service/api.py — News Curation Microservice REST API
"""

from fastapi import APIRouter, Query
from services.news_curation_service.engine import fetch_breaking_market_news, fetch_stock_news_24h

router = APIRouter(prefix="/api/v1/news", tags=["News Curation Service"])

@router.get("/breaking")
def get_breaking(limit: int = Query(5, ge=1, le=20)):
    return {"count": limit, "items": fetch_breaking_market_news(limit)}

@router.get("/stock/{ticker}")
def get_stock_news(ticker: str, limit: int = Query(5, ge=1, le=20)):
    return fetch_stock_news_24h(ticker, limit)
