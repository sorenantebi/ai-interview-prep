---
video: https://www.youtube.com/watch?v=EYeR-_1NRlQ
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/4sum/
neetcode: https://neetcode.io/problems/4sum
---
# 4Sum

**Topic:** Two Pointers · **Difficulty:** Medium

## Problem

Given an integer array `nums` of length `n` and an integer `target`, return all unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that:

- `0 <= a, b, c, d < n`
- `a`, `b`, `c`, and `d` are distinct indices.
- `nums[a] + nums[b] + nums[c] + nums[d] == target`

The quadruplets may be returned in any order, and no two returned quadruplets may contain the same values.

## Examples

**Example 1**
```text
Input: nums = [1,0,-1,0,-2,2], target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
```

**Example 2**
```text
Input: nums = [2,2,2,2,2], target = 8
Output: [[2,2,2,2]]
```

## Constraints

- `1 <= nums.length <= 200`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
