from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class BacktestConfig:
    initial_capital: float = 10_000.0
    commission_rate: float = 0.001
    slippage_rate: float = 0.0005


class BacktestingService:
    def run(self, data: pd.DataFrame, signal: pd.Series, cfg: BacktestConfig) -> dict[str, float]:
        returns = data["close"].pct_change().fillna(0).to_numpy()
        pos = signal.shift(1).fillna(0).clip(-1, 1).to_numpy()

        gross = pos * returns
        trades = np.abs(np.diff(pos, prepend=0))
        costs = trades * (cfg.commission_rate + cfg.slippage_rate)
        net = gross - costs

        equity_curve = cfg.initial_capital * np.cumprod(1 + net)
        total_return = (equity_curve[-1] / cfg.initial_capital) - 1
        max_dd = self._max_drawdown(equity_curve)
        sharpe = self._sharpe(net)
        win_rate = float((net > 0).mean())

        return {
            "total_return": float(total_return),
            "max_drawdown": float(max_dd),
            "sharpe_ratio": float(sharpe),
            "win_rate": win_rate,
            "final_equity": float(equity_curve[-1]),
        }

    @staticmethod
    def _max_drawdown(equity: np.ndarray) -> float:
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        return float(np.min(drawdown))

    @staticmethod
    def _sharpe(net_returns: np.ndarray, annualization: int = 252) -> float:
        std = np.std(net_returns)
        if std == 0:
            return 0.0
        return (np.mean(net_returns) / std) * np.sqrt(annualization)
