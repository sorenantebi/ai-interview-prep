---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/non-overlapping-intervals/
neetcode: https://neetcode.io/problems/non-overlapping-intervals
---
# Non Overlapping Intervals

**Topic:** Intervals · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/non-overlapping-intervals/) · [NeetCode](https://neetcode.io/problems/non-overlapping-intervals)

## Problem

Given an array of intervals `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you must delete so that the remaining intervals are pairwise non-overlapping. Intervals that only touch at a single endpoint (e.g. `[1,2]` and `[2,3]`) are **not** considered overlapping.

## Examples

**Example 1**
```text
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: removing [1,3] leaves [1,2],[2,3],[3,4].
```

**Example 2**
```text
Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
```

**Example 3**
```text
Input: intervals = [[1,2],[2,3]]
Output: 0
```

## Constraints

- `1 <= intervals.length <= 10^5`
- `intervals[i].length == 2`
- `-5 * 10^4 <= start_i < end_i <= 5 * 10^4`
