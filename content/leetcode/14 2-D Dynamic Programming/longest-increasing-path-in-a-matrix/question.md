---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
neetcode: https://neetcode.io/problems/longest-increasing-path-in-matrix
---
# Longest Increasing Path In a Matrix

**Topic:** 2-D Dynamic Programming · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) · [NeetCode](https://neetcode.io/problems/longest-increasing-path-in-matrix)

## Problem

Given an `m x n` integer matrix, return the length of the longest **strictly increasing** path in it. From any cell you can move to one of its four neighbours (up, down, left, right); diagonal moves and wrapping around the border are not allowed. The path length counts cells.

## Examples

**Example 1**
```text
Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
Output: 4
Explanation: 1 -> 2 -> 6 -> 9
```

**Example 2**
```text
Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
Output: 4
Explanation: 3 -> 4 -> 5 -> 6
```

**Example 3**
```text
Input: matrix = [[1]]
Output: 1
```

## Constraints

- `m == matrix.length`, `n == matrix[i].length`
- `1 <= m, n <= 200`
- `0 <= matrix[i][j] <= 2^31 - 1`
