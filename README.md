# QuantEdge

QuantEdge is a production-style AI-powered algorithmic trading and backtesting platform scaffold with clean architecture, secure auth, modular strategy/risk/AI components, testing, and CI/CD.

## Repository Structure

```text
backend/
  app/
    api/
    core/
    services/
    models/
    strategies/
    risk/
    ai/
    utils/
  tests/
  Dockerfile
frontend/
  components/
  pages/
  services/
  hooks/
  context/
```

## Tech Stack

- Frontend: Next.js + Tailwind + Lightweight Charts (scaffold folders included)
- Backend: FastAPI, Pydantic, JWT auth, yfinance integration
- Data: PostgreSQL (configured via env), Redis cache abstraction
- ML: Logistic Regression + Random Forest feature scoring
- DevOps: Docker + GitHub Actions CI

## Quick Start (Backend)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## Implemented Features

- JWT auth with access and refresh token flow
- Rate-limited auth endpoints
- In-memory user/audit store (can be replaced by SQLAlchemy repositories)
- Yahoo Finance OHLC endpoint with cache-first retrieval
- EMA crossover strategy module
- O(n) vectorized backtesting engine with slippage/commission
- Risk engine with 1-2% risk enforcement and position sizing
- AI feature engineering + model training score endpoint
- Unit and API tests with pytest
- CI pipeline (lint, mypy, tests)

## 60-Day Delivery Plan

See `docs/roadmap.md`.
