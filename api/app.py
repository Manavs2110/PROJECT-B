"""
app.py — FinPulse Microservices FastAPI Gateway
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.settings import settings
from api.routes import market, news, post, prediction

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Clean, production-ready microservices for daily stock market intelligence, visual slide generation, and Instagram publishing."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated images statically
app.mount("/images", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="images")

# Mount Routers
app.include_router(market.router)
app.include_router(news.router)
app.include_router(post.router)
app.include_router(prediction.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME, "version": settings.VERSION}
