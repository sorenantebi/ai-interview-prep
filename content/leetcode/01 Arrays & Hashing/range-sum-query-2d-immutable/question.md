---
video: https://www.youtube.com/watch?v=KE8MQuwE2yA
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/range-sum-query-2d-immutable/
neetcode: https://neetcode.io/problems/range-sum-query-2d-immutable
---
# Range Sum Query 2D - Immutable

**Topic:** Arrays & Hashing · **Difficulty:** Medium

## Problem

You are given a 2D integer matrix and must answer many queries about it. Each query asks for the sum of all elements inside a rectangle, defined by its upper left corner `(row1, col1)` and its lower right corner `(row2, col2)`, both corners inclusive.

Implement the `NumMatrix` class:

- `NumMatrix(int[][] matrix)` initializes the object with the integer matrix `matrix`.
- `int sumRegion(int row1, int col1, int row2, int col2)` returns the sum of the elements of `matrix` inside the rectangle defined by its upper left corner `(row1, col1)` and lower right corner `(row2, col2)`.

You must design an algorithm where `sumRegion` runs in `O(1)` time.

## Examples

**Example 1**
```text
Input:
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
Output:
[null, 8, 11, 12]
```

Explanation:
```text
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8
numMatrix.sumRegion(1, 1, 2, 2); // return 11
numMatrix.sumRegion(1, 2, 2, 4); // return 12
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 200`
- `-10^4 <= matrix[i][j] <= 10^4`
- `0 <= row1 <= row2 < m`
- `0 <= col1 <= col2 < n`
- At most `10^4` calls will be made to `sumRegion`.
