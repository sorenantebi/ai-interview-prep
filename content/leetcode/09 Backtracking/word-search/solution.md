---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/word-search/
neetcode: https://neetcode.io/problems/search-for-word
---
# Word Search - Solution

**Question:** Word Search - Question · **Difficulty:** Medium

## Intuition

Try every cell as a starting point and run a DFS that matches `word` one character at a time, moving to the four neighbors. Mark a cell as visited while it is on the current path (temporarily overwrite it) and restore it when backtracking, so it can be used by other paths.

## Approach

1. Quick prune: if the board lacks enough copies of some letter in `word`, return `false`. Optionally reverse `word` if its last letter is rarer than its first, to cut branching early.
2. `dfs(r, c, i)`: return `true` if `i == len(word)`; return `false` if out of bounds or `board[r][c] != word[i]`.
3. Temporarily set `board[r][c] = "#"`, recurse into the four neighbors with `i + 1`, then restore the cell.
4. Return `true` if any start cell's DFS succeeds.

## Code

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        ROWS, COLS = len(board), len(board[0])
        path = set()

        def dfs(r, c, i):
            if i == len(word):
                return True
            if (
                min(r, c) < 0
                or r >= ROWS
                or c >= COLS
                or word[i] != board[r][c]
                or (r, c) in path
            ):
                return False
            path.add((r, c))
            res = (
                dfs(r + 1, c, i + 1)
                or dfs(r - 1, c, i + 1)
                or dfs(r, c + 1, i + 1)
                or dfs(r, c - 1, i + 1)
            )
            path.remove((r, c))
            return res

        # To prevent TLE,reverse the word if frequency of the first letter is more than the last letter's
        count = sum(map(Counter, board), Counter())
        if count[word[0]] > count[word[-1]]:
            word = word[::-1]
            
        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False

    # O(n * m * 4^n)
```

## Complexity

- **Time:** `O(m * n * 3^L)` — each of the `m*n` starts explores at most 3 new directions per step for `L = len(word)` steps.
- **Space:** `O(L)` — recursion depth (the board is marked in place).

## Other Approaches

- **Visited set instead of in-place marking:** store `(r, c)` on the path in a set — same time, `O(L)` extra space, leaves the board untouched throughout.

## Key Takeaway

Grid path search = DFS from every cell with in-place "visited" marking that is undone on return; frequency checks and starting from the rarer end are cheap, powerful prunes.
