---
video: https://www.youtube.com/watch?v=d3UOz7zdE4I
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/unique-paths-ii/
neetcode: https://neetcode.io/problems/unique-paths-ii
---
# Unique Paths II

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium

## Problem

You are given an `m x n` integer grid `obstacleGrid`. A robot starts at the top-left corner `grid[0][0]` and wants to reach the bottom-right corner `grid[m - 1][n - 1]`. At every step it can only move either down or right.

A cell containing `1` is an obstacle and a cell containing `0` is free space. The robot's path may not pass through any obstacle cell.

Return the number of unique paths the robot can take to reach the bottom-right corner. The test cases are generated so that the answer is at most `2 * 10^9`.

## Examples

**Example 1**
```text
Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
```
There is one obstacle in the middle of the 3x3 grid. The two paths are Right -> Right -> Down -> Down and Down -> Down -> Right -> Right.

**Example 2**
```text
Input: obstacleGrid = [[0,1],[0,0]]
Output: 1
```

## Constraints

- `m == obstacleGrid.length`
- `n == obstacleGrid[i].length`
- `1 <= m, n <= 100`
- `obstacleGrid[i][j]` is `0` or `1`.
