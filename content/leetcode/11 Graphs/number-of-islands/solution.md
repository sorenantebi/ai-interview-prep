---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-islands/
neetcode: https://neetcode.io/problems/count-number-of-islands
---
# Number of Islands - Solution

**Question:** Number of Islands - Question · **Difficulty:** Medium

## Intuition

Treat the grid as a graph where land cells are nodes and adjacent land cells share an edge. The number of islands is the number of connected components. Scan the grid; whenever an unvisited land cell is found, it starts a new island, and a flood fill (BFS/DFS) marks the entire island as visited.

## Approach

1. Loop over every cell.
2. When a cell is `'1'`, increment the island count and flood-fill from it.
3. The flood fill (iterative BFS here, to avoid recursion limits) turns every reachable `'1'` into `'0'` so it is never counted again.
4. Return the count.

## Code

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        islands = 0
        visit = set()
        rows, cols = len(grid), len(grid[0])

        def dfs(r, c):
            if (
                r not in range(rows)
                or c not in range(cols)
                or grid[r][c] == "0"
                or (r, c) in visit
            ):
                return

            visit.add((r, c))
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            for dr, dc in directions:
                dfs(r + dr, c + dc)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visit:
                    islands += 1
                    dfs(r, c)
        return islands

# DFS O(1) Space and much less code
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        def dfs(r, c):
            if not 0 <= r < len(grid) or not 0 <= c < len(grid[0]) or grid[r][c] == '0':
                return 0
            grid[r][c] = '0'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
            return 1
        count = 0
        for r in range(rows):
            for c in range(cols):
                count += dfs(r, c)
        return count

# BFS Version From Video
class SolutionBFS:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = set()
        islands = 0

         def bfs(r, c):
             q = deque()
             visited.add((r, c))
             q.append((r, c))
           
             while q:
                 row, col = q.popleft()
                 directions = [[1, 0],[-1, 0],[0, 1],[0, -1]]
               
                 for dr, dc in directions:
                     r, c = row + dr, col + dc
                     if (r) in range(rows) and (c) in range(cols) and grid[r][c] == '1' and (r, c) not in visited:
                       
                         q.append((r, c ))
                         visited.add((r, c ))

         for r in range(rows):
             for c in range(cols):
               
                 if grid[r][c] == "1" and (r, c) not in visited:
                     bfs(r, c)
                     islands += 1 

         return islands
```

## Complexity

- **Time:** `O(m * n)` — each cell is enqueued/visited at most once.
- **Space:** `O(min(m, n))` to `O(m * n)` — the BFS queue in the worst case; the grid is modified in place instead of using a visited set.

## Other Approaches

- **Recursive DFS:** same idea with recursion — Time `O(m * n)`, Space `O(m * n)` recursion stack (may hit Python's recursion limit on large grids).
- **Union-Find:** union adjacent land cells and count distinct roots — Time `O(m * n * α(mn))`, Space `O(m * n)`.

## Key Takeaway

"Count groups of connected cells" = count connected components: scan + flood fill, marking cells visited as soon as they are enqueued.

## C++

```cpp
/*
    Given grid where '1' is land & '0' is water, return # of islands

    DFS, set visited land to '0' to not visit it again, count islands

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        
        int result = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    dfs(grid, i, j, m, n);
                    result++;
                }
            }
        }
        
        return result;
    }
private:
    void dfs(vector<vector<char>>& grid, int i, int j, int m, int n) {
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == '0') {
            return;
        }
        grid[i][j] = '0';
        
        dfs(grid, i - 1, j, m, n);
        dfs(grid, i + 1, j, m, n);
        dfs(grid, i, j - 1, m, n);
        dfs(grid, i, j + 1, m, n);
    }
};
```
