---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum-ii/
neetcode: https://neetcode.io/problems/combination-target-sum-ii
---
# Combination Sum II

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/combination-sum-ii/) · [NeetCode](https://neetcode.io/problems/combination-target-sum-ii)

## Problem

Given an array of positive integers `candidates` (which **may contain duplicates**) and a positive integer `target`, return all unique combinations whose elements sum to `target`. Each array position may be used **at most once** in a combination.

The result must not contain duplicate combinations (two combinations with the same multiset of values are the same). Return them in any order.

## Examples

**Example 1**
```text
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6],[1,2,5],[1,7],[2,6]]
```

**Example 2**
```text
Input: candidates = [2,5,2,1,2], target = 5
Output: [[1,2,2],[5]]
```

## Constraints

- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`
