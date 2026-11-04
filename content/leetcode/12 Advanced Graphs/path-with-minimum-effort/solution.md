---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/path-with-minimum-effort/
neetcode: https://neetcode.io/problems/path-with-minimum-effort
---
# Path With Minimum Effort - Solution

## Intuition

The cost of a route is its largest single step, not the sum of steps. This is a minimax path problem, which Dijkstra's algorithm handles if the distance to a cell is defined as the smallest achievable "maximum step" over all routes reaching it. Extending a route by one step gives `max(current effort, step difference)`, and this value never decreases, so the greedy ordering of Dijkstra stays valid.

## Approach

1. Keep `effort[r][c]`, the best known route effort to each cell, initialised to infinity except `0` at `(0, 0)`.
2. Use a min-heap keyed by effort, starting with `(0, 0, 0)`.
3. Pop the cell with the smallest effort. If it is the bottom-right cell, return its effort.
4. Skip the entry if it is stale (its effort is larger than the recorded one).
5. For each of the four neighbours, compute `new_effort = max(effort, abs(height difference))`. If it improves the neighbour's recorded effort, update it and push it onto the heap.

## Code

```python
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        
        efforts = [[float('inf')] * n for _ in range(m)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        efforts[0][0] = 0
        pq = [(0, 0, 0)]  # (effort, row, col)
        
        while pq:
            curEffort, i, j = heapq.heappop(pq)
            
            # reached the bottom-right corner => return the effort
            if i == m - 1 and j == n - 1:
                return curEffort
            
            for dx, dy in directions:
                x, y = i + dx, j + dy
                
                if 0 <= x < m and 0 <= y < n:
                    newEffort = max(abs(heights[x][y] - heights[i][j]), curEffort)
                    
                    if newEffort < efforts[x][y]:
                        efforts[x][y] = newEffort
                        heapq.heappush(pq, (newEffort, x, y))
        
        return efforts[m - 1][n - 1]
```

## Complexity

- **Time:** `O(R * C * log(R * C))` — each cell can be pushed a bounded number of times (at most once per edge relaxation, about 4 per cell), and each heap operation costs `O(log(R * C))`.
- **Space:** `O(R * C)` — the effort table and the heap.

## Other Approaches

- **Binary search on the answer + BFS/DFS:** binary search the maximum allowed step and check reachability of the goal using only steps within that limit — Time `O(R * C * log(max height))` / Space `O(R * C)`
- **Union-Find (Kruskal-style):** sort all edges by height difference and union cells until the start and end are connected; the last edge added is the answer — Time `O(R * C * log(R * C))` / Space `O(R * C)`
