---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-a-2d-matrix/
neetcode: https://neetcode.io/problems/search-2d-matrix
---
# Search a 2D Matrix

**Topic:** Binary Search · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/search-a-2d-matrix/) · [NeetCode](https://neetcode.io/problems/search-2d-matrix)

## Problem

You are given an `m x n` integer matrix `matrix` with two properties:

- each row is sorted in non-decreasing order, and
- the first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` if `target` occurs in the matrix and `false` otherwise. The solution must run in `O(log(m * n))` time.

## Examples

**Example 1**
```text
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

**Example 2**
```text
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

## Constraints

- `m == matrix.length`, `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`
