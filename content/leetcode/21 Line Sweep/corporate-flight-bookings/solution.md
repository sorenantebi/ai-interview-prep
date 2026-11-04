---
topic: "Line Sweep"
difficulty: Medium
leetcode: https://leetcode.com/problems/corporate-flight-bookings/
---
# Corporate Flight Bookings - Solution

## Intuition

Adding `seats` to every flight in a range one by one is wasteful. Instead, record only where the range starts (the running total goes up) and where it ends (the running total goes down). A prefix sum over these change points then yields the total for every flight. This is a difference array, a form of line sweep.

## Approach

1. Create an array `diff` of size `n + 1`, all zeros.
2. For each booking `[first, last, seats]`, add `seats` at index `first - 1` and subtract `seats` at index `last` (the flight just after the range; the extra slot keeps `last == n` in bounds).
3. Sweep left to right over `diff`, keeping a running sum. The running sum at index `i` is the answer for flight `i + 1`.
4. Return the first `n` entries.

## Code

```python
from typing import List, Optional

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        diff = [0] * (n + 1)
        for first, last, seats in bookings:
            diff[first - 1] += seats
            diff[last] -= seats

        answer = []
        total = 0
        for i in range(n):
            total += diff[i]
            answer.append(total)
        return answer
```

## Complexity

- **Time:** `O(n + m)` — each of the `m` bookings is handled in constant time, then one pass over `n` flights.
- **Space:** `O(n)` — the difference array (the output array is also of size `n`).

## Other Approaches

- **Brute force:** for each booking, add `seats` to every flight in its range — Time `O(n * m)` / Space `O(1)` extra
- **Sorted events sweep:** turn each booking into start/end events, sort them, and sweep — Time `O(m log m + n)` / Space `O(m)`
