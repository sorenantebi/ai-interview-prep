---
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/island-perimeter/
neetcode: https://neetcode.io/problems/island-perimeter
---
# Island Perimeter - Solution

## Intuition

Each land cell contributes 4 edges to the perimeter, but every edge shared with a neighboring land cell is hidden from both cells. So the perimeter equals `4 * land cells - 2 * shared edges`. Equivalently, count each land-cell side that faces water or the grid boundary.

## Approach

1. Iterate over every cell in the grid.
2. For each land cell, add 4 to the perimeter.
3. If the cell above is also land, subtract 2 (the shared edge is removed from both cells).
4. If the cell to the left is also land, subtract 2.
5. Checking only up and left counts each shared edge exactly once.
6. Return the total.

## Code

```python
class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        visit = set()

        def dfs(i, j):
            if i >= len(grid) or j >= len(grid[0]) or i < 0 or j < 0 or grid[i][j] == 0:
                return 1
            if (i, j) in visit:
                return 0

            visit.add((i, j))
            perim = dfs(i, j + 1)
            perim += dfs(i + 1, j)
            perim += dfs(i, j - 1)
            perim += dfs(i - 1, j)
            return perim

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j]:
                    return dfs(i, j)
```

## Complexity

- **Time:** `O(row * col)` — every cell is visited once with constant work.
- **Space:** `O(1)` — only a counter is used.

## Other Approaches

- **DFS/BFS from a land cell:** traverse the island and count neighbors that are water or out of bounds — Time `O(row * col)` / Space `O(row * col)`
- **Count all four sides per cell:** for each land cell, check all four neighbors and add 1 for each water or boundary side — Time `O(row * col)` / Space `O(1)`

## C++

```cpp
// Time complexity is O(M*N)
// Space complexity is O(1)

class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
      int m = grid.size();
      int n = grid[0].size();
      
      int prem = 0;
      
      for(int i = 0 ; i < m ; i++)
      {
        for(int j = 0 ; j < n ; j++)
        {
          if(grid[i][j] == 1) {
            prem += 4;
          
            if(j > 0 && grid[i][j-1] == 1) prem -=2;
            if(i >0 && grid[i-1][j] == 1) prem -=2;

          }
        }
      }
      
      return prem;
    }
};
```
