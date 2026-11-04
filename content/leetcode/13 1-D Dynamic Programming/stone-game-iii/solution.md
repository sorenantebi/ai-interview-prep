---
topic: "1-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/stone-game-iii/
neetcode: https://neetcode.io/problems/stone-game-iii
---
# Stone Game III - Solution

## Intuition

Instead of tracking both scores, track the score *difference* (current player minus opponent) for the game starting at index `i`. Since the opponent plays optimally from the next position with the same objective, the current player's best difference is the value they take minus the opponent's best difference from the remaining stones.

## Approach

1. Let `dp[i]` be the best achievable difference (current player's score minus the opponent's) when the game starts with stones `i..n-1`. Set `dp[n] = 0`.
2. For `i` from `n-1` down to `0`, try taking `k` stones for `k` in 1..3 (while `i + k <= n`). Accumulate the taken sum and set `dp[i] = max(taken - dp[i + k])`.
3. Look at `dp[0]`: positive means Alice wins, negative means Bob wins, zero means a tie.
4. Only the next three states are needed, so a rolling array of size 4 suffices.

## Code

```python
from typing import List, Optional

class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        dp = [0] * (n + 4)
        for i in range(n - 1, -1, -1):
            best = float("-inf")
            taken = 0
            for k in range(1, 4):
                if i + k > n:
                    break
                taken += stoneValue[i + k - 1]
                best = max(best, taken - dp[i + k])
            dp[i] = best
        if dp[0] > 0:
            return "Alice"
        if dp[0] < 0:
            return "Bob"
        return "Tie"
```

## Complexity

- **Time:** `O(n)` — each position considers at most 3 moves.
- **Space:** `O(n)` — the `dp` array; this can be reduced to `O(1)` with a rolling window of 4 values.

## Other Approaches

- **Top-down memoization:** recursion on the start index with the same difference recurrence, cached — Time `O(n)` / Space `O(n)` (recursion depth up to `n`)
- **Rolling array:** keep only `dp[i+1..i+3]` instead of the full table — Time `O(n)` / Space `O(1)`
- **Brute-force recursion:** try all 1–3 stone moves without caching — Time `O(3^n)` / Space `O(n)`
