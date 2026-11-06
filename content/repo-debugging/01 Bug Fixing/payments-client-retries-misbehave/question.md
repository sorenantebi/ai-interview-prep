---
difficulty: Medium
kind: bug-fix
---
# Payments client retries misbehave

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
The `payments` package wraps our card gateway. Calls that fail with temporary errors (timeouts, rate limits) are retried with exponential backoff, and the sleep function is injected so tests never wait. Since the last release, support has seen three problems. The waits between retries grow much faster than the configured schedule. The client sometimes sends one more request than `max_attempts` allows. And when the issuer declines a card, the caller gets no error, so the checkout flow crashes later on an empty result.

## Your tasks
1. The backoff delays don't follow the expected schedule (starting at `base_delay` and multiplying by `factor` for each further retry). Find and fix the cause.
2. A client configured with `max_attempts=N` can end up making `N + 1` requests before giving up. Find and fix the cause.
3. Errors that should never be retried (declined card, invalid request) don't reach the caller. Find and fix the cause.
4. Make all visible tests pass without changing the tests. Hidden tests cover more edge cases.

## Notes
- The public entry points are `PaymentsClient.charge` in `payments/client.py` and `call_with_retry` in `payments/retry.py`.
- `max_attempts` counts the first request too: `max_attempts=3` means one request plus at most two retries.
- Only subclasses of `TransientError` are retryable. Any other error should reach the caller unchanged, and exceptions that are not `PaymentError`s must never be retried.
- When the gateway sends a `retry_after` hint, we wait at least that long.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
