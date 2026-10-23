---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/subsets-ii/
neetcode: https://neetcode.io/problems/subsets-ii
---
# Subsets II

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/subsets-ii/) · [NeetCode](https://neetcode.io/problems/subsets-ii)

## Problem

Given an integer array `nums` that **may contain duplicate values**, return all distinct subsets (the power set). Two subsets with the same multiset of values count as the same subset and must appear only once.

The subsets may be returned in any order.

## Examples

**Example 1**
```text
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
```

**Example 2**
```text
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
