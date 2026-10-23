---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/spiral-matrix/
neetcode: https://neetcode.io/problems/spiral-matrix
---
# Spiral Matrix

**Topic:** Math & Geometry · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/spiral-matrix/) · [NeetCode](https://neetcode.io/problems/spiral-matrix)

## Problem

Given an `m x n` `matrix`, return all of its elements in **spiral order**. Start at the top-left corner, go right along the top row, down the right column, left along the bottom row, up the left column, and keep spiralling inward until every element has been visited exactly once.

## Examples

**Example 1**
```text
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Example 2**
```text
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

## Constraints

- `m == matrix.length`, `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`
