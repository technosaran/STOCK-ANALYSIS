from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> pd.Series:
        """Return signal series: 1 long, -1 short, 0 flat."""
