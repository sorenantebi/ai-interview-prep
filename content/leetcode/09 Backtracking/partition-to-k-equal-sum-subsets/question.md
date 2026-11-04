---
video: https://www.youtube.com/watch?v=mBk4I0X46oI
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/partition-to-k-equal-sum-subsets/
neetcode: https://neetcode.io/problems/partition-to-k-equal-sum-subsets
---
# Partition to K Equal Sum Subsets

**Topic:** Backtracking · **Difficulty:** Medium

## Problem

Given an integer array `nums` and an integer `k`, return `true` if the array can be divided into `k` non-empty subsets whose sums are all equal. Every element must belong to exactly one subset. Otherwise, return `false`.

## Examples

**Example 1**
```text
Input: nums = [4,3,2,3,5,2,1], k = 4
Output: true
```
It is possible to divide it into 4 subsets (5), (1, 4), (2, 3), (2, 3) with equal sums.

**Example 2**
```text
Input: nums = [1,2,3,4], k = 3
Output: false
```

## Constraints

- `1 <= k <= nums.length <= 16`
- `1 <= nums[i] <= 10^4`
- The frequency of each element is in the range `[1, 4]`.
