---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/swim-in-rising-water/
neetcode: https://neetcode.io/problems/swim-in-rising-water
---
# Swim In Rising Water - Solution

**Question:** Swim In Rising Water - Question · **Difficulty:** Hard

## Intuition

The time needed for a path is the highest elevation along it (including start and end). We want the path minimising that maximum — a minimax shortest path. Dijkstra with `max` instead of `+` solves it: always expand the reachable cell with the lowest elevation seen so far.

## Approach

1. Min-heap of `(time_needed, r, c)` starting with `(grid[0][0], 0, 0)`; mark `(0, 0)` visited.
2. Pop the lowest entry. If it is the bottom-right cell, return its time.
3. For each unvisited neighbour, mark visited and push `(max(time, grid[nr][nc]), nr, nc)`.

## Code

```python
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        N = len(grid)
        visit = set()
        minH = [[grid[0][0], 0, 0]]  # (time/max-height, r, c)
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        visit.add((0, 0))
        while minH:
            t, r, c = heapq.heappop(minH)
            if r == N - 1 and c == N - 1:
                return t
            for dr, dc in directions:
                neiR, neiC = r + dr, c + dc
                if (
                    neiR < 0
                    or neiC < 0
                    or neiR == N
                    or neiC == N
                    or (neiR, neiC) in visit
                ):
                    continue
                visit.add((neiR, neiC))
                heapq.heappush(minH, [max(t, grid[neiR][neiC]), neiR, neiC])
```

## Complexity

- **Time:** `O(n^2 log n)` — each of the `n^2` cells is pushed once; heap ops cost `log(n^2)`.
- **Space:** `O(n^2)` — heap and visited set.

## Other Approaches

- **Binary search + BFS:** binary search `t` in `[grid[0][0], n^2 - 1]` and check reachability through cells `<= t` — Time `O(n^2 log n)`, Space `O(n^2)`.
- **Union-Find by elevation:** add cells in increasing elevation order, union with already-added neighbours, stop when corners are connected — Time `O(n^2 α(n))` after sorting, Space `O(n^2)`.

## Key Takeaway

"Minimise the bottleneck (max) along a path" is solved by Dijkstra with `max`, by binary search on the answer + BFS, or by Kruskal-style union-find — all three are worth recognising.
