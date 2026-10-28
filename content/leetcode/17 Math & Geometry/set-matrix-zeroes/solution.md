---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/set-matrix-zeroes/
neetcode: https://neetcode.io/problems/set-zeroes-in-matrix
---
# Set Matrix Zeroes - Solution

**Question:** Set Matrix Zeroes - Question · **Difficulty:** Medium

## Intuition

The `O(m + n)` approach records which rows and columns contain a zero. To get `O(1)` extra space, store those markers in the matrix itself: `matrix[0][c]` marks column `c` and `matrix[r][0]` marks row `r`. The top-left cell `matrix[0][0]` would have to mark both row 0 and column 0, so keep one extra boolean, `first_row_zero`, for row 0. Apply the inner markers before clearing row 0 and column 0, because clearing them first would wipe out the markers.

## Approach

1. Scan every cell. When `matrix[r][c] == 0`, set `matrix[0][c] = 0`. Also set `matrix[r][0] = 0` if `r > 0`, or `first_row_zero = True` if `r == 0`.
2. For `r` in `1..m-1` and `c` in `1..n-1`, set `matrix[r][c] = 0` if `matrix[0][c] == 0` or `matrix[r][0] == 0`.
3. If `matrix[0][0] == 0`, column 0 must be zeroed: set `matrix[r][0] = 0` for all `r`.
4. If `first_row_zero`, set all of row 0 to zero.

## Code

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        # O(1)
        ROWS, COLS = len(matrix), len(matrix[0])
        rowZero = False

        # determine which rows/cols need to be zero
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0
                    if r > 0:
                        matrix[r][0] = 0
                    else:
                        rowZero = True

        for r in range(1, ROWS):
            for c in range(1, COLS):
                if matrix[0][c] == 0 or matrix[r][0] == 0:
                    matrix[r][c] = 0

        if matrix[0][0] == 0:
            for r in range(ROWS):
                matrix[r][0] = 0

        if rowZero:
            for c in range(COLS):
                matrix[0][c] = 0
```

## Complexity

- **Time:** `O(m * n)`: a constant number of passes over the grid.
- **Space:** `O(1)`: the markers are stored in the matrix itself, plus one boolean.

## Other Approaches

- **Row/column sets:** record the zero rows and zero columns in two sets, then make a second pass. Time `O(m * n)`, Space `O(m + n)`.
- **Copy the matrix:** read zeros from a copy and write into the original. Time `O(m * n * (m + n))` if done naively, Space `O(m * n)`.

## Key Takeaway

To meet an `O(1)` space requirement on a grid, reuse its first row and column as bookkeeping. Watch the shared corner cell, and process the marker row and column last.

## C++

```cpp
/*
    Given matrix, if element 0, set entire row/col to 0

    Use 1st row/col as flag to determine if entire row/col 0

    Time: O(mn)
    Space: O(1)
*/

class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size();
        int n = matrix[0].size();
        
        bool isFirstRowZero = false;
        bool isFirstColZero = false;
        
        for (int i = 0; i < m; i++) {
            if (matrix[i][0] == 0) {
                isFirstColZero = true;
                break;
            }
        }
        
        for (int j = 0; j < n; j++) {
            if (matrix[0][j] == 0) {
                isFirstRowZero = true;
                break;
            }
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }
            }
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
        }
        
        if (isFirstColZero) {
            for (int i = 0; i < m; i++) {
                matrix[i][0] = 0;
            }
        }
        
        if (isFirstRowZero) {
            for (int j = 0; j < n; j++) {
                matrix[0][j] = 0;
            }
        }
    }
};
```
