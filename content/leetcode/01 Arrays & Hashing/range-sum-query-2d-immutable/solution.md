---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/range-sum-query-2d-immutable/
neetcode: https://neetcode.io/problems/range-sum-query-2d-immutable
---
# Range Sum Query 2D - Immutable - Solution

## Intuition

Since the matrix never changes, we can spend time up front to make every query constant time. A 2D prefix sum table stores, for each cell, the sum of the whole rectangle from the top left corner `(0, 0)` to that cell. Any rectangle sum is then obtained by inclusion-exclusion over four table entries.

## Approach

1. Build a table `prefix` of size `(m + 1) x (n + 1)` filled with zeros. The extra row and column of zeros avoid boundary checks.
2. Fill it so that `prefix[i + 1][j + 1]` is the sum of `matrix[0..i][0..j]`:
   `prefix[i+1][j+1] = matrix[i][j] + prefix[i][j+1] + prefix[i+1][j] - prefix[i][j]`.
3. For a query, take the large rectangle ending at `(row2, col2)`, subtract the strip above `row1` and the strip left of `col1`, and add back the overlap that was subtracted twice:
   `prefix[row2+1][col2+1] - prefix[row1][col2+1] - prefix[row2+1][col1] + prefix[row1][col1]`.

## Code

```python
class NumMatrix:
    def __init__(self, matrix):
        self.sum_ = [[0] * (len(matrix[0]) + 1) for _ in range(len(matrix) + 1)]
        for i, line in enumerate(matrix):
            previous = 0
            for j, num in enumerate(line):
                previous += num
                above = self.sum_[i][j + 1]
                self.sum_[i + 1][j + 1] = previous + above

    def sumRegion(self, row1, col1, row2, col2):
        sum_col2 = self.sum_[row2 + 1][col2 + 1] - self.sum_[row1][col2 + 1]
        sum_col1 = self.sum_[row2 + 1][col1] - self.sum_[row1][col1]
        return sum_col2 - sum_col1
```

## Complexity

- **Time:** `O(m * n)` for construction, `O(1)` per `sumRegion` call — the table is built once, and each query reads four entries.
- **Space:** `O(m * n)` — the prefix table has `(m + 1) * (n + 1)` entries.

## Other Approaches

- **Brute force:** sum every cell in the rectangle for each query — Time `O(m * n)` per query / Space `O(1)` extra
- **Row-wise prefix sums:** keep a 1D prefix sum per row and add up one value per row in the query range — Time `O(m * n)` build, `O(m)` per query / Space `O(m * n)`

## C++

```cpp
class NumMatrix {
public:

    vector<vector<int>> dp;

    NumMatrix(vector<vector<int>>& matrix) {
        int r = matrix.size(),c = matrix[0].size();
        dp = matrix;

        for(int i =0;i<r;i++){
            for(int j =0;j<c;j++){
                if(i>0) dp[i][j] += dp[i-1][j]; // add prev row
                if(j>0) dp[i][j] += dp[i][j-1]; // add prev col

                // remove diagonal as it is added twice above
                if(i>0&&j>0) dp[i][j] -= dp[i-1][j-1];
            }
        }
    }
    
    int sumRegion(int row1, int col1, int row2, int col2) {
        int answer = dp[row2][col2];

        if(row1>0) answer -= dp[row1-1][col2];  // remove prev row on col1
        if(col1>0) answer -= dp[row2][col1-1]; // remo prev col on row2

        // add prev diagonal as pre row and prev col both contains that value
        if(row1>0&&col1>0) answer += dp[row1-1][col1-1];
        return answer;
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */
```
