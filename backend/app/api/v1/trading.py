from fastapi import APIRouter, Depends
import pandas as pd

from app.ai.signal_model import AISignalModel
from app.api.deps import get_current_claims
from app.risk.engine import PositionSizingInput, RiskEngine
from app.services.backtesting_service import BacktestConfig, BacktestingService
from app.strategies.ema import EMACrossoverStrategy

router = APIRouter()


@router.post("/backtest")
def run_backtest(_claims: dict[str, str] = Depends(get_current_claims)) -> dict[str, float]:
    close = pd.Series([100, 101, 102, 101, 103, 104, 102, 106, 108, 109], dtype=float)
    data = pd.DataFrame({"close": close})
    strategy = EMACrossoverStrategy(2, 5)
    signal = strategy.generate_signal(data)
    service = BacktestingService()
    return service.run(data=data, signal=signal, cfg=BacktestConfig())


@router.post("/risk/position-size")
def position_size(_claims: dict[str, str] = Depends(get_current_claims)) -> dict[str, float]:
    risk_engine = RiskEngine()
    quantity = risk_engine.position_size(
        PositionSizingInput(capital=10_000, risk_percent=0.01, entry_price=100, stop_price=98)
    )
    return {"quantity": quantity}


@router.post("/ai/train")
def train_ai(_claims: dict[str, str] = Depends(get_current_claims)) -> dict[str, float]:
    frame = pd.DataFrame(
        {
            "close": [100, 101, 99, 102, 105, 107, 106, 108, 110, 109, 111, 114, 115, 113, 116],
            "volume": [1_000, 1_010, 1_030, 1_100, 1_050, 1_120, 1_090, 1_130, 1_200, 1_150, 1_180, 1_250, 1_240, 1_210, 1_300],
        }
    )
    model = AISignalModel()
    engineered = model.feature_engineering(frame)
    return model.train(engineered)
