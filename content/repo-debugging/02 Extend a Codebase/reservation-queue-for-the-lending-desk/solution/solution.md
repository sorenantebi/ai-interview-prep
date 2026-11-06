# Reservation queue for the lending desk - Solution

## Root causes / approach
Nothing is broken; this is a feature that has to fit the existing design.

**Invariant.** `Book.available` counts only copies that can be borrowed by anyone. A copy that has been returned but set aside for a hold is *not* counted, so the existing `checkout` check `available < 1` already keeps strangers from taking it. Every copy that becomes free goes through one helper, `_release_copy(isbn)`: if a hold is waiting, it becomes ready (`ready_at = now`, `expires_at = now + HOLD_DAYS`), otherwise `available += 1`. Returns, expiries and cancellations of ready holds all use it, so the "queue first, shelf second" rule lives in one place.

**`library/holds.py`.** `HoldQueue` is a dict `isbn -> list[Hold]` in placement order, with `add`, `get`, `remove`, `position`, `first_waiting` and `expired`. Ready holds are always a prefix of the list (a copy is only ever given to the *first waiting* hold), so `first_waiting` is a linear scan that stops at the first non-ready hold. `expired` uses `expires_at <= now`, which makes exactly 3 days already expired.

**`library/service.py`.**
- `expire_holds()` first removes all expired holds, then releases one copy per removed hold. Releasing after removing matters when several holds expire together, because a freed copy must never be handed to a hold that is about to be dropped. A newly ready hold gets `expires_at` in the future, so the cascade cannot loop.
- `checkout` and `return_book` call `expire_holds()` first, so an expired hold never wins a race against a lazy sweep. In `checkout`, a ready hold is consumed without decrementing `available` (the copy was never counted); otherwise the old path applies. The loan-limit and already-borrowed checks run before the hold is consumed, so a failed collection keeps the hold.
- `return_book` returns the `Hold` that received the copy or `None`.
- `place_hold` rejects available books, current borrowers and duplicate holds. `cancel_hold` hands a ready hold's copy on. `hold_position` delegates to the queue.

Complexity: every operation scans one ISBN queue and `expire_holds` scans all queues, i.e. O(total holds). That is fine for a desk-sized system; an index of ready holds by expiry (a heap) would be the next step if it ever mattered.

## How to find it
Start with `tests/test_holds.py` and the first failure: `AttributeError: place_hold`. That tells you the service API is missing. Read `service.py` and `models.py` before writing anything: `Hold` already has `is_ready`, `ready_at` and `expires_at`, `HOLD_DAYS` already exists in `utils.py`, and `Clock` is the only source of time. Work through the tests in order: queue first (`holds.py`), then `place_hold` / `return_book`, then collection in `checkout`, then expiry. Before finishing, list the edge cases the notes imply: the exact 3-day boundary, expiry noticed lazily by `checkout`, several copies of one title, cancelling a waiting hold versus a ready one, and a holder who is at the loan limit.
