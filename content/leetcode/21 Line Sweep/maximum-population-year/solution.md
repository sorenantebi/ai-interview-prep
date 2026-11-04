---
topic: "Line Sweep"
difficulty: Easy
leetcode: https://leetcode.com/problems/maximum-population-year/
---
# Maximum Population Year - Solution

## Intuition

The population only changes at birth and death years. A birth adds one person starting that year, and a death removes one person starting that year (since the person is not counted in their death year). Recording these changes and sweeping through the years in order gives the population of every year with a running sum.

## Approach

1. Create a difference array `delta` covering years 1950 through 2050.
2. For each log, add 1 at the birth year and subtract 1 at the death year.
3. Sweep the years in increasing order, keeping a running sum as the current population.
4. Track the maximum population seen; update the answer only on a strictly greater value, so the earliest year wins ties.
5. Return the recorded year.

## Code

```python
from typing import List, Optional

class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        start = 1950
        delta = [0] * 101
        for birth, death in logs:
            delta[birth - start] += 1
            delta[death - start] -= 1

        best_year = start
        best = 0
        alive = 0
        for i, change in enumerate(delta):
            alive += change
            if alive > best:  # strict, so ties keep the earliest year
                best = alive
                best_year = start + i
        return best_year
```

## Complexity

- **Time:** `O(n + Y)` — one pass over the logs plus one pass over the fixed range of `Y = 101` years.
- **Space:** `O(Y)` — the difference array has a fixed size of 101, independent of `n`.

## Other Approaches

- **Brute force counting:** for each year in the range, count how many logs contain it — Time `O(n * Y)` / Space `O(1)`
- **Sorted events:** sort birth and death years separately and sweep with two pointers — Time `O(n log n)` / Space `O(n)`
