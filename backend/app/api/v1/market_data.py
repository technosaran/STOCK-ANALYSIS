from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_current_claims
from app.schemas.market_data import MarketDataResponse
from app.services.market_data_service import market_data_service

router = APIRouter()


@router.get("/ohlc", response_model=MarketDataResponse)
def get_ohlc(
    symbol: str = Query(..., min_length=1, max_length=10),
    interval: str = Query("1d"),
    period: str = Query("1mo"),
    _claims: dict[str, str] = Depends(get_current_claims),
) -> MarketDataResponse:
    try:
        return market_data_service.get_ohlc(symbol=symbol, interval=interval, period=period)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
