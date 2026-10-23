---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/rotting-oranges/
neetcode: https://neetcode.io/problems/rotting-fruit
---
# Rotting Oranges

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/rotting-oranges/) · [NeetCode](https://neetcode.io/problems/rotting-fruit)

## Problem

You are given an `m x n` grid where each cell is:

- `0`: empty
- `1`: a fresh orange
- `2`: a rotten orange

Every minute, each fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes until no fresh orange remains. If some fresh orange can never rot, return `-1`. If there are no fresh oranges at the start, the answer is `0`.

## Examples

**Example 1**
```text
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
```

**Example 2**
```text
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The bottom-left orange is never adjacent to a rotten one.
```

**Example 3**
```text
Input: grid = [[0,2]]
Output: 0
Explanation: There are no fresh oranges at minute 0.
```

## Constraints

- `1 <= m, n <= 10`
- `grid[i][j]` is `0`, `1`, or `2`
