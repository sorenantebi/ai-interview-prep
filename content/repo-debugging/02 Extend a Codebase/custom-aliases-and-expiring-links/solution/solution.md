# Custom aliases and expiring links - Solution

## Root causes / approach

**Alias validation (`shortener/validation.py`).** Add `validate_alias` next to `validate_url`, so all input checks stay in one module.
- Use `re.fullmatch` with `[A-Za-z0-9_-]{3,32}`. `re.match` with `$` would accept a trailing newline (`"abc\n"`), and `str.isalnum()` would accept non-ASCII letters such as `é`.
- Reject non-strings, then check the reserved names (`api`, `admin`, `static`, `health`) with `alias.lower()`, because reserved names are case-insensitive while aliases are otherwise case-sensitive.

**Expiry on the record (`shortener/storage.py`).** Add `expires_at: Optional[float] = None` to `LinkRecord` and an `is_expired(now)` method.
- The comparison is `now >= expires_at`, because a link must already be expired at exactly `created_at + ttl`.
- Keeping this on the record means `resolve`, `stats`, `purge_expired` and alias claiming all share one definition of "expired".

**Service (`shortener/service.py`).**
- `shorten(url, alias=None, ttl=None)` validates everything first: URL, then alias, then ttl (`ValueError` if it is `<= 0`). Only after that does it read the clock, claim the alias or generate a code, and add the record. Rejected calls therefore change nothing and don't use up a sequence number. A custom alias never calls `_generate_code`, so the sequence stays gapless.
- `_claim_alias` raises `AliasTakenError` if a live record holds the alias. If the holder is expired, it deletes it first, because `LinkStore.add` refuses duplicates. This gives "expired links don't block aliases" and a fresh record with `hits == 0`.
- `_generate_code` now loops until it finds a code that is not in the store. Without this, a user alias such as `1000` would make the generator hit `AliasTakenError` (or silently clobber the alias with a different store). The counter keeps advancing, so the loop is amortised O(1).
- `_get_live` is the single lookup used by `resolve` and `stats`: `LinkNotFoundError` if missing, `LinkExpiredError` if expired. The hit counter is only incremented after it succeeds, so expired links record no hits.
- `purge_expired` takes one `now` reading, collects the expired codes from `store.records()` (a snapshot, so deleting while iterating is safe) and deletes them. It returns the count. A later lookup raises `LinkNotFoundError`.
- Time always comes from `self._clock.now()`, so the tests can drive expiry with `FakeClock`.

Complexity: `shorten`, `resolve` and `stats` are O(1). `purge_expired` is O(n) over the stored links.

## How to find it
1. Run the tests and read the failures in `test_aliases.py` and `test_expiry.py`: they fail with `TypeError: shorten() got an unexpected keyword argument`, which shows the signature is the first thing to change.
2. Read `service.py` end to end. It is short, and it shows the flow validate, generate, store, and the places each feature plugs in.
3. Read `storage.py` and `errors.py`. `LinkStore.add` already raises `AliasTakenError`, and the exception classes you need are already declared. Note that `delete` and `records` exist for purging.
4. Notice that `_generate_code` blindly increments a counter. Ask what happens if an alias equals a future code (the visible test `test_generated_code_never_overwrites_an_alias` targets this), and make it skip taken codes.
5. Read the requirements for boundaries: expiry at exactly `ttl` means `>=`, an alias is reusable after expiry, and an expired link counts no hit. Then check the order of validation so rejected calls leave no trace.
