import pytest

from app.risk.engine import PositionSizingInput, RiskEngine


def test_position_size_respects_risk_amount() -> None:
    engine = RiskEngine()
    quantity = engine.position_size(
        PositionSizingInput(capital=10_000, risk_percent=0.01, entry_price=100, stop_price=99)
    )
    assert quantity == pytest.approx(100.0)


def test_position_size_rejects_invalid_risk() -> None:
    engine = RiskEngine()
    with pytest.raises(ValueError):
        engine.position_size(
            PositionSizingInput(capital=10_000, risk_percent=0.05, entry_price=100, stop_price=99)
        )
