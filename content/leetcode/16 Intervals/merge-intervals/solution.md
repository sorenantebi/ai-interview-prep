---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/merge-intervals/
neetcode: https://neetcode.io/problems/merge-intervals
---
# Merge Intervals - Solution

**Question:** Merge Intervals - Question · **Difficulty:** Medium

## Intuition

After sorting by start, any interval that overlaps the current merged block must come right after it — an interval can only overlap the last block if its start is `<=` that block's end. So one pass over the sorted list either extends the last block or starts a new one.

## Approach

1. Sort intervals by start.
2. Initialize `res` with the first interval.
3. For each next interval `[s, e]`: if `s <= res[-1][1]`, set `res[-1][1] = max(res[-1][1], e)`; otherwise append `[s, e]`.
4. Return `res`.

## Code

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda pair: pair[0])
        output = [intervals[0]]

        for start, end in intervals:
            lastEnd = output[-1][1]

            if start <= lastEnd:
                # merge
                output[-1][1] = max(lastEnd, end)
            else:
                output.append([start, end])
        return output
```

## Complexity

- **Time:** `O(n log n)` — dominated by sorting; the merge pass is `O(n)`.
- **Space:** `O(n)` for the output (plus `O(n)` used by Python's sort).

## Other Approaches

- **Sweep over endpoints / counting array:** mark +1 at starts and -1 after ends over the coordinate range and read off covered segments — Time `O(n + V)` where `V` is the value range, Space `O(V)`; fiddly with touching endpoints.
- **Graph of overlapping intervals + connected components:** Time `O(n^2)`, Space `O(n^2)`.

## Key Takeaway

Sort by start, then greedily extend the last merged interval with `max(end)` — the template for most interval problems.
