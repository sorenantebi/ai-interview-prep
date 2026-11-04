---
video: https://www.youtube.com/watch?v=YUF3_eBdzsk
topic: "Binary Search"
difficulty: Hard
leetcode: https://leetcode.com/problems/split-array-largest-sum/
neetcode: https://neetcode.io/problems/split-array-largest-sum
---
# Split Array Largest Sum

**Topic:** Binary Search · **Difficulty:** Hard

## Problem

Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty contiguous subarrays so that the largest sum among those subarrays is as small as possible.

Return that minimized largest sum.

A subarray is a contiguous part of the array.

## Examples

**Example 1**
```text
Input: nums = [7,2,5,10,8], k = 2
Output: 18
```
There are four ways to split `nums` into two subarrays. The best is `[7,2,5]` and `[10,8]`, where the largest subarray sum is 18.

**Example 2**
```text
Input: nums = [1,2,3,4,5], k = 2
Output: 9
```
The best split is `[1,2,3]` and `[4,5]`, where the largest subarray sum is 9.

## Constraints

- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 10^6`
- `1 <= k <= min(50, nums.length)`
