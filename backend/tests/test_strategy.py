import pandas as pd

from app.strategies.ema import EMACrossoverStrategy


def test_ema_strategy_generates_series() -> None:
    df = pd.DataFrame({"close": [1, 2, 3, 2, 4, 6, 5]})
    strategy = EMACrossoverStrategy(short_window=2, long_window=4)

    signal = strategy.generate_signal(df)

    assert len(signal) == len(df)
    assert signal.isin([-1, 0, 1]).all()
