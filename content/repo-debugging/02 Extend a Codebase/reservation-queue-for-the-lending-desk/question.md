---
difficulty: Medium
kind: extend
---
# Reservation queue for the lending desk

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
The `library` package backs the front desk of a small public library: staff check books out to members, take them back, and list overdue loans. Popular titles are always out, and members keep asking the desk to "put their name down". You are asked to add a reservation queue (holds): when a book is returned, it must go to the first person waiting instead of back on the shelf, and a member who doesn't pick it up within 3 days loses the hold.

## Your tasks
1. Implement `HoldQueue` in `library/holds.py` (the class is stubbed out, every method raises `NotImplementedError`). It keeps one FIFO queue of `Hold` objects per ISBN.
2. Extend `LendingService` in `library/service.py` with the public methods `place_hold(member_id, isbn)`, `cancel_hold(member_id, isbn)`, `hold_position(member_id, isbn)` and `expire_holds()`, and change `return_book` and `checkout` so that holds are honoured (rules below).
3. Make the failing tests in `tests/test_holds.py` pass without breaking `tests/test_lending.py`. Then think about edge cases the visible tests do not cover; the hidden tests do.

## Notes
- Rules for holds:
  - `place_hold` returns the new `Hold`. It raises `HoldError` if the book still has an available copy (the member should just borrow it), if the member currently has the book on loan, or if the member already has a hold on it. Unknown ids raise the existing `UnknownMember` / `UnknownBook`.
  - `return_book` still restores a copy to the shelf when nobody is waiting. If somebody is waiting, the copy is *not* added to `Book.available`. It is set aside for the first waiting hold, which becomes *ready*: `ready_at` is the current clock time and `expires_at` is `ready_at` + `HOLD_DAYS` (3 days). `return_book` returns that `Hold`, or `None` when the copy went back on the shelf.
  - Only the holder of a ready hold may check out the reserved copy. Collecting it removes the hold, does not touch `Book.available`, and creates a normal loan (the usual loan limit and "already borrowed" checks still apply; a failed collection leaves the hold in place). Everyone else gets `NoCopiesAvailable` while no copy is available.
  - A ready hold is expired as soon as `now >= expires_at`. `expire_holds()` removes every expired hold, passes each freed copy on to the next waiting hold (which becomes ready at the current time) or back to the shelf, and returns the list of expired holds. `place_hold`, `cancel_hold`, `hold_position`, `checkout` and `return_book` must treat expired holds as gone even if nobody called `expire_holds()` explicitly.
  - `cancel_hold` removes the member's hold (`HoldError` if there is none). Cancelling a *ready* hold passes its copy on like an expiry does.
  - `hold_position` is the 1-based position in the ISBN's queue, counting ready holds too (`HoldError` if there is no hold).
  - A book may have several copies, so several holds of one ISBN can be ready at the same time; ready holds always sit at the front of their queue.
- Time comes from `Clock` (`library/utils.py`); tests move it with `clock.advance(...)`. Don't call `datetime.now()` directly.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
