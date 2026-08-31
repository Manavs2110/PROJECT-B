"""
services/visual_rendering_service/api.py — Visual Rendering Microservice REST API
"""

from fastapi import APIRouter
from services.visual_rendering_service.renderer_market_impact import render_market_impact_carousel
from services.visual_rendering_service.renderer_prediction import render_prediction_carousel

router = APIRouter(prefix="/api/v1/render", tags=["Visual Rendering Service"])
