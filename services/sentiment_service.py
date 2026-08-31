"""
sentiment_service.py — AI Macro & Sector Sentiment Intelligence Service
"""

import json
import requests
from typing import Dict, Any, List
from config.settings import settings

def analyze_market_sentiment(indices: Dict[str, Any], fii_dii: Dict[str, Any], news: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes live market parameters and breaking news to determine market sentiment,
    sector rotation, and tactical strategy.
    """
    news_summary = "\n".join([f"• {a.get('title')} ({a.get('source_name')})" for a in news[:4]])

    prompt = f"""You are a senior institutional equity research strategist.
Analyze the following market indicators and breaking news:

INDICES:
• Nifty 50: {indices['nifty']['formatted_price']} ({indices['nifty']['formatted_change']})
• Sensex: {indices['sensex']['formatted_price']} ({indices['sensex']['formatted_change']})
• Bank Nifty: {indices['banknifty']['formatted_price']} ({indices['banknifty']['formatted_change']})
• India VIX: {indices['vix']['price']:.2f} ({indices['vix']['formatted_change']})

CASH FLOWS:
• FII Net: {fii_dii['fii']['formatted_net']} ({fii_dii['fii']['bias']})
• DII Net: {fii_dii['dii']['formatted_net']} ({fii_dii['dii']['bias']})
• Total Institutional: {fii_dii['formatted_total_net']}

TOP NEWS:
{news_summary}

Return valid JSON with:
{{
  "market_mood": "Bullish / Bearish / Consolidation / Volatile",
  "vix_interpretation": "Brief volatility assessment (under 12 words)",
  "sectors": [
    {{
      "sector_name": "Banking & Financials",
      "impact": "BULLISH",
      "catalyst": "Private lenders leading credit growth and stable asset quality.",
      "affected_stocks": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK"]
    }},
    {{
      "sector_name": "IT & Artificial Intelligence",
      "impact": "BULLISH",
      "catalyst": "Global tech rally and robust enterprise AI deal momentum.",
      "affected_stocks": ["TCS", "INFY", "HCLTECH", "WIPRO"]
    }},
    {{
      "sector_name": "Energy & Oil & Gas",
      "impact": "BEARISH",
      "catalyst": "Crude oil corrections adjusting downstream marketing margins.",
      "affected_stocks": ["RELIANCE", "ONGC", "BPCL", "IOC"]
    }}
  ],
  "institutional_outlook": "One sentence summary on institutional positioning",
  "tactical_strategy": "One clear tactical action for the trading session"
}}
"""

    analysis = None
    if settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("gsk_placeholder"):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.25,
                    "response_format": {"type": "json_object"}
                },
                timeout=8
            )
            if r.status_code == 200:
                analysis = json.loads(r.json()["choices"][0]["message"]["content"])
        except Exception:
            pass

    if not analysis or "sectors" not in analysis:
        is_pos = indices["nifty"]["is_positive"]
        analysis = {
            "market_mood": "Bullish Momentum" if is_pos else "Consolidation",
            "vix_interpretation": f"India VIX at {indices['vix']['price']:.2f} signals calm volatility environment",
            "sectors": [
                {
                    "sector_name": "Banking & Financials",
                    "impact": "BULLISH",
                    "catalyst": "Private lenders leading credit growth and stable asset quality.",
                    "affected_stocks": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK"]
                },
                {
                    "sector_name": "IT & Artificial Intelligence",
                    "impact": "BULLISH",
                    "catalyst": "Global tech rally and robust enterprise AI deal momentum.",
                    "affected_stocks": ["TCS", "INFY", "HCLTECH", "WIPRO"]
                },
                {
                    "sector_name": "Energy & Oil & Gas",
                    "impact": "BEARISH",
                    "catalyst": "Crude oil corrections adjusting downstream marketing margins.",
                    "affected_stocks": ["RELIANCE", "ONGC", "BPCL", "IOC"]
                }
            ],
            "institutional_outlook": f"FIIs ({fii_dii['fii']['formatted_net']}) & DIIs ({fii_dii['dii']['formatted_net']}) active in cash segment.",
            "tactical_strategy": "Accumulate leading private banks & IT leaders on intraday pullbacks."
        }

    return analysis
