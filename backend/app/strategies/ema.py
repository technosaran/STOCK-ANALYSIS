import pandas as pd

from app.strategies.base import BaseStrategy


class EMACrossoverStrategy(BaseStrategy):
    def __init__(self, short_window: int = 12, long_window: int = 26) -> None:
        if short_window >= long_window:
            raise ValueError("short_window must be less than long_window")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data: pd.DataFrame) -> pd.Series:
        close = data["close"]
        short_ema = close.ewm(span=self.short_window, adjust=False).mean()
        long_ema = close.ewm(span=self.long_window, adjust=False).mean()
        signal = (short_ema > long_ema).astype(int)
        return signal.diff().fillna(0)
