---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/surrounded-regions/
neetcode: https://neetcode.io/problems/surrounded-regions
---
# Surrounded Regions

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/surrounded-regions/) · [NeetCode](https://neetcode.io/problems/surrounded-regions)

## Problem

You are given an `m x n` board of characters `'X'` and `'O'`. A **region** is a group of `'O'` cells connected 4-directionally. A region is **surrounded** if none of its cells lie on the border of the board (i.e. it is completely enclosed by `'X'` cells).

Capture every surrounded region by flipping all of its `'O'` cells to `'X'`. Modify the board **in place**; the function returns nothing. Regions touching the border remain unchanged.

## Examples

**Example 1**
```text
Input: board = [["X","X","X","X"],
                ["X","O","O","X"],
                ["X","X","O","X"],
                ["X","O","X","X"]]
Output:        [["X","X","X","X"],
                ["X","X","X","X"],
                ["X","X","X","X"],
                ["X","O","X","X"]]
Explanation: The bottom 'O' is on the border, so it is not captured.
```

**Example 2**
```text
Input: board = [["X"]]
Output: [["X"]]
```

## Constraints

- `1 <= m, n <= 200`
- `board[i][j]` is `'X'` or `'O'`
