# Payments client retries misbehave - Solution

## Root causes / approach

There are three independent bugs, one per file.

**1. Wrong backoff growth: `payments/backoff.py`, `compute_delay`**
The expression was `base * retry_number ** factor`, with base and exponent swapped. The delay grew polynomially (`n²`) instead of exponentially. The first retry still waited `base`, because `1 ** factor == 1`, so the bug only showed from the second retry (0.5, 2.0, 4.5, ... instead of 0.5, 1.0, 2.0, ...). With `factor=1` it looked correct. The fix is `base * factor ** (retry_number - 1)`: the first retry waits `base`, and each further retry multiplies by `factor`. The `min(..., max_delay)` cap stays.

**2. One attempt too many: `payments/policy.py`, `RetryPolicy.should_retry`**
`attempts_made` is the number of requests already sent, and `max_attempts` includes the first request. The check `attempts_made <= self.max_attempts` is still true after the last allowed attempt, so one more request went out. For `max_attempts=3` that gave 4 calls, and the `RetryExhaustedError` reported `attempts=4`. The fix is `attempts_made < self.max_attempts`. With `max_attempts=1` the policy now never retries.

**3. Swallowed non-retryable error: `payments/retry.py`, `call_with_retry`**
When `should_retry` returned False for a non-retryable error (declined card, invalid request), the code logged a warning and then did `return None`. The caller got `None` instead of an exception. `PaymentsClient.charge` then crashed on `Charge.from_response(None)` with a confusing `TypeError`. The fix is to re-raise the original exception with a bare `raise` after logging. It must be the same instance, not wrapped in `RetryExhaustedError`, because it was never retried. Errors that are not `PaymentError`s were never caught by the `except` and still propagate.

## How to find it

- Start with `tests/test_backoff.py::test_delay_doubles_with_each_retry`. The failure message prints the list `[0.5, 2.0, 4.5, ...]`. Reading `compute_delay` shows the swapped base and exponent immediately, with no need to look at the retry loop.
- `test_gives_up_after_max_attempts` says it made 4 calls instead of 3. Follow `call_with_retry` to the only place that decides whether to continue, `RetryPolicy.should_retry`, and check the comparison against the definition of `max_attempts` (the first request counts).
- `test_non_retryable_error_is_raised_immediately` fails with "expected CardDeclinedError" and no exception at all. Print the return value of `call_with_retry`: it is `None`. Read the `except` branch for non-retryable errors and notice that it returns instead of re-raising.
- Fix in this order: bug 1, then bug 2, then bug 3. `test_retries_transient_errors_with_growing_delay` depends on bug 1, so it goes green once the delay is fixed.
