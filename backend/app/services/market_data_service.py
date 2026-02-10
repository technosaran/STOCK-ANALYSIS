import json
from datetime import UTC, datetime, timedelta
from typing import Any

import pandas as pd
import yfinance as yf

from app.core.config import settings
from app.schemas.market_data import MarketDataResponse, OHLCV


class InMemoryCache:
    def __init__(self) -> None:
        self._data: dict[str, tuple[datetime, str]] = {}

    def get(self, key: str) -> str | None:
        entry = self._data.get(key)
        if not entry:
            return None
        expires_at, value = entry
        if datetime.now(UTC) > expires_at:
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        self._data[key] = (datetime.now(UTC) + timedelta(seconds=ttl_seconds), value)


class MarketDataService:
    def __init__(self, cache: InMemoryCache) -> None:
        self.cache = cache

    def get_ohlc(self, symbol: str, interval: str, period: str = "1mo") -> MarketDataResponse:
        cache_key = f"ohlc:{symbol}:{interval}:{period}"
        cached = self.cache.get(cache_key)
        if cached:
            payload = json.loads(cached)
            return MarketDataResponse(**payload, source="cache")

        frame = yf.Ticker(symbol).history(period=period, interval=interval)
        if isinstance(frame, pd.DataFrame) and frame.empty:
            raise ValueError("No market data returned")

        rows = [
            OHLCV(
                timestamp=index.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            )
            for index, row in frame.iterrows()
        ]

        response_payload: dict[str, Any] = {
            "symbol": symbol.upper(),
            "interval": interval,
            "rows": [item.model_dump(mode="json") for item in rows],
        }
        self.cache.set(cache_key, json.dumps(response_payload), settings.yahoo_cache_ttl_seconds)
        return MarketDataResponse(**response_payload, source="yahoo")


market_data_service = MarketDataService(InMemoryCache())
