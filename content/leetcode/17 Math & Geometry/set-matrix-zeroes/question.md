---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/set-matrix-zeroes/
neetcode: https://neetcode.io/problems/set-zeroes-in-matrix
---
# Set Matrix Zeroes

**Topic:** Math & Geometry · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/set-matrix-zeroes/) · [NeetCode](https://neetcode.io/problems/set-zeroes-in-matrix)

## Problem

You are given an `m x n` integer `matrix`. Wherever an element is `0`, set its **entire row and entire column** to `0`.

Only zeros that were in the original matrix count; zeros created by this process must not spread further. The update must be done **in place**. As a follow-up, try to use only constant extra space.

## Examples

**Example 1**
```text
Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

**Example 2**
```text
Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

## Constraints

- `m == matrix.length`, `n == matrix[0].length`
- `1 <= m, n <= 200`
- `-2^31 <= matrix[i][j] <= 2^31 - 1`
