"""
market.py — Market Indices & Cash Flow Endpoints
"""

from fastapi import APIRouter
from services.market_data_service import get_market_indices, get_fii_dii_cash_flows

router = APIRouter(prefix="/api/v1/market", tags=["Market Data"])

@router.get("/indices")
def get_indices():
    """Returns live Nifty 50, Sensex, Bank Nifty, and India VIX data."""
    return get_market_indices()

@router.get("/fii-dii")
def get_fii_dii():
    """Returns official NSE FII/FPI and DII cash flow data."""
    return get_fii_dii_cash_flows()
