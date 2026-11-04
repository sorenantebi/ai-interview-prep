---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/number-of-flowers-in-full-bloom/
---
# Number of Flowers in Full Bloom - Solution

## Intuition

At time `t`, the number of flowers in bloom equals the number of flowers that have started by `t` minus the number that have already ended before `t`. Both counts can be found with binary search on sorted arrays of start times and end times.

## Approach

1. Build a sorted list `starts` of all start times and a sorted list `ends` of all end times.
2. For each person arriving at time `t`, count flowers with `start <= t` using `bisect_right(starts, t)`.
3. Count flowers with `end < t` using `bisect_left(ends, t)`.
4. The answer for that person is the difference of the two counts.

## Code

```python
from typing import List, Optional
from bisect import bisect_left, bisect_right

class Solution:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:
        starts = sorted(s for s, _ in flowers)
        ends = sorted(e for _, e in flowers)
        # started by t, minus finished strictly before t (end is inclusive)
        return [bisect_right(starts, t) - bisect_left(ends, t) for t in people]
```

## Complexity

- **Time:** `O((F + P) log F)` — sorting the two arrays costs `O(F log F)`, and each of the `P` people needs two binary searches.
- **Space:** `O(F)` — the sorted start and end arrays (excluding the output).

## Other Approaches

- **Sweep with events and sorted queries:** sort flower events and people, sweep through time while maintaining a running count of active flowers — Time `O((F + P) log (F + P))` / Space `O(F + P)`
- **Min-heap of end times:** sort flowers by start and people by arrival, push end times into a heap and pop those that ended before the person arrives — Time `O((F + P) log F)` / Space `O(F + P)`
- **Brute force:** for each person, scan all flowers — Time `O(F · P)` / Space `O(1)`
