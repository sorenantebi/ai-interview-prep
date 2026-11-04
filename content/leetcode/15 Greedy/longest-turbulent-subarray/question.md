---
video: https://www.youtube.com/watch?v=V_iHUhR8Dek
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-turbulent-subarray/
neetcode: https://neetcode.io/problems/longest-turbulent-subarray
---
# Longest Turbulent Subarray

**Topic:** Greedy · **Difficulty:** Medium

## Problem

Given an integer array `arr`, return the length of the longest turbulent subarray.

A subarray is turbulent if the comparison sign strictly alternates between each pair of adjacent elements. Formally, a subarray `[arr[i], arr[i + 1], ..., arr[j]]` is turbulent if either:

- for every `i <= k < j`, `arr[k] > arr[k + 1]` when `k` is odd and `arr[k] < arr[k + 1]` when `k` is even; or
- for every `i <= k < j`, `arr[k] > arr[k + 1]` when `k` is even and `arr[k] < arr[k + 1]` when `k` is odd.

Equal adjacent elements break turbulence. A subarray of length 1 is always turbulent.

## Examples

**Example 1**
```text
Input: arr = [9,4,2,10,7,8,8,1,9]
Output: 5
Explanation: arr[1] > arr[2] < arr[3] > arr[4] < arr[5]
```

**Example 2**
```text
Input: arr = [4,8,12,16]
Output: 2
```

**Example 3**
```text
Input: arr = [100]
Output: 1
```

## Constraints

- `1 <= arr.length <= 4 * 10^4`
- `0 <= arr[i] <= 10^9`
