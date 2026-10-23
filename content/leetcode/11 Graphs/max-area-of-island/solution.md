---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/max-area-of-island/
neetcode: https://neetcode.io/problems/max-area-of-island
---
# Max Area of Island - Solution

**Question:** Max Area of Island - Question · **Difficulty:** Medium

## Intuition

This is "Number of Islands" with a size counter: each island is a connected component, and we want the size of the largest one. Flood-fill each island once, count how many cells the fill visits, and keep the maximum.

## Approach

1. Scan every cell.
2. When an unvisited land cell is found, run a DFS (iterative stack) that sinks visited cells (sets them to `0`) and counts them.
3. Update the best area with the count.
4. Return the best area (0 if no land was found).

## Code

```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        visit = set()

        def dfs(r, c):
            if (
                r < 0
                or r == ROWS
                or c < 0
                or c == COLS
                or grid[r][c] == 0
                or (r, c) in visit
            ):
                return 0
            visit.add((r, c))
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

        area = 0
        for r in range(ROWS):
            for c in range(COLS):
                area = max(area, dfs(r, c))
        return area
```

## Complexity

- **Time:** `O(m * n)` — every cell is pushed and popped at most once.
- **Space:** `O(m * n)` — worst-case stack size when the whole grid is land; the grid itself serves as the visited marker.

## Other Approaches

- **Recursive DFS returning area:** `dfs(r, c) = 1 + sum(dfs(neighbors))` — Time `O(m * n)`, Space `O(m * n)` recursion depth.
- **Union-Find with component sizes:** union adjacent land cells and track sizes — Time `O(m * n * α(mn))`, Space `O(m * n)`.

## Key Takeaway

Flood fill can return an aggregate (size, perimeter, bounding box) of each component — a small extension of the island-counting template.
