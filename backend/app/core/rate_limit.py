from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[datetime]] = defaultdict(deque)

    def allow(self, key: str, max_requests: int, per_seconds: int) -> bool:
        now = datetime.now(UTC)
        threshold = now - timedelta(seconds=per_seconds)
        bucket = self._hits[key]

        while bucket and bucket[0] < threshold:
            bucket.popleft()

        if len(bucket) >= max_requests:
            return False

        bucket.append(now)
        return True


rate_limiter = InMemoryRateLimiter()
