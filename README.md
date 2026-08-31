# 💹 FinPulse — Daily Market Intelligence Microservices (PROJECT-B)

A clean, production-ready microservices architecture designed to automate financial market intelligence, generate high-conviction 4-slide Instagram carousels, and publish to `@finpulse.daily`.

---

## 🏛️ Microservices Architecture

- **`services/market_data_service.py`**: Live Nifty 50, BSE Sensex, Bank Nifty, India VIX & official NSE FII/DII cash flows.
- **`services/news_service.py`**: Real-time breaking market catalysts and 24h stock news engine.
- **`services/sentiment_service.py`**: AI sector rotation matrix & tactical strategy.
- **`services/image_service.py`**: 1080×1080 Pillow visual renderer with BSE/Wall St exchange silhouettes, Bull/Bear mascot emblems, and clean typography.
- **`services/publisher_service.py`**: Instagram publishing service with 2FA session persistence.
- **`api/app.py`**: FastAPI Gateway exposing modular REST endpoints.

---

## 🚀 Quickstart

### 1. Generate 4-Slide Post
```bash
python3 main.py --generate
```

### 2. Launch FastAPI Microservice Gateway
```bash
python3 main.py --api --port 8000
```
*Interactive Swagger Documentation: http://localhost:8000/docs*

### 3. Generate & Publish Directly to Instagram
```bash
python3 main.py --publish
```
