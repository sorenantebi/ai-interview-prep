---
video: https://www.youtube.com/watch?v=fxT9KjakYPM
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/maximum-sum-circular-subarray/
neetcode: https://neetcode.io/problems/maximum-sum-circular-subarray
---
# Maximum Sum Circular Subarray

**Topic:** Greedy · **Difficulty:** Medium

## Problem

You are given a circular integer array `nums` of length `n`, meaning the last element is followed by the first one. Formally, the next element of `nums[i]` is `nums[(i + 1) % n]` and the previous element of `nums[i]` is `nums[(i - 1 + n) % n]`.

Return the maximum possible sum of a non-empty subarray of this circular array.

A subarray may use each element of the underlying array at most once. That is, for a subarray `nums[i], nums[i + 1], ..., nums[j]`, there are no indices `k1`, `k2` in `[i, j]` with `k1 % n == k2 % n`.

## Examples

**Example 1**
```text
Input: nums = [1,-2,3,-2]
Output: 3
```
Explanation: The subarray `[3]` has the maximum sum 3.

**Example 2**
```text
Input: nums = [5,-3,5]
Output: 10
```
Explanation: The subarray `[5,5]` (wrapping around the end) has sum 5 + 5 = 10.

**Example 3**
```text
Input: nums = [-3,-2,-3]
Output: -2
```
Explanation: The subarray `[-2]` has the maximum sum -2.

## Constraints

- `n == nums.length`
- `1 <= n <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`
