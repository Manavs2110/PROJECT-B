"""
test_microservices.py — Comprehensive Test Suite for Separated Microservices
"""

import os
import sys
import unittest
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from common import settings, get_font, create_gradient_canvas
from services.market_data_service import fetch_market_indices, fetch_fii_dii_cash_flows
from services.news_curation_service import fetch_breaking_market_news, fetch_stock_news_24h
from services.technical_analysis_service import compute_nifty_technicals, compute_option_metrics
from services.prediction_service import generate_prediction_model
from services.visual_rendering_service import render_market_impact_carousel, render_prediction_carousel

class TestMicroservicesArchitecture(unittest.TestCase):

    def test_common_module(self):
        self.assertIsNotNone(settings.OUTPUT_DIR)
        canvas = create_gradient_canvas((185, 28, 28), (69, 10, 10))
        self.assertEqual(canvas.size, (1080, 1080))

    def test_market_data_service(self):
        indices = fetch_market_indices()
        flows = fetch_fii_dii_cash_flows()
        self.assertIn("nifty", indices)
        self.assertIn("sensex", indices)
        self.assertIn("fii", flows)
        self.assertIn("dii", flows)

    def test_news_curation_service(self):
        news = fetch_breaking_market_news(limit=3)
        stock_news = fetch_stock_news_24h("TCS", limit=2)
        self.assertGreaterEqual(len(news), 1)
        self.assertEqual(stock_news["ticker"], "TCS")

    def test_technical_analysis_service(self):
        tech = compute_nifty_technicals()
        derivs = compute_option_metrics(tech["current_price"], tech["pivots"]["pivot"])
        self.assertIn("pivots", tech)
        self.assertIn("moving_averages", tech)
        self.assertIn("pcr", derivs)

    def test_prediction_service(self):
        model = generate_prediction_model()
        self.assertIn("technical_data", model)
        self.assertIn("prediction", model)
        self.assertIn("trade_playbook", model["prediction"])

    def test_visual_rendering_post1(self):
        indices = fetch_market_indices()
        flows = fetch_fii_dii_cash_flows()
        news = fetch_breaking_market_news(limit=3)
        sentiment = {
            "market_mood": "Bullish",
            "vix_interpretation": "Low volatility",
            "sectors": [{"sector_name": "Banking", "impact": "BULLISH", "catalyst": "Growth", "affected_stocks": ["HDFCBANK"]}],
            "tactical_strategy": "Buy on dips"
        }
        slides = render_market_impact_carousel(indices, flows, sentiment, news)
        self.assertEqual(len(slides), 4)
        for s in slides:
            self.assertTrue(os.path.exists(s))

    def test_visual_rendering_post2(self):
        model = generate_prediction_model()
        slides = render_prediction_carousel(model)
        self.assertEqual(len(slides), 4)
        for s in slides:
            self.assertTrue(os.path.exists(s))

if __name__ == "__main__":
    unittest.main()
