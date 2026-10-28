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

## C++

```cpp
/*
    Top & left pacific, bottom & right atlantic, determine spots that flow to both

    Instead go outside in, from oceans to spots where rain could flow from
    Faster bc avoids repeated work: cells along a path can also reach that ocean

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size();
        int n = heights[0].size();
        
        vector<vector<bool>> pacific(m, vector<bool>(n));
        vector<vector<bool>> atlantic(m, vector<bool>(n));
        
        for (int i = 0; i < m; i++) {
            dfs(heights, pacific, i, 0, m, n);
            dfs(heights, atlantic, i, n - 1, m, n);
        }
        
        for (int j = 0; j < n; j++) {
            dfs(heights, pacific, 0, j, m, n);
            dfs(heights, atlantic, m - 1, j, m, n);
        }
        
        vector<vector<int>> result;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (pacific[i][j] && atlantic[i][j]) {
                    result.push_back({i, j});
                }
            }
        }
        
        return result;
    }
private:
    void dfs(vector<vector<int>>& heights, vector<vector<bool>>& visited,
        int i, int j, int m, int n) {
        
        visited[i][j] = true;
        
        if (i > 0 && !visited[i - 1][j] && heights[i - 1][j] >= heights[i][j]) {
            dfs(heights, visited, i - 1, j, m, n);
        }
        if (i < m - 1 && !visited[i + 1][j] && heights[i + 1][j] >= heights[i][j]) {
            dfs(heights, visited, i + 1, j, m, n);
        }
        if (j > 0 && !visited[i][j - 1] && heights[i][j - 1] >= heights[i][j]) {
            dfs(heights, visited, i, j - 1, m, n);
        }
        if (j < n - 1 && !visited[i][j + 1] && heights[i][j + 1] >= heights[i][j]) {
            dfs(heights, visited, i, j + 1, m, n);
        }
    }
};


/*
    BFS solution
*/

class Solution {
private:
    int rows, cols;

    void bfs(queue<pair<int, int>>& q, vector<vector<bool>>& visited, vector<vector<int>>& heights) {

        vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
        while (!q.empty()) {
            auto [row, col] = q.front();
            q.pop();
            for (const auto &direction : directions) {
                int newRow = row + direction.first;
                int newCol = col + direction.second;
                if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols && !visited[newRow][newCol] 
                               && heights[newRow][newCol] >= heights[row][col]) {
                    q.push({newRow, newCol});
                    visited[newRow][newCol] = true;
                }
            }
        }
    }
    
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        rows = heights.size();
        cols = heights[0].size();
        vector<vector<int>> results;
        queue<pair<int, int>> pacificQueue;
        queue<pair<int, int>> atlanticQueue;
        vector<vector<bool>> pacific(rows, vector<bool>(cols, false));
        vector<vector<bool>> atlantic(rows, vector<bool>(cols, false));

        for (int row = 0; row < rows; ++row) {
            pacific[row][0] = true;
            atlantic[row][cols - 1] = true;
            pacificQueue.push({row, 0});
            atlanticQueue.push({row, cols-1});
        }

        for (int col = 0; col < cols; ++col) {
            pacific[0][col] = true;
            atlantic[rows - 1][col] = true;
            pacificQueue.push({0, col});
            atlanticQueue.push({rows - 1, col});
        }

        bfs(pacificQueue, pacific, heights);
        bfs(atlanticQueue, atlantic, heights);

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (pacific[row][col] && atlantic[row][col]) {
                    results.push_back({row, col});
                }
            }
        }

        return results;
    
    }
};
```
