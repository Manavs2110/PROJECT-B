"""
services/technical_analysis_service/api.py — Technical Analysis Microservice REST API
"""

from fastapi import APIRouter
from services.technical_analysis_service.indicators import compute_nifty_technicals
from services.technical_analysis_service.options import compute_option_metrics

router = APIRouter(prefix="/api/v1/technical", tags=["Technical Analysis Service"])

@router.get("/nifty")
def get_nifty_technicals():
    tech = compute_nifty_technicals()
    derivs = compute_option_metrics(tech["current_price"], tech["pivots"]["pivot"])
    return {"technical": tech, "derivatives": derivs}
