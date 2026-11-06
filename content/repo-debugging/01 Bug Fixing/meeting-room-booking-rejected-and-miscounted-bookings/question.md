---
difficulty: Medium
kind: bug-fix
---
# Meeting-room booking: rejected and miscounted bookings

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
`rooms` is a small booking service used by the office team to reserve meeting rooms and to produce daily usage reports. Since last week, people complain that a meeting which starts exactly when the previous one in the same room ends is refused as "overlapping", and that an evening booking running until midnight cannot be made at all. The facility manager also says the utilization numbers in the daily report look too low whenever meetings last longer than a whole number of hours.

## Your tasks
1. Users report that back-to-back bookings in the same room are rejected as conflicts. Find and fix the cause (the failing tests show the symptoms).
2. Users report that a booking ending at midnight (for example 23:00 to 00:00 the next day) is refused. Find and fix the cause.
3. The daily report undercounts booked time for meetings such as 90 minutes. Find and fix the cause.
4. Make sure all visible tests pass without changing the tests, and think about edge cases the hidden tests may probe.

## Notes
- Entry point is `rooms/service.py` (`BookingService`); `rooms/report.py` builds reports on top of it.
- All times are naive `datetime` objects in office-local time. A booking is a half-open interval: it occupies `[start, end)`.
- Rooms are closed overnight, so a booking may not run past the midnight that follows its start, but it may end exactly at that midnight.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
