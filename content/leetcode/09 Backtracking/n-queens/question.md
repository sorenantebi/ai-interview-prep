---
topic: "Backtracking"
difficulty: Hard
leetcode: https://leetcode.com/problems/n-queens/
neetcode: https://neetcode.io/problems/n-queens
---
# N Queens

**Topic:** Backtracking · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/n-queens/) · [NeetCode](https://neetcode.io/problems/n-queens)

## Problem

Place `n` queens on an `n x n` chessboard so that no two queens attack each other — no two share a row, a column, or a diagonal.

Given `n`, return **all** distinct solutions in any order. Each solution is a list of `n` strings representing the rows of the board, where `'Q'` marks a queen and `'.'` an empty square.

## Examples

**Example 1**
```text
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
```

**Example 2**
```text
Input: n = 1
Output: [["Q"]]
```

## Constraints

- `1 <= n <= 9`
