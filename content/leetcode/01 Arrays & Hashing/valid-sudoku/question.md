---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/valid-sudoku/
neetcode: https://neetcode.io/problems/valid-sudoku
---
# Valid Sudoku

**Topic:** Arrays & Hashing · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/valid-sudoku/) · [NeetCode](https://neetcode.io/problems/valid-sudoku)

## Problem

You are given a partially filled `9 x 9` Sudoku board as a grid of strings, where each cell is a digit `"1"`–`"9"` or `"."` for an empty cell. Decide whether the board is **valid** so far, meaning that among the filled cells:

1. No row contains the same digit twice.
2. No column contains the same digit twice.
3. None of the nine `3 x 3` sub-boxes contains the same digit twice.

Only the filled cells need to be checked. A valid board does not have to be solvable.

## Examples

**Example 1**
```text
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
```

**Example 2**
```text
Input: the same board, but with the top-left "5" replaced by "8"
Output: false
Explanation: column 0 (and the top-left box) now contains two 8s.
```

## Constraints

- `board.length == 9` and `board[i].length == 9`
- `board[i][j]` is a digit `"1"`–`"9"` or `"."`.
