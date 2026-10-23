---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/coin-change/
neetcode: https://neetcode.io/problems/coin-change
---
# Coin Change - Solution

**Question:** Coin Change - Question · **Difficulty:** Medium

## Intuition

Greedy (largest coin first) fails, e.g. `[1,3,4]` for `6` gives `4+1+1` instead of `3+3`. Instead use unbounded-knapsack DP: `dp[a]` = fewest coins for amount `a`, built bottom-up via `dp[a] = 1 + min(dp[a - c])` over coins `c <= a`.

## Approach

1. `dp = [0] + [INF] * amount`, where `INF = amount + 1` (more coins than could ever be needed, so it means "unreachable").
2. For `a` from 1 to `amount`, for each coin `c <= a`, `dp[a] = min(dp[a], dp[a - c] + 1)`.
3. Return `dp[amount]` if finite, else `-1`.

## Code

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0

        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])
        return dp[amount] if dp[amount] != amount + 1 else -1
```

## Complexity

- **Time:** `O(amount · len(coins))` — each amount tries every coin.
- **Space:** `O(amount)` — the DP array.

## Other Approaches

- **BFS over amounts:** each level adds one coin; first time you hit `amount` is the answer — Time `O(amount · len(coins))`, Space `O(amount)`.
- **Memoised recursion:** `f(a) = 1 + min f(a - c)` — same complexity, plus recursion stack.

## Key Takeaway

Minimum-count with unlimited reuse is unbounded knapsack; when greedy looks tempting, test a counterexample like `[1,3,4], 6`.
