---
video: https://www.youtube.com/watch?v=BGgYC-YkGvc
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-in-mountain-array/
neetcode: https://neetcode.io/problems/find-in-mountain-array
---
# Find in Mountain Array

**Topic:** Binary Search · **Difficulty:** Hard

## Problem

An array `arr` is a *mountain array* if and only if:

- `arr.length >= 3`
- There exists some index `i` with `0 < i < arr.length - 1` such that:
  - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
  - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`

You are given a mountain array `mountainArr` and an integer `target`. Return the minimum index such that `mountainArr.get(index) == target`. If no such index exists, return `-1`.

This is an interactive problem: you cannot access the array directly, only through the `MountainArray` interface:

- `MountainArray.get(k)` returns the element at index `k` (0-indexed).
- `MountainArray.length()` returns the length of the array.

Solutions that make more than 100 calls to `MountainArray.get` are judged Wrong Answer. Attempts to circumvent the judge result in disqualification.

## Examples

**Example 1**
```text
Input: mountainArr = [1,2,3,4,5,3,1], target = 3
Output: 2
Explanation: 3 exists in the array at index 2 and index 5. Return the minimum index, which is 2.
```

**Example 2**
```text
Input: mountainArr = [0,1,2,4,2,1], target = 3
Output: -1
Explanation: 3 does not exist in the array, so return -1.
```

## Constraints

- `3 <= mountainArr.length() <= 10^4`
- `0 <= target <= 10^9`
- `0 <= mountainArr.get(index) <= 10^9`
