---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum/
neetcode: https://neetcode.io/problems/combination-target-sum
---
# Combination Sum

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/combination-sum/) · [NeetCode](https://neetcode.io/problems/combination-target-sum)

## Problem

Given an array of **distinct** positive integers `candidates` and a positive integer `target`, return all unique combinations of candidates whose sum equals `target`. The same candidate may be used **any number of times**.

Two combinations are considered the same if they use each number the same number of times (order does not matter). Return the combinations in any order. The test data guarantees fewer than 150 valid combinations.

## Examples

**Example 1**
```text
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
```

**Example 2**
```text
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

**Example 3**
```text
Input: candidates = [2], target = 1
Output: []
```

## Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`, all distinct
- `1 <= target <= 40`
