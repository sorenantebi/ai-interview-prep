---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-path-sum/
neetcode: https://neetcode.io/problems/minimum-path-sum
---
# Minimum Path Sum - Solution

## Intuition

Every cell can only be entered from the cell above or the cell to its left. So the cheapest way to reach a cell is its own value plus the cheaper of those two predecessors. The answer is the cheapest cost at the bottom-right cell.

## Approach

1. Let `dp[j]` hold the minimum path sum to reach the current cell in column `j` of the row being processed.
2. Initialize the first row as running prefix sums, since those cells can only be reached from the left.
3. For each following row, the first column can only be reached from above, so add the cell value to `dp[0]`.
4. For every other column, set `dp[j] = grid[i][j] + min(dp[j], dp[j - 1])`, where `dp[j]` is still the value from the row above and `dp[j - 1]` is the already-updated value to the left.
5. Return `dp[n - 1]` after the last row.

## Code

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        prev = [float("inf")] * n
        prev[-1] = 0

        for row in range(m - 1, -1, -1):
            dp = [float("inf")] * n
            for col in range(n - 1, -1, -1):
                if col < n - 1:
                    dp[col] = min(dp[col], dp[col + 1])
                dp[col] = min(dp[col], prev[col]) + grid[row][col]
            prev = dp

        return prev[0]
```

## Complexity

- **Time:** `O(m * n)` — each cell is processed once.
- **Space:** `O(n)` — only one row of DP values is kept.

## Other Approaches

- **Full 2-D DP table:** store the minimum cost for every cell in an `m x n` table — Time `O(m * n)` / Space `O(m * n)`
- **In-place DP:** overwrite `grid` with the running minimum costs — Time `O(m * n)` / Space `O(1)` extra, but mutates the input
- **Top-down recursion with memoization:** recurse from the bottom-right cell and cache results — Time `O(m * n)` / Space `O(m * n)`

## C++

```cpp
class Solution{
    public:    
        void Helper(vector<vector<int>> & grid, vector<vector<int>> & dp, int i, int k){            
            int X = grid.size();            
            int Y = grid[0].size();            
            for(int i = 0; i < X; i++){                
                for(k = 0; k < Y; k++){                    
                    if((i - 1 >= 0) && (k - 1 >= 0)){
                        dp[i][k] = grid[i][k] + min(dp[i - 1][k], dp[i][k - 1]);             
                    }
                    else{
                        if(i - 1 >= 0){
                            dp[i][k] = grid[i][k] + dp[i - 1][k];
                        }                        
                        if(k - 1 >= 0){
                            dp[i][k] = grid[i][k] + dp[i][k - 1];
                        }
                    }
                }
            }   
            
        }    
        int minPathSum(vector<vector<int>>& grid){            
            vector<vector<int>> dp(grid.size(), vector<int>(grid[0].size()));            
            dp[0][0] = grid[0][0];            
            Helper(grid, dp, grid.size() - 1, grid[0].size() - 1);            
            return dp[grid.size() - 1][grid[0].size() - 1];        
        }
};
```
