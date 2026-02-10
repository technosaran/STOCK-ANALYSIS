from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class User:
    id: str
    email: str
    hashed_password: str
    role: str = "user"
    is_verified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
