"""
settings.py — Production Configuration & Environment Manager for FinPulse
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "FinPulse Daily Market Intelligence Microservice"
    VERSION: str = "2.0.0"
    BASE_DIR: Path = BASE_DIR
    
    # Storage Paths
    OUTPUT_DIR: Path = BASE_DIR / "output" / "images"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    DATA_DIR: Path = BASE_DIR / "data"
    SESSIONS_DIR: Path = BASE_DIR / "data" / "sessions"
    
    # API Keys & Credentials
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    IMGBB_API_KEY: str = os.getenv("IMGBB_API_KEY", "")
    
    # Instagram Credentials
    INSTAGRAM_USERNAME: str = os.getenv("INSTAGRAM_FINPULSE_USERNAME", "finpulse.daily")
    INSTAGRAM_PASSWORD: str = os.getenv("INSTAGRAM_FINPULSE_PASSWORD", "")
    
    # Server Settings
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    
    # Visual Branding
    PAGE_HANDLE: str = "finpulse.daily"
    BRAND_NAME: str = "FINPULSE DAILY"

settings = Settings()
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
