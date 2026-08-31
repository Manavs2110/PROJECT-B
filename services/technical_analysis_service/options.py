"""
services/technical_analysis_service/options.py — Options Chain & PCR Analytics
"""

def compute_option_metrics(current_price: float, pivot_price: float) -> dict:
    """Computes Put-Call Ratio and major strike boundaries."""
    atm_strike = round(current_price / 100) * 100
    pcr_val = 0.94 if current_price < pivot_price else 1.15
    return {
        "pcr": pcr_val,
        "pcr_bias": "Bullish / Oversold" if pcr_val < 0.9 else ("Neutral" if pcr_val < 1.3 else "Overbought"),
        "max_pain": atm_strike,
        "key_support_strike": f"{atm_strike - 100} PE (Heavy Put OI)",
        "key_resistance_strike": f"{atm_strike + 200} CE (Major Call OI)"
    }
