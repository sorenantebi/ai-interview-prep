---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/unique-paths-ii/
neetcode: https://neetcode.io/problems/unique-paths-ii
---
# Unique Paths II - Solution

## Intuition

A cell can only be entered from the cell above or the cell to its left, so the number of paths to a cell is the sum of the paths to those two neighbours. An obstacle cell has zero paths into it, which blocks everything that would have flowed through it.

## Approach

1. Keep a single row `dp` of length `n`, where `dp[j]` is the number of paths to the current cell in column `j`.
2. Initialise `dp[0] = 1` if the start is free, otherwise `0`.
3. For each row, for each column `j`: if the cell is an obstacle, set `dp[j] = 0`; otherwise, if `j > 0`, add `dp[j - 1]` (paths from the left) to `dp[j]` (paths from above, carried over from the previous row).
4. Return `dp[n - 1]`.

## Code

```python
class Solution:
    def uniquePathsWithObstacles(self, grid: List[List[int]]) -> int:
        M, N = len(grid), len(grid[0])
        dp = [0] * N
        dp[N-1] = 1

        # Time: O(N*M), Space: O(N)
        for r in reversed(range(M)):
            for c in reversed(range(N)):
                if grid[r][c]:
                    dp[c] = 0
                elif c + 1 < N:
                    dp[c] = dp[c] + dp[c + 1]
        return dp[0]


        # Time: O(N*M), Space: O(N*M)
        M, N = len(grid), len(grid[0])
        dp = {(M - 1, N - 1): 1}

        def dfs(r, c):
            if r == M or c == N or grid[r][c]:
                return 0
            if (r, c) in dp:
                return dp[(r, c)]
            dp[(r, c)] = dfs(r + 1, c) + dfs(r, c + 1)
            return dp[(r, c)]
        return dfs(0, 0)
```

## Complexity

- **Time:** `O(m * n)` — every cell is visited once.
- **Space:** `O(n)` — only one row of counts is kept.

## Other Approaches

- **2-D DP table:** same recurrence stored in a full `m x n` grid — Time `O(m * n)` / Space `O(m * n)`
- **Top-down memoization:** recursion from the start with a cache on `(i, j)` — Time `O(m * n)` / Space `O(m * n)`

## C++

```cpp
/*

Given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]).
The robot can only move either down or right at any point in time. An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

Example. obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
	 There is one obstacle in the middle of the 3x3 grid above.
	 There are two ways to reach the bottom-right corner:
         1. Right -> Right -> Down -> Down
         2. Down -> Down -> Right -> Right
	 So, the number of unique paths the robot can take is 2. Hence we return 2 as our answer.


Time: O(m * n)
Space: O(n)

*/


class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& grid) {

        int m = grid.size(), n = grid[0].size();
        if(grid[m-1][n-1] == 1 || grid[0][0] == 1) return 0;
        vector<long long> dp(n);
        dp[n-1] = 1;
        for(int i=m-1; i>=0; i--) {
            for(int j=n-1; j>=0; j--) {
                if(grid[i][j] == 1) dp[j] = 0;
                else if(j == n-1) continue;
                else dp[j] = dp[j] + dp[j+1];
            }
        }
        return dp[0];

    }
};
```
