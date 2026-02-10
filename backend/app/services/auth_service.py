from dataclasses import asdict
from uuid import uuid4

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.audit_log import AuditLog
from app.models.user import User


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_email: dict[str, User] = {}
        self._audit_logs: list[AuditLog] = []

    def create_user(self, email: str, password: str) -> User:
        normalized = email.lower()
        if normalized in self._users_by_email:
            raise ValueError("user already exists")
        user = User(id=str(uuid4()), email=normalized, hashed_password=hash_password(password))
        self._users_by_email[normalized] = user
        self._audit_logs.append(
            AuditLog(actor_user_id=user.id, action="register", details=f"registered:{normalized}")
        )
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._users_by_email.get(email.lower())

    def validate_credentials(self, email: str, password: str) -> User | None:
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        self._audit_logs.append(
            AuditLog(actor_user_id=user.id, action="login", details=f"login:{user.email}")
        )
        return user

    def get_audit_logs(self) -> list[dict[str, str]]:
        return [asdict(item) for item in self._audit_logs]


class AuthService:
    def __init__(self, store: InMemoryUserStore) -> None:
        self.store = store

    def register(self, email: str, password: str) -> dict[str, str]:
        user = self.store.create_user(email=email, password=password)
        return self._token_pair(user.id, user.role)

    def login(self, email: str, password: str) -> dict[str, str]:
        user = self.store.validate_credentials(email=email, password=password)
        if not user:
            raise ValueError("invalid credentials")
        return self._token_pair(user.id, user.role)

    def refresh(self, user_id: str, role: str) -> dict[str, str]:
        return self._token_pair(user_id=user_id, role=role)

    @staticmethod
    def _token_pair(user_id: str, role: str) -> dict[str, str]:
        return {
            "access_token": create_access_token(subject=user_id, role=role),
            "refresh_token": create_refresh_token(subject=user_id),
            "token_type": "bearer",
        }


user_store = InMemoryUserStore()
auth_service = AuthService(user_store)
