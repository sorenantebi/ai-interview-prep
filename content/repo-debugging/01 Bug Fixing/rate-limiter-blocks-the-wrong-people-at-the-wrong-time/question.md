---
difficulty: Medium
kind: bug-fix
---
# Rate limiter blocks the wrong people at the wrong time

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
`ratelimit` is the small sliding-window limiter that sits in front of our public API. Support has opened three complaints. Customers who make exactly one request per window are intermittently rejected, even though they are within their quota. Two users of the same organisation say they "use up each other's quota". After the platform team gave the `export` endpoint a stricter limit, other services in the same process started seeing that limit as well.

## Your tasks
1. Run the visible tests and read the failures. They show the symptoms but not the causes.
2. Find the root cause of each problem and fix it with a minimal, targeted change. Do not rewrite modules or change public signatures.
3. Make sure your fixes also behave sensibly for cases the visible tests don't cover. Hidden tests exercise ids without an organisation, identical names in different organisations, and repeated requests at exact window boundaries.

## Notes
- Entry point: `Gateway.handle(user_id, endpoint, now)` in `ratelimit/gateway.py`. It delegates to `RateLimiter.check`. Time is always passed in as `now` (seconds, float); nothing reads the system clock.
- User ids look like `"org/name"` (e.g. `"acme/alice"`). Ids without a slash (e.g. `"solo"`) are valid and have no organisation.
- Quota is tracked per user, per endpoint. A request that is denied must not count against the quota.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
