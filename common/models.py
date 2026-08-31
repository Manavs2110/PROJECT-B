"""
common/models.py — Shared Domain Models & Pydantic Schemas
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MarketQuote(BaseModel):
    name: str
    price: float
    formatted_price: str
    change: float
    change_pct: float
    formatted_change: str
    bias: str
    is_positive: bool

class FlowCategory(BaseModel):
    category: str
    buy: float
    sell: float
    net: float
    bias: str
    formatted_net: str

class FiiDiiData(BaseModel):
    date: str
    source: str
    fii: FlowCategory
    dii: FlowCategory
    total_net: float
    formatted_total_net: str
    sentiment: str

class NewsItem(BaseModel):
    title: str
    source_name: str
    url: str
    published_at: str

class SectorImpact(BaseModel):
    sector_name: str
    impact: str
    catalyst: str
    affected_stocks: List[str]

class PredictionPayload(BaseModel):
    predicted_trend: str
    probability_bull_pct: int
    expected_trading_range: str
    key_catalyst_driver: str
    options_strategy: str

class PublishRequest(BaseModel):
    slides: List[str]
    caption: str
    verification_code: Optional[str] = None
