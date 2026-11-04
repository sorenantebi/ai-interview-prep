---
video: https://www.youtube.com/watch?v=DzMT3bDgVn0
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/transpose-matrix/
neetcode: https://neetcode.io/problems/transpose-matrix
---
# Transpose Matrix

**Topic:** Math & Geometry · **Difficulty:** Easy

## Problem

You are given a 2D integer array `matrix`. Return its transpose.

The transpose of a matrix is the matrix flipped over its main diagonal, so that the row and column indices of every element are swapped: the element at position `(i, j)` in the original ends up at position `(j, i)` in the result.

## Examples

**Example 1**
```text
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[1,4,7],[2,5,8],[3,6,9]]
```

**Example 2**
```text
Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 1000`
- `1 <= m * n <= 10^5`
- `-10^9 <= matrix[i][j] <= 10^9`
