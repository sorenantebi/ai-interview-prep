# Meeting-room booking: rejected and miscounted bookings - Solution

## Root causes / approach

**1. Back-to-back bookings rejected - `rooms/models.py`, `Booking.overlaps`.**
The overlap test used `<=` on both sides, which treats intervals that merely touch (one ends at 10:00, the next starts at 10:00) as overlapping. Bookings are half-open `[start, end)`, so touching is fine. The fix is strict comparison: `self.start < other.end and other.start < self.end`. This also fixed `free_slots` tests that book adjacent slots.

**2. Booking ending at midnight refused - `rooms/timeutils.py`, `fits_in_day`.**
The helper compared calendar dates (`start.date() == end.date()`). A booking 23:00 to 00:00 ends on the next calendar date, so it was rejected with `ValueError`, even though the rules allow ending exactly at the midnight that follows the start. The fix compares against the boundary instead: `end <= next_midnight(start)`. A booking ending one second after midnight is still rejected, and a full 00:00 to 24:00 booking is allowed.

**3. Report undercounts fractional hours - `rooms/report.py`, `hours_booked`.**
Each duration was converted with `timedelta.seconds // 3600`. Integer division drops the minutes of every booking (90 minutes became 1 hour), and `.seconds` is only the seconds component of the timedelta, so it would also wrap for durations of 24 hours or more. The fix sums `total_seconds()` and divides once with true division: `sum(...) / 3600`. Utilization and `summary` are computed from it, so they are corrected too.

## How to find it
- Start with `test_back_to_back_bookings_allowed`. The error is a `ConflictError` for bookings that touch, so go to the only place that decides overlap, `Booking.overlaps`, and check the comparison operators against the half-open rule in the notes.
- `test_booking_ending_at_midnight_allowed` raises `ValueError("a booking must not run past midnight")`. That message comes from `BookingService.book`, which delegates to `fits_in_day`. Print `end.date()` for a 00:00 end time to see why the date comparison fails.
- For the report tests, the failing assert shows 1 instead of 1.5. Print `b.duration.seconds` and the result of `// 3600` for a 90-minute booking to see where the half hour goes.
- After fixing, re-run and then think through edge cases: 24-hour bookings, a booking one second past midnight, ties in `summary`, and bookings before opening time in `free_slots`.
