---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/edit-distance/
neetcode: https://neetcode.io/problems/edit-distance
---
# Edit Distance - Solution

**Question:** Edit Distance - Question · **Difficulty:** Medium

## Intuition

Let `dp[i][j]` be the edit distance between `word1[:i]` and `word2[:j]`. If the last characters match, no operation is needed: `dp[i-1][j-1]`. Otherwise take `1 +` the best of delete (`dp[i-1][j]`), insert (`dp[i][j-1]`), or replace (`dp[i-1][j-1]`). Base cases: converting to/from an empty string costs its length.

## Approach

1. `prev = list(range(n + 1))` is row `i = 0` (insert `j` characters).
2. For each `i` from 1 to `m`, build `cur` with `cur[0] = i` (delete `i` characters), then fill `cur[j]` with the recurrence using `prev[j-1]`, `prev[j]`, `cur[j-1]`.
3. After all rows, return `prev[n]`.

## Code

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        dp = [[float("inf")] * (len(word2) + 1) for i in range(len(word1) + 1)]

        for j in range(len(word2) + 1):
            dp[len(word1)][j] = len(word2) - j
        for i in range(len(word1) + 1):
            dp[i][len(word2)] = len(word1) - i

        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j + 1], dp[i + 1][j + 1])
        return dp[0][0]
```

## Complexity

- **Time:** `O(m * n)` — each prefix pair evaluated once.
- **Space:** `O(n)` — two rows.

## Other Approaches

- **Full 2-D table:** same recurrence; allows backtracking the actual edit script — Time `O(mn)`, Space `O(mn)`.
- **Memoized recursion on `(i, j)`:** top-down version — Time `O(mn)`, Space `O(mn)` plus recursion stack.

## Key Takeaway

Edit distance is the template for two-string alignment DPs: match -> diagonal, mismatch -> 1 + min(up, left, diagonal).
