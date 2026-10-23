---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/permutations/
neetcode: https://neetcode.io/problems/permutations
---
# Permutations

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/permutations/) · [NeetCode](https://neetcode.io/problems/permutations)

## Problem

Given an array `nums` of **distinct** integers, return every possible ordering (permutation) of its elements. The permutations can be returned in any order.

## Examples

**Example 1**
```text
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Example 2**
```text
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

**Example 3**
```text
Input: nums = [1]
Output: [[1]]
```

## Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All values in `nums` are unique
