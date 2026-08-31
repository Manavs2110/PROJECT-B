"""
test_microservices.py — Production Test Suite for PROJECT-B
"""

import os
import sys
import unittest
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from services import (
    get_market_indices, get_fii_dii_cash_flows,
    get_breaking_market_news, get_stock_news_24h,
    analyze_market_sentiment, generate_4slide_carousel,
    fetch_nifty_technical_data, generate_nifty_prediction_model,
    generate_nifty_prediction_carousel
)

class TestFinPulseMicroservices(unittest.TestCase):

    def test_market_indices(self):
        indices = get_market_indices()
        self.assertIn("nifty", indices)
        self.assertIn("sensex", indices)
        self.assertIn("banknifty", indices)
        self.assertIn("vix", indices)
        self.assertGreater(indices["nifty"]["price"], 0)

    def test_fii_dii_flows(self):
        flows = get_fii_dii_cash_flows()
        self.assertIn("fii", flows)
        self.assertIn("dii", flows)
        self.assertIn("total_net", flows)

    def test_breaking_news(self):
        news = get_breaking_market_news(limit=3)
        self.assertGreaterEqual(len(news), 1)
        self.assertIn("title", news[0])

    def test_stock_news_24h(self):
        res = get_stock_news_24h("RELIANCE", limit=3)
        self.assertEqual(res["ticker"], "RELIANCE")
        self.assertGreaterEqual(res["count"], 1)

    def test_sentiment_analysis(self):
        indices = get_market_indices()
        flows = get_fii_dii_cash_flows()
        news = get_breaking_market_news(limit=3)
        sentiment = analyze_market_sentiment(indices, flows, news)
        self.assertIn("market_mood", sentiment)
        self.assertIn("sectors", sentiment)

    def test_4slide_image_generation(self):
        indices = get_market_indices()
        flows = get_fii_dii_cash_flows()
        news = get_breaking_market_news(limit=3)
        sentiment = analyze_market_sentiment(indices, flows, news)
        slides = generate_4slide_carousel(indices, flows, sentiment, news)
        self.assertEqual(len(slides), 4)
        for s in slides:
            self.assertTrue(os.path.exists(s))

    def test_technical_analysis(self):
        tech = fetch_nifty_technical_data()
        self.assertIn("current_price", tech)
        self.assertIn("pivots", tech)
        self.assertIn("moving_averages", tech)
        self.assertIn("oscillators", tech)
        self.assertGreater(tech["pivots"]["r1"], tech["pivots"]["s1"])

    def test_nifty_prediction_model(self):
        model = generate_nifty_prediction_model()
        self.assertIn("technical_data", model)
        self.assertIn("derivatives_data", model)
        self.assertIn("prediction", model)
        self.assertIn("trade_playbook", model["prediction"])

    def test_nifty_prediction_carousel_generation(self):
        model = generate_nifty_prediction_model()
        slides = generate_nifty_prediction_carousel(model)
        self.assertEqual(len(slides), 4)
        for s in slides:
            self.assertTrue(os.path.exists(s))

if __name__ == "__main__":
    unittest.main()
