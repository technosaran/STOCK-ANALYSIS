from fastapi import APIRouter

from app.api.v1 import auth, market_data, trading

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(market_data.router, prefix="/market-data", tags=["market-data"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
