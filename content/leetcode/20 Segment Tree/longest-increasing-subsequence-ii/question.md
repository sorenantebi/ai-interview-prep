---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/longest-increasing-subsequence-ii/
---
# Longest Increasing Subsequence II

**Topic:** Segment Tree · **Difficulty:** Hard

## Problem

You are given an integer array `nums` and an integer `k`.

Find the longest subsequence of `nums` that satisfies both conditions:

- The subsequence is strictly increasing.
- The difference between every pair of adjacent elements in the subsequence is at most `k`.

Return the length of the longest such subsequence.

A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

## Examples

**Example 1**
```text
Input: nums = [4,2,1,4,3,4,5,8,15], k = 3
Output: 5
```
The longest valid subsequence is `[1,3,4,5,8]`. The subsequence `[1,3,4,5,8,15]` is not valid because `15 - 8 = 7` is larger than `3`.

**Example 2**
```text
Input: nums = [7,4,5,1,8,12,4,7], k = 5
Output: 4
```
The longest valid subsequence is `[4,5,8,12]`.

**Example 3**
```text
Input: nums = [1,5], k = 1
Output: 1
```
The longest valid subsequence is `[1]`.

## Constraints

- `1 <= nums.length <= 10^5`
- `1 <= nums[i], k <= 10^5`
