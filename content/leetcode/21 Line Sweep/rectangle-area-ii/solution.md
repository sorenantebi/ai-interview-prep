---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/rectangle-area-ii/
---
# Rectangle Area II - Solution

## Intuition

Sweep a vertical line from left to right. Between two consecutive x-coordinates where something starts or ends, the set of rectangles crossing the line does not change. The covered area in that vertical strip is therefore `(strip width) * (length of the union of the active y-intervals)`. Summing over all strips gives the union area.

## Approach

1. Turn each rectangle into two events: an "open" event at `x1` and a "close" event at `x2`, both carrying the interval `[y1, y2]`.
2. Sort the events by x.
3. Keep a list of active y-intervals, sorted by start, and the current covered y-length.
4. For each event, first add `covered_length * (x - prev_x)` to the area, since the active set was constant over that strip.
5. Then insert or remove the event's interval and recompute the covered y-length by merging the sorted intervals in one linear pass.
6. Return the accumulated area modulo `10^9 + 7`. Python integers are exact, so the modulus is applied only once at the end.

## Code

```python
from typing import List
from bisect import insort

class Solution:
    def rectangleArea(self, rectangles: List[List[int]]) -> int:
        MOD = 10**9 + 7
        events = []
        for x1, y1, x2, y2 in rectangles:
            events.append((x1, 1, y1, y2))
            events.append((x2, -1, y1, y2))
        events.sort()

        active = []
        covered = 0
        area = 0
        prev_x = events[0][0]
        for x, kind, y1, y2 in events:
            area += covered * (x - prev_x)
            prev_x = x
            if kind == 1:
                insort(active, (y1, y2))
            else:
                active.remove((y1, y2))

            # merge sorted intervals to get the union length
            covered = 0
            end = 0
            for a, b in active:
                if b > end:
                    covered += b - max(a, end)
                    end = b
        return area % MOD
```

## Complexity

- **Time:** `O(n^2)` — there are `2n` events, and each one triggers an `O(n)` insert/remove and an `O(n)` merge over the active intervals.
- **Space:** `O(n)` — the event list and the active interval list.

## Other Approaches

- **Segment tree sweep:** sweep over x and keep a segment tree on compressed y-coordinates that stores the covered length — Time `O(n log n)` / Space `O(n)`
- **Coordinate compression with a grid:** compress x and y, mark every covered cell, and sum the areas of the marked cells — Time `O(n^3)` / Space `O(n^2)`
- **Inclusion-exclusion over rectangles:** add and subtract the areas of intersections of every subset — Time `O(2^n)` / Space `O(n)` (too slow here)
