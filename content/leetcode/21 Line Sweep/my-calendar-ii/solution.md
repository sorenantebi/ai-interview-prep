---
topic: "Line Sweep"
difficulty: Medium
leetcode: https://leetcode.com/problems/my-calendar-ii/
---
# My Calendar II - Solution

## Intuition

A triple booking occurs exactly when a new event overlaps a region that is already double booked. So it is enough to track two things: all booked events, and the set of intervals that are covered twice. A new event is rejected if it intersects any double-booked interval; otherwise it is safe, and its overlaps with the existing single bookings become new double-booked intervals.

## Approach

1. Keep a list `calendar` of all accepted events and a list `overlaps` of double-booked intervals.
2. In `book(start, end)`, check every interval in `overlaps`. If `start < o_end and end > o_start`, a triple booking would occur, so return `false`.
3. Otherwise, for each event in `calendar`, if it overlaps `[start, end)`, add the intersection `[max(starts), min(ends))` to `overlaps`.
4. Append the new event to `calendar` and return `true`.

Because step 2 guarantees the new event does not touch any existing double-booked interval, the intervals in `overlaps` never overlap one another, so step 3 stays correct.

## Code

```python
from typing import List, Optional

class MyCalendarTwo:

    def __init__(self):
        self.calendar = []
        self.overlaps = []

    def book(self, startTime: int, endTime: int) -> bool:
        for s, e in self.overlaps:
            if startTime < e and endTime > s:
                return False
        for s, e in self.calendar:
            if startTime < e and endTime > s:
                self.overlaps.append((max(s, startTime), min(e, endTime)))
        self.calendar.append((startTime, endTime))
        return True


# Your MyCalendarTwo object will be instantiated and called as such:
# obj = MyCalendarTwo()
# param_1 = obj.book(startTime, endTime)
```

## Complexity

- **Time:** `O(n)` per `book` call, `O(n^2)` overall — each call scans the `calendar` and `overlaps` lists, both of size at most `n`.
- **Space:** `O(n)` — the two lists hold at most `n` events and `n` overlap intervals.

## Other Approaches

- **Line sweep with an ordered map:** store `+1` at starts and `-1` at ends, sweep in sorted order and reject if the running count reaches 3 (then undo the change) — Time `O(n^2)` overall with re-sorting per call (`O(n)` per call with a sorted structure plus scan) / Space `O(n)`
- **Segment tree with lazy propagation:** dynamic range-add and range-max over coordinates up to `10^9`, reject if the max would reach 3 — Time `O(log C)` per call / Space `O(n log C)`
