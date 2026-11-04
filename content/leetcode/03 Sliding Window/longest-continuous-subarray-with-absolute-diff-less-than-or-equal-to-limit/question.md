---
video: https://www.youtube.com/watch?v=V-ecDfY5xEw
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/
neetcode: https://neetcode.io/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit
---
# Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

**Topic:** Sliding Window · **Difficulty:** Medium

## Problem

You are given an integer array `nums` and an integer `limit`. Return the length of the longest non-empty contiguous subarray in which the absolute difference between every pair of elements is less than or equal to `limit`.

## Examples

**Example 1**
```text
Input: nums = [8,2,4,7], limit = 4
Output: 2
```
The subarrays `[2,4]` and `[4,7]` are valid. Any subarray of length 3 or more contains a pair that differs by more than 4 (for instance, `|8-2| = 6` and `|7-2| = 5`).

**Example 2**
```text
Input: nums = [10,1,2,4,7,2], limit = 5
Output: 4
```
The subarray `[2,4,7,2]` is valid, since its largest difference is `|7-2| = 5`. Extending it to the left adds `1`, and `|7-1| = 6 > 5`.

**Example 3**
```text
Input: nums = [4,2,2,2,4,4,2,2], limit = 0
Output: 3
```
With `limit = 0`, all elements in the subarray must be equal. The longest run of equal values is `[2,2,2]`.

## Constraints

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= limit <= 10^9`
