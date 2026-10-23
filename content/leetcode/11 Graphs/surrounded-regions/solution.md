---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/surrounded-regions/
neetcode: https://neetcode.io/problems/surrounded-regions
---
# Surrounded Regions - Solution

**Question:** Surrounded Regions - Question · **Difficulty:** Medium

## Intuition

It is hard to tell directly whether a region is surrounded, but it is easy to find the regions that are **not**: exactly those connected to a border `'O'`. Mark everything reachable from border `'O'`s as safe; every other `'O'` must be captured.

## Approach

1. For every `'O'` on the border, flood-fill (BFS) its region and temporarily mark those cells as `'T'` (safe).
2. Scan the whole board:
   - Remaining `'O'` cells are surrounded → flip to `'X'`.
   - `'T'` cells are safe → restore to `'O'`.

## Code

```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        flag = set()

        def dfs(r, c):
            if not(r in range(rows) and c in range(cols)) or board[r][c] != 'O' or (r, c) in flag:
                return
            flag.add((r, c))
            return (dfs(r + 1, c), dfs(r - 1, c), dfs(r, c + 1), dfs(r, c - 1))

        # traverse through the board
        for r in range(rows):
            for c in range(cols):
                if( (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and board[r][c] == 'O'):
                    dfs(r, c)

        # set all of the 'X's to 'O's
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O' and (r, c) not in flag:
                    board[r][c] = 'X'

    '''
    def solve(self, board: List[List[str]]) -> None:
        ROWS, COLS = len(board), len(board[0])

        def capture(r, c):
            if r < 0 or c < 0 or r == ROWS or c == COLS or board[r][c] != "O":
                return
            board[r][c] = "T"
            capture(r + 1, c)
            capture(r - 1, c)
            capture(r, c + 1)
            capture(r, c - 1)

        # 1. (DFS) Capture unsurrounded regions (O -> T)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O" and (r in [0, ROWS - 1] or c in [0, COLS - 1]):
                    capture(r, c)

        # 2. Capture surrounded regions (O -> X)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O":
                    board[r][c] = "X"

        # 3. Uncapture unsurrounded regions (T -> O)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "T":
                    board[r][c] = "O"
    '''
```

## Complexity

- **Time:** `O(m * n)` — each cell is visited a constant number of times.
- **Space:** `O(m * n)` — the BFS queue in the worst case; marking is done in place.

## Other Approaches

- **Union-Find with a virtual border node:** union border `'O'`s with a dummy node and adjacent `'O'`s with each other; flip any `'O'` not connected to the dummy — Time `O(m * n * α(mn))`, Space `O(m * n)`.

## Key Takeaway

Invert the question: instead of finding enclosed regions, find the ones that escape to the border and treat everything else as captured.
