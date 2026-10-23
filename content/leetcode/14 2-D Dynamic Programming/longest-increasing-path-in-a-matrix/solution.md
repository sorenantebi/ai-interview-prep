---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
neetcode: https://neetcode.io/problems/longest-increasing-path-in-matrix
---
# Longest Increasing Path In a Matrix - Solution

**Question:** Longest Increasing Path In a Matrix - Question · **Difficulty:** Hard

## Intuition

Edges go from a cell to a strictly larger neighbour, so the graph is a DAG and the answer is its longest path. The cleanest iterative way is **topological sort (Kahn's algorithm)**: repeatedly peel off cells that have no smaller neighbour; the number of layers peeled is the longest path length. (Memoized DFS works too but can hit Python's recursion limit on large snake-shaped inputs.)

## Approach

1. For every cell compute `indeg` = number of neighbours with a strictly smaller value.
2. Put all cells with `indeg == 0` (local minima) in a queue.
3. Process the queue level by level; each level increments `length`. When popping a cell, decrement `indeg` of each strictly larger neighbour and enqueue it when it hits 0.
4. Return the number of levels processed.

## Code

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        ROWS, COLS = len(matrix), len(matrix[0])
        dp = {}  # (r, c) -> LIP

        def dfs(r, c, prevVal):
            if r < 0 or r == ROWS or c < 0 or c == COLS or matrix[r][c] <= prevVal:
                return 0
            if (r, c) in dp:
                return dp[(r, c)]

            res = 1
            res = max(res, 1 + dfs(r + 1, c, matrix[r][c]))
            res = max(res, 1 + dfs(r - 1, c, matrix[r][c]))
            res = max(res, 1 + dfs(r, c + 1, matrix[r][c]))
            res = max(res, 1 + dfs(r, c - 1, matrix[r][c]))
            dp[(r, c)] = res
            return res

        for r in range(ROWS):
            for c in range(COLS):
                dfs(r, c, -1)
        return max(dp.values())
```

## Complexity

- **Time:** `O(m * n)` — each cell and each of its 4 edges is processed a constant number of times.
- **Space:** `O(m * n)` — the in-degree table and the queue.

## Other Approaches

- **DFS + memoization:** `lip(r, c) = 1 + max(lip(neighbour))` over larger neighbours — Time `O(mn)`, Space `O(mn)`; needs a raised recursion limit for deep paths in Python.
- **Sort cells by value and DP:** process cells in increasing order, `dp[cell] = 1 + max(dp[smaller neighbours])` — Time `O(mn log mn)`, Space `O(mn)`.

## Key Takeaway

"Strictly increasing" moves define a DAG, so no visited set is needed; longest path in a DAG = memoized DFS or the number of layers in a topological sort.
