"""
services/market_data_service/api.py — Market Data Microservice REST API
"""

from fastapi import APIRouter
from services.market_data_service.client import fetch_market_indices, fetch_fii_dii_cash_flows

router = APIRouter(prefix="/api/v1/market", tags=["Market Data Service"])

@router.get("/indices")
def get_indices():
    return fetch_market_indices()

@router.get("/fii-dii")
def get_fii_dii():
    return fetch_fii_dii_cash_flows()
