from dataclasses import dataclass


@dataclass(slots=True)
class PositionSizingInput:
    capital: float
    risk_percent: float
    entry_price: float
    stop_price: float


class RiskEngine:
    @staticmethod
    def validate_risk_percent(risk_percent: float) -> None:
        if risk_percent <= 0 or risk_percent > 0.02:
            raise ValueError("risk_percent must be within (0, 0.02]")

    def position_size(self, data: PositionSizingInput) -> float:
        self.validate_risk_percent(data.risk_percent)
        risk_amount = data.capital * data.risk_percent
        per_share_risk = abs(data.entry_price - data.stop_price)
        if per_share_risk <= 0:
            raise ValueError("entry_price and stop_price cannot be equal")
        return risk_amount / per_share_risk
