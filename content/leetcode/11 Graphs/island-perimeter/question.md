---
video: https://www.youtube.com/watch?v=fISIuAFRM2s
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/island-perimeter/
neetcode: https://neetcode.io/problems/island-perimeter
---
# Island Perimeter

**Topic:** Graphs · **Difficulty:** Easy

## Problem

You are given a `row x col` grid where `grid[i][j] = 1` represents land and `grid[i][j] = 0` represents water.

Cells are connected horizontally and vertically (not diagonally). The grid is completely surrounded by water, and it contains exactly one island (one or more connected land cells). The island has no "lakes": water inside the island is not connected to the water around it. Each cell is a square with side length 1.

Return the perimeter of the island.

## Examples

**Example 1**
```text
Input: grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
Output: 16
```

**Example 2**
```text
Input: grid = [[1]]
Output: 4
```

**Example 3**
```text
Input: grid = [[1,0]]
Output: 4
```

## Constraints

- `row == grid.length`
- `col == grid[i].length`
- `1 <= row, col <= 100`
- `grid[i][j]` is `0` or `1`.
- There is exactly one island in `grid`.
