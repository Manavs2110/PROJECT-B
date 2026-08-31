"""
services/prediction_service/api.py — Nifty 50 Prediction Microservice REST API
"""

from fastapi import APIRouter
from services.prediction_service.predictor import generate_prediction_model

router = APIRouter(prefix="/api/v1/prediction", tags=["Prediction Service"])

@router.get("/nifty-model")
def get_model():
    return generate_prediction_model()
