---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/valid-sudoku/
neetcode: https://neetcode.io/problems/valid-sudoku
---
# Valid Sudoku - Solution

**Question:** Valid Sudoku - Question · **Difficulty:** Medium

## Intuition

Each filled cell belongs to exactly one row, one column, and one `3 x 3` box (box index `(r // 3, c // 3)`). Keep a set of seen digits for every row, column, and box; scanning the board once, a digit already present in any of its three sets means the board is invalid.

## Approach

1. Create 9 sets for rows, 9 for columns, and 9 for boxes.
2. For each cell `(r, c)` with digit `d` (skip `"."`):
   - Compute `b = (r // 3) * 3 + c // 3`.
   - If `d` is in `rows[r]`, `cols[c]`, or `boxes[b]`, return `False`.
   - Otherwise add `d` to all three sets.
3. Return `True` after the scan.

## Code

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        cols = collections.defaultdict(set)
        rows = collections.defaultdict(set)
        squares = collections.defaultdict(set)  # key = (r /3, c /3)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                if (
                    board[r][c] in rows[r]
                    or board[r][c] in cols[c]
                    or board[r][c] in squares[(r // 3, c // 3)]
                ):
                    return False
                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                squares[(r // 3, c // 3)].add(board[r][c])

        return True
```

## Complexity

- **Time:** `O(1)` — the board is fixed at 81 cells (`O(n^2)` for a general `n x n` board).
- **Space:** `O(1)` — 27 sets of at most 9 digits each (`O(n^2)` in general).

## Other Approaches

- **Three separate passes:** validate all rows, then all columns, then all boxes — same complexity, more code.
- **Bitmasks:** replace each set with a 9-bit integer and test `mask & (1 << d)` — Time `O(1)`, Space `O(1)`, faster constants.

## Key Takeaway

Map each cell to its constraint groups with simple index arithmetic (`(r // 3) * 3 + c // 3` for the box) and use one hash set per group to detect conflicts in a single pass.
