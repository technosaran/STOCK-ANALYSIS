from datetime import datetime

from pydantic import BaseModel


class OHLCV(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketDataResponse(BaseModel):
    symbol: str
    interval: str
    rows: list[OHLCV]
    source: str
