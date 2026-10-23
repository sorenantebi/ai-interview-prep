---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-islands/
neetcode: https://neetcode.io/problems/count-number-of-islands
---
# Number of Islands

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/number-of-islands/) · [NeetCode](https://neetcode.io/problems/count-number-of-islands)

## Problem

You are given an `m x n` grid of characters where `'1'` is land and `'0'` is water. An island is a group of land cells connected horizontally or vertically (not diagonally). Everything outside the grid is water.

Return the number of islands in the grid.

## Examples

**Example 1**
```text
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
```

**Example 2**
```text
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

## Constraints

- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`
