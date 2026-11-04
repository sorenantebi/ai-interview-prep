---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/stone-game-ii/
neetcode: https://neetcode.io/problems/stone-game-ii
---
# Stone Game II - Solution

## Intuition

The state of the game is fully described by two values: the index `i` of the first remaining pile and the current `M`. Since both players are optimal and the total is fixed, the player to move wants to maximize the stones they collect from the suffix `piles[i:]`. Taking `X` piles leaves the opponent a smaller subgame, and whatever the opponent does not get from the suffix is ours.

## Approach

1. Build suffix sums so `suffix[i]` is the total stones in `piles[i:]`.
2. Define `dp(i, M)` as the maximum stones the current player can collect from `piles[i:]` with the given `M`.
3. If `i + 2M >= n`, the player can take everything: `dp(i, M) = suffix[i]`.
4. Otherwise, try every `X` in `1..2M`. After taking `X` piles, the opponent gets `dp(i + X, max(M, X))`, so we get `suffix[i] - dp(i + X, max(M, X))`. Take the maximum over `X`.
5. Memoize on `(i, M)` and return `dp(0, 1)`.

## Code

```python
from typing import List, Optional
from functools import lru_cache

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]

        @lru_cache(maxsize=None)
        def dp(i: int, M: int) -> int:
            if i + 2 * M >= n:
                return suffix[i]
            best = 0
            for X in range(1, 2 * M + 1):
                # opponent plays optimally on the rest; we keep the remainder
                best = max(best, suffix[i] - dp(i + X, max(M, X)))
            return best

        return dp(0, 1)
```

## Complexity

- **Time:** `O(n^3)` — there are `O(n^2)` states `(i, M)` (with `M <= n`), and each tries up to `2M = O(n)` moves.
- **Space:** `O(n^2)` — memo table over `(i, M)`, plus `O(n)` for suffix sums and recursion depth.

## Other Approaches

- **Bottom-up DP table:** iterate `i` from `n-1` down to `0` and `M` from `1` to `n`, filling `dp[i][M]` with the same recurrence — Time `O(n^3)` / Space `O(n^2)`
- **Minimax without memoization:** plain recursion over all move sequences — Time exponential / Space `O(n)`
