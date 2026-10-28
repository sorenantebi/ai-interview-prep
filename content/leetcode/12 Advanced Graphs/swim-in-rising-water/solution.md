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

## C++

```cpp
/*
    Given an integer elevation matrix, rain falls, at time t, depth everywhere is t
    Can swim iff elevation at most t, return least time get from top left to bottom right

    Shortest path w/ min heap: at every step, find lowest water level to move forward

    Time: O(n^2 log n)
    Space: O(n^2)
*/

class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        if (n == 1) {
            return 0;
        }
        
        vector<vector<bool>> visited(n, vector<bool>(n));
        visited[0][0] = true;
        
        int result = max(grid[0][0], grid[n - 1][n - 1]);
        
        priority_queue<vector<int>, vector<vector<int>>, greater<vector<int>>> pq;
        pq.push({result, 0, 0});
        
        while (!pq.empty()) {
            vector<int> curr = pq.top();
            pq.pop();
            
            result = max(result, curr[0]);
            
            for (int i = 0; i < 4; i++) {
                int x = curr[1] + dirs[i][0];
                int y = curr[2] + dirs[i][1];
                
                if (x < 0 || x >= n || y < 0 || y >= n || visited[x][y]) {
                    continue;
                }
                
                if (x == n - 1 && y == n - 1) {
                    return result;
                }

                pq.push({grid[x][y], x, y});
                visited[x][y] = true;
            }
        }
        
        return -1;
    }
private:
    vector<vector<int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
};
```
