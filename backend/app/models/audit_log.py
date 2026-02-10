from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class AuditLog:
    actor_user_id: str
    action: str
    details: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
