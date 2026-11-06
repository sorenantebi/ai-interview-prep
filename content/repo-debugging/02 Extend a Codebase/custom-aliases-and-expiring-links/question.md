---
difficulty: Medium
kind: extend
---
# Custom aliases and expiring links

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
Our internal URL shortener hands out sequential codes such as `1000`, `1001`, ... and keeps every link forever. The marketing team wants memorable custom aliases (`/spring-sale`) and campaign links that stop working after a while. You are extending the existing `shortener` package to support both. The existing tests pass today, and the new tests in `tests/test_aliases.py` and `tests/test_expiry.py` fail until the features are built.

## Your tasks
1. **Custom aliases.** `ShortenerService.shorten` should accept an optional `alias`. If it is given, the alias becomes the short code instead of a generated one.
   - A valid alias is 3 to 32 characters long and uses only ASCII letters, digits, `-` and `_`. Aliases are case-sensitive, so `Docs` and `docs` are different aliases.
   - The names `api`, `admin`, `static` and `health` are reserved. They are rejected whatever their case (`API` is rejected too).
   - An invalid alias raises `InvalidAliasError`. An alias that is already in use by a live link raises `AliasTakenError` and leaves the existing link untouched.
   - Generated codes must never collide with an alias or overwrite one, even when someone registers an alias that looks like a code that has not been generated yet (for example `1000`).
2. **Link expiry.** `shorten` should also accept an optional `ttl` (seconds, int or float). Use the service's injected clock, never `time.time()` directly.
   - `ttl` must be positive, otherwise raise `ValueError`. Without a `ttl` the link never expires.
   - A link expires exactly `ttl` seconds after it was created. At that instant it is already expired.
   - `resolve` and `stats` on an expired link raise `LinkExpiredError`, and an expired link does not count a hit.
   - `stats` should expose the expiry time as `expires_at` (`None` for links that don't expire).
   - An expired link no longer blocks its alias: shortening with that alias again replaces the old link with a fresh one.
   - Add `ShortenerService.purge_expired()`, which deletes all expired links from storage and returns how many it removed. Afterwards those codes raise `LinkNotFoundError`.

## Notes
- Entry point: `shortener/service.py`. Validation lives in `shortener/validation.py`, persistence in `shortener/storage.py`, and the clocks in `shortener/clock.py`. The exception classes you need are already declared in `shortener/errors.py`.
- Follow the existing structure and put each piece where the existing code would put it.
- Input is validated before anything is stored or any generated code is used up. Check the URL first, then the alias. A rejected call must leave the service unchanged. Generated codes stay sequential, and a custom alias does not use up a sequence number.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
