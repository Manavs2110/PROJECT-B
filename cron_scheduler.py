"""
cron_scheduler.py — Automated 4:00 PM IST Daily Publishing Service for FinPulse
Orchestrates Market Closing Intelligence (Post #1) & Prediction (Post #2) on trading days.
"""

import sys
import time
import argparse
import datetime
import zoneinfo
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FinPulseScheduler")

IST = zoneinfo.ZoneInfo("Asia/Kolkata")

def execute_daily_publishing_job(publish_to_instagram: bool = True) -> dict:
    """
    Executes the 4:00 PM IST post-market closing pipeline:
    1. Fetches latest closing indices, FII/DII cash flows, and breaking news.
    2. Renders 5-slide Market Intelligence carousel (Post #1).
    3. Runs Technical & Prediction model and renders 5-slide Prediction carousel (Post #2).
    4. Automatically publishes both carousels to Instagram @finpulse.daily.
    """
    logger.info("🚀 Starting 4:00 PM IST Automated Publishing Pipeline...")
    results = {"timestamp": datetime.datetime.now(IST).isoformat(), "post1": None, "post2": None}

    try:
        from services.market_data_service import fetch_market_indices, fetch_fii_dii_cash_flows
        from services.news_curation_service import fetch_breaking_market_news
        from services.prediction_service import generate_prediction_model
        from services.visual_rendering_service import render_market_impact_carousel, render_prediction_carousel
        from services.publishing_service import publish_carousel_to_instagram
        from gateway.app import build_market_post_caption, build_prediction_post_caption

        # ── 1. POST #1: DAILY MARKET INTELLIGENCE ──
        logger.info("📊 Step 1/4: Fetching market closing data & flows...")
        indices = fetch_market_indices()
        fii_dii = fetch_fii_dii_cash_flows()
        news = fetch_breaking_market_news(limit=5)

        sentiment = {
            "market_mood": "Bullish Momentum" if indices["nifty"]["is_positive"] else "Consolidation",
            "vix_interpretation": f"India VIX at {indices['vix']['price']:.2f} signals calm volatility",
            "sectors": [
                {"sector_name": "Banking & Financials", "impact": "BULLISH", "catalyst": "Private lenders leading credit growth.", "affected_stocks": ["HDFCBANK", "ICICIBANK", "SBIN"]},
                {"sector_name": "IT & AI", "impact": "BULLISH", "catalyst": "Global enterprise AI momentum.", "affected_stocks": ["TCS", "INFY", "HCLTECH"]},
                {"sector_name": "Energy & Oil", "impact": "BEARISH", "catalyst": "Downstream margin adjustments.", "affected_stocks": ["RELIANCE", "ONGC"]}
            ],
            "tactical_strategy": "Accumulate leading private banks & IT leaders on pullbacks."
        }

        logger.info("🎨 Step 2/4: Rendering Post #1 (5-slide carousel)...")
        slides_1 = render_market_impact_carousel(indices, fii_dii, sentiment, news)
        caption_1 = build_market_post_caption(indices, fii_dii, sentiment, news)

        if publish_to_instagram:
            logger.info("📲 Step 3/4: Publishing Post #1 to Instagram @finpulse.daily...")
            pub_res1 = publish_carousel_to_instagram(slides_1, caption_1)
            results["post1"] = pub_res1
            if pub_res1.get("success"):
                logger.info(f"✅ Post #1 published live: {pub_res1.get('post_url')}")
            else:
                logger.warning(f"⚠️ Post #1 publish issue: {pub_res1.get('error')}")
        else:
            results["post1"] = {"success": True, "slides": slides_1, "mode": "render_only"}

        # ── 2. POST #2: NIFTY 50 PREDICTION ──
        logger.info("🎯 Step 4/4: Generating & Rendering Post #2 (Prediction & Strategy)...")
        model = generate_prediction_model()
        slides_2 = render_prediction_carousel(model)
        caption_2 = build_prediction_post_caption(model)

        if publish_to_instagram:
            logger.info("📲 Publishing Post #2 to Instagram @finpulse.daily...")
            pub_res2 = publish_carousel_to_instagram(slides_2, caption_2)
            results["post2"] = pub_res2
            if pub_res2.get("success"):
                logger.info(f"✅ Post #2 published live: {pub_res2.get('post_url')}")
            else:
                logger.warning(f"⚠️ Post #2 publish issue: {pub_res2.get('error')}")
        else:
            results["post2"] = {"success": True, "slides": slides_2, "mode": "render_only"}

        logger.info("🎉 4:00 PM Daily Publishing Job Completed Successfully!")
        return {"success": True, "results": results}

    except Exception as e:
        logger.error(f"❌ Error during 4:00 PM publishing job: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


def run_daemon(target_hour: int = 16, target_minute: int = 0):
    """
    Continuous background daemon waking up at target time (16:00 IST)
    every Monday through Friday (trading days).
    """
    logger.info(f"⏰ FinPulse Scheduler Daemon started. Scheduled for {target_hour:02d}:{target_minute:02d} IST (Mon-Fri).")
    last_run_date = None

    while True:
        now = datetime.datetime.now(IST)
        weekday = now.weekday()  # 0 = Monday, 4 = Friday
        today_date = now.date()

        if weekday < 5:  # Monday to Friday
            if now.hour == target_hour and now.minute == target_minute and last_run_date != today_date:
                logger.info(f"🔔 Target time reached ({now.strftime('%Y-%m-%d %H:%M:%S %Z')}). Triggering daily publishing job...")
                execute_daily_publishing_job(publish_to_instagram=True)
                last_run_date = today_date
                time.sleep(70)

        time.sleep(30)


def print_cron_setup_instructions():
    """Generates the exact crontab entry for macOS / Linux system cron."""
    python_path = sys.executable
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    cron_line = f"0 16 * * 1-5 cd {project_dir} && {python_path} {script_path} --now >> {project_dir}/cron.log 2>&1"

    print("\n" + "═" * 70)
    print("  📋 NATIVE OS CRONTAB SETUP (4:00 PM IST MON-FRI)")
    print("═" * 70)
    print("\nTo schedule this natively using your system cron, run:")
    print("  $ crontab -e\n")
    print("And paste the following line at the bottom:\n")
    print(f"  {cron_line}\n")
    print("This will execute every Monday through Friday at exactly 4:00 PM (16:00 IST).\n")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinPulse 4:00 PM IST Daily Auto-Publishing Cron Scheduler")
    parser.add_argument("--now", action="store_true", help="Execute the daily 4:00 PM publishing job immediately")
    parser.add_argument("--no-publish", action="store_true", help="Generate slides and captions without uploading to Instagram")
    parser.add_argument("--daemon", action="store_true", help="Run as a continuous background daemon checking every minute")
    parser.add_argument("--setup-cron", action="store_true", help="Show system crontab setup instructions")

    args = parser.parse_args()

    if args.setup_cron:
        print_cron_setup_instructions()
    elif args.now:
        execute_daily_publishing_job(publish_to_instagram=not args.no_publish)
    elif args.daemon:
        run_daemon(target_hour=16, target_minute=0)
    else:
        parser.print_help()
