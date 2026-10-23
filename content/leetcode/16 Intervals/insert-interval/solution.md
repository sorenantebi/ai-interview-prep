---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/insert-interval/
neetcode: https://neetcode.io/problems/insert-new-interval
---
# Insert Interval - Solution

**Question:** Insert Interval - Question · **Difficulty:** Medium

## Intuition

Because the input is sorted and disjoint, it splits into three consecutive groups relative to `newInterval`: intervals that end before it starts (copy as-is), intervals that overlap it (absorb them by widening `newInterval`), and intervals that start after it ends (copy as-is). One linear scan handles all three.

## Approach

1. Copy every interval with `end < newInterval.start` to the result.
2. While the current interval has `start <= newInterval.end`, merge: `newInterval = [min(starts), max(ends)]`.
3. Append the merged `newInterval`.
4. Copy all remaining intervals.

## Code

```python
class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        res = []

        for i in range(len(intervals)):
            if newInterval[1] < intervals[i][0]:
                res.append(newInterval)
                return res + intervals[i:]
            elif newInterval[0] > intervals[i][1]:
                res.append(intervals[i])
            else:
                newInterval = [
                    min(newInterval[0], intervals[i][0]),
                    max(newInterval[1], intervals[i][1]),
                ]
        res.append(newInterval)
        return res
```

## Complexity

- **Time:** `O(n)` — single pass over the intervals.
- **Space:** `O(n)` for the output list; `O(1)` extra besides it.

## Other Approaches

- **Append then Merge Intervals:** add `newInterval`, sort, and run the standard merge — Time `O(n log n)`, Space `O(n)`.
- **Binary search for the insertion window:** find the first/last overlapping indices with `bisect` — still `O(n)` overall because the output must be built.

## Key Takeaway

With sorted, disjoint intervals, think "before / overlapping / after": the overlap condition is `a.start <= b.end and b.start <= a.end`.
