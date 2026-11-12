import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.opened_at = None

    def call(self, function, *args, **kwargs):
        if self.state == "OPEN":
            elapsed = time.monotonic() - self.opened_at

            if elapsed < self.recovery_timeout:
                raise RuntimeError("Circuit Breaker OPEN: servicio temporalmente bloqueado")

            self.state = "HALF_OPEN"

        try:
            result = function(*args, **kwargs)

            self.failures = 0
            self.state = "CLOSED"
            self.opened_at = None

            return result

        except Exception:
            self.failures += 1

            if self.state == "HALF_OPEN" or self.failures >= self.failure_threshold:
                self.state = "OPEN"
                self.opened_at = time.monotonic()

            raise


def retry_with_backoff(function, max_attempts=3, base_delay=1):
    for attempt in range(max_attempts):
        try:
            return function()

        except Exception:
            if attempt == max_attempts - 1:
                raise

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
