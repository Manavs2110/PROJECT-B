"""
services/publishing_service/api.py — Publishing Microservice REST API
"""

from fastapi import APIRouter, HTTPException
from common.models import PublishRequest
from services.publishing_service.publisher import publish_carousel_to_instagram

router = APIRouter(prefix="/api/v1/publish", tags=["Publishing Service"])

@router.post("/instagram")
def publish_to_instagram(req: PublishRequest):
    res = publish_carousel_to_instagram(req.slides, req.caption, req.verification_code)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res)
    return res
