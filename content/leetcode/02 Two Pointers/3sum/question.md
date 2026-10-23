---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/3sum/
neetcode: https://neetcode.io/problems/three-integer-sum
---
# 3Sum

**Topic:** Two Pointers · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/3sum/) · [NeetCode](https://neetcode.io/problems/three-integer-sum)

## Problem

Given an integer array `nums`, return every **unique** triplet `[nums[i], nums[j], nums[k]]` with `i`, `j`, `k` pairwise distinct indices such that the three values sum to `0`. The result must not contain duplicate triplets (as multisets of values). The triplets and the order inside them may be returned in any order.

## Examples

**Example 1**
```text
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
```

**Example 2**
```text
Input: nums = [0,1,1]
Output: []
```

**Example 3**
```text
Input: nums = [0,0,0]
Output: [[0,0,0]]
```

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`
