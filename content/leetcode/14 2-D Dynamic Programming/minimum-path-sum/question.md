---
video: https://www.youtube.com/watch?v=pGMsrvt0fpk
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-path-sum/
neetcode: https://neetcode.io/problems/minimum-path-sum
---
# Minimum Path Sum

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium

## Problem

You are given an `m x n` grid filled with non-negative integers. Find a path from the top-left cell to the bottom-right cell that minimizes the sum of all numbers along the path, and return that minimum sum.

At every step you may only move either down or right.

## Examples

**Example 1**
```text
Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
```
Explanation: The path 1 → 3 → 1 → 1 → 1 minimizes the sum.

**Example 2**
```text
Input: grid = [[1,2,3],[4,5,6]]
Output: 12
```

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 200`
- `0 <= grid[i][j] <= 200`
