from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenPair
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=TokenPair)
def register(payload: RegisterRequest, request: Request) -> dict[str, str]:
    key = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(key=f"register:{key}", max_requests=10, per_seconds=60):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    try:
        return auth_service.register(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, request: Request) -> dict[str, str]:
    key = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(
        key=f"login:{key}", max_requests=settings.auth_rate_limit_per_minute, per_seconds=60
    ):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    try:
        return auth_service.login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest) -> dict[str, str]:
    try:
        claims = jwt.decode(
            payload.refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        if claims.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        sub = claims.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return auth_service.refresh(user_id=sub, role="user")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc
