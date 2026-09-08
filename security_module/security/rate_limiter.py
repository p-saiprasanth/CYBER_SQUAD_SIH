"""
rate_limiter.py
---------------
Phase 1 (remainder) — Rate limiting.

Simple sliding-window rate limiter to prevent API abuse (e.g. someone
hammering /security/verify-evidence or brute-forcing login). In-memory
implementation appropriate for a hackathon MVP single-process demo;
swap for Redis-backed limiting in production/multi-instance deployment.
"""

import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Parameters
        ----------
        max_requests   : max allowed requests per key within the window
        window_seconds : size of the sliding window, in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits = defaultdict(deque)  # key -> deque of request timestamps

    def allow(self, key: str) -> bool:
        """
        Check whether a request identified by `key` (e.g. user_id or IP)
        is allowed right now. Returns True if allowed, False if rate-limited.
        """
        now = time.time()
        window_start = now - self.window_seconds
        hits = self._hits[key]

        # drop timestamps that have fallen out of the window
        while hits and hits[0] < window_start:
            hits.popleft()

        if len(hits) >= self.max_requests:
            return False

        hits.append(now)
        return True

    def remaining(self, key: str) -> int:
        """How many requests this key has left in the current window."""
        now = time.time()
        window_start = now - self.window_seconds
        hits = self._hits[key]
        while hits and hits[0] < window_start:
            hits.popleft()
        return max(0, self.max_requests - len(hits))


# Pre-configured limiters for sensitive endpoints
login_limiter = RateLimiter(max_requests=5, window_seconds=60)          # 5 login attempts / min
verify_limiter = RateLimiter(max_requests=30, window_seconds=60)        # 30 verifications / min
ai_query_limiter = RateLimiter(max_requests=10, window_seconds=60)      # 10 AI queries / min


if __name__ == "__main__":
    limiter = RateLimiter(max_requests=3, window_seconds=10)
    user = "U001"

    for i in range(5):
        allowed = limiter.allow(user)
        print(f"Request {i+1}: {'allowed' if allowed else 'BLOCKED (rate limited)'}")
