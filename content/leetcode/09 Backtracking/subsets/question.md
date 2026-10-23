---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/subsets/
neetcode: https://neetcode.io/problems/subsets
---
# Subsets

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/subsets/) · [NeetCode](https://neetcode.io/problems/subsets)

## Problem

Given an integer array `nums` whose elements are all **distinct**, return every possible subset (the power set), including the empty subset and the full array.

The result must not contain duplicate subsets. The subsets, and the elements inside each subset, may be returned in any order.

## Examples

**Example 1**
```text
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**Example 2**
```text
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All values in `nums` are unique
