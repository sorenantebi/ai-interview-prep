---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/my-calendar-iii/
---
# My Calendar III - Solution

## Intuition

The maximum number of overlapping events is the maximum prefix sum of a difference array: add `+1` at each start and `-1` at each end. Because times go up to `10^9`, we can't use an array, but we only need the sparse set of boundary points. With at most 400 calls, that is at most 800 points.

## Approach

1. Keep a sorted map from time to delta, `+1` at `startTime` and `-1` at `endTime`.
2. On each `book`, update the two entries, keeping the keys in sorted order (via `bisect.insort` on a list of keys).
3. Sweep through the keys in order, accumulating the running sum of deltas.
4. Return the maximum running sum seen.

## Code

```python
from typing import List, Optional
from bisect import insort

class MyCalendarThree:

    def __init__(self):
        self.delta = {}
        self.times = []

    def book(self, startTime: int, endTime: int) -> int:
        for t, d in ((startTime, 1), (endTime, -1)):
            if t not in self.delta:
                self.delta[t] = 0
                insort(self.times, t)
            self.delta[t] += d
        best = cur = 0
        for t in self.times:
            cur += self.delta[t]
            best = max(best, cur)
        return best
```

## Complexity

- **Time:** `O(n)` per `book` call, `O(n^2)` overall — each call sweeps up to `2n` boundary points (insertion into the sorted list is also `O(n)`).
- **Space:** `O(n)` — at most `2n` distinct boundary points are stored.

## Other Approaches

- **Dynamic segment tree with lazy propagation:** range add `+1` and track the global max — Time `O(log C)` per call amortized / Space `O(n log C)`, where `C = 10^9`.
- **Brute-force overlap counting:** for each new event, recount overlaps at every boundary point — Time `O(n^2)` per call / Space `O(n)`.
