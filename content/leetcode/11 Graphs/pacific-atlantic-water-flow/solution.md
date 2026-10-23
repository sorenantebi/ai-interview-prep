---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/pacific-atlantic-water-flow/
neetcode: https://neetcode.io/problems/pacific-atlantic-water-flow
---
# Pacific Atlantic Water Flow - Solution

**Question:** Pacific Atlantic Water Flow - Question · **Difficulty:** Medium

## Intuition

Checking every cell's downhill paths separately is expensive. Reverse the flow: start from the ocean borders and move **uphill** (to neighbors with height `>=` the current one). Every cell reached from the Pacific border can drain into the Pacific, and likewise for the Atlantic. The answer is the intersection of the two reachable sets.

## Approach

1. Seed a BFS with all Pacific border cells (top row + left column) and find all cells reachable by moving to neighbors of equal or greater height.
2. Do the same from the Atlantic border cells (bottom row + right column).
3. Return the cells present in both reachable sets.

## Code

```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        ROWS, COLS = len(heights), len(heights[0])
        pac, atl = set(), set()

        def dfs(r, c, visit, prevHeight):
            if (
                (r, c) in visit
                or r < 0
                or c < 0
                or r == ROWS
                or c == COLS
                or heights[r][c] < prevHeight
            ):
                return
            visit.add((r, c))
            dfs(r + 1, c, visit, heights[r][c])
            dfs(r - 1, c, visit, heights[r][c])
            dfs(r, c + 1, visit, heights[r][c])
            dfs(r, c - 1, visit, heights[r][c])

        for c in range(COLS):
            dfs(0, c, pac, heights[0][c])
            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])

        for r in range(ROWS):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, COLS - 1, atl, heights[r][COLS - 1])

        res = []
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) in pac and (r, c) in atl:
                    res.append([r, c])
        return res
```

## Complexity

- **Time:** `O(m * n)` — each BFS visits every cell at most once.
- **Space:** `O(m * n)` — the two visited sets and the queue.

## Other Approaches

- **DFS from every cell:** for each cell, search downhill to see whether both oceans are reachable — Time `O((m * n)^2)`, Space `O(m * n)`.

## Key Takeaway

When asking "which cells can reach target X", reverse the edges and search once from X — turning many searches into one.
