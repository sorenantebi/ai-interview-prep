---
video: https://www.youtube.com/watch?v=o-YDQzHoaKM
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/find-k-closest-elements/
neetcode: https://neetcode.io/problems/find-k-closest-elements
---
# Find K Closest Elements

**Topic:** Sliding Window · **Difficulty:** Medium

## Problem

You are given a sorted integer array `arr` and two integers `k` and `x`. Return the `k` integers in the array that are closest to `x`. The result must be sorted in ascending order.

An integer `a` is closer to `x` than an integer `b` if:

- `|a - x| < |b - x|`, or
- `|a - x| == |b - x|` and `a < b`

## Examples

**Example 1**
```text
Input: arr = [1,2,3,4,5], k = 4, x = 3
Output: [1,2,3,4]
```

**Example 2**
```text
Input: arr = [1,1,2,3,4,5], k = 4, x = -1
Output: [1,1,2,3]
```

## Constraints

- `1 <= k <= arr.length`
- `1 <= arr.length <= 10^4`
- `arr` is sorted in ascending order.
- `-10^4 <= arr[i], x <= 10^4`
