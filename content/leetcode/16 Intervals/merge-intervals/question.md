---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/merge-intervals/
neetcode: https://neetcode.io/problems/merge-intervals
---
# Merge Intervals

**Topic:** Intervals · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/merge-intervals/) · [NeetCode](https://neetcode.io/problems/merge-intervals)

## Problem

Given an array `intervals` where `intervals[i] = [start_i, end_i]`, merge every group of overlapping intervals into a single interval and return the resulting array of non-overlapping intervals that together cover exactly the same points. Intervals that touch at an endpoint (e.g. `[1,4]` and `[4,5]`) are considered overlapping. The answer may be returned in any order.

## Examples

**Example 1**
```text
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

**Example 2**
```text
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
```

**Example 3**
```text
Input: intervals = [[4,7],[1,4]]
Output: [[1,7]]
```

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`
