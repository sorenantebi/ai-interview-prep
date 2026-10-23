---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/meeting-rooms-ii/
neetcode: https://neetcode.io/problems/meeting-schedule-ii
---
# Meeting Rooms II

**Topic:** Intervals · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/meeting-rooms-ii/) · [NeetCode](https://neetcode.io/problems/meeting-schedule-ii)

## Problem

Given an array of meeting time intervals `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms needed to hold all meetings so that no two meetings in the same room overlap. A meeting ending at time `t` frees its room for a meeting starting at time `t`.

## Examples

**Example 1**
```text
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
```

**Example 2**
```text
Input: intervals = [[7,10],[2,4]]
Output: 1
```

**Example 3**
```text
Input: intervals = [[1,5],[2,6],[3,7],[5,8]]
Output: 3
```

## Constraints

- `1 <= intervals.length <= 10^4`
- `0 <= start_i < end_i <= 10^6`
