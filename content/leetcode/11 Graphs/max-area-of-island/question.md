---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/max-area-of-island/
neetcode: https://neetcode.io/problems/max-area-of-island
---
# Max Area of Island

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/max-area-of-island/) · [NeetCode](https://neetcode.io/problems/max-area-of-island)

## Problem

You are given an `m x n` binary grid where `1` is land and `0` is water. An island is a group of `1`s connected 4-directionally (horizontally or vertically). The area of an island is the number of land cells it contains.

Return the largest island area in the grid, or `0` if there is no land.

## Examples

**Example 1**
```text
Input: grid = [[0,0,1,0,0],[0,1,1,0,0],[0,0,0,1,1],[0,0,0,1,1]]
Output: 4
Explanation: The 2x2 block in the bottom-right is the largest island.
```

**Example 2**
```text
Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0
```

## Constraints

- `1 <= m, n <= 50`
- `grid[i][j]` is `0` or `1`
