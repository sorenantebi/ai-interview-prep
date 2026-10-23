---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
neetcode: https://neetcode.io/problems/buy-and-sell-crypto-with-cooldown
---
# Best Time to Buy And Sell Stock With Cooldown - Solution

**Question:** Best Time to Buy And Sell Stock With Cooldown - Question · **Difficulty:** Medium

## Intuition

At the end of each day you are in one of three states: **holding** a share, **just sold** today (so tomorrow is a cooldown), or **resting** (no share, free to buy). Each state's best profit depends only on the previous day's states, giving a tiny state machine DP.

## Approach

1. Initialize `hold = -inf`, `sold = 0`, `rest = 0`.
2. For each price `p`, compute the new states from the old ones:
   - `hold' = max(hold, rest - p)` — keep holding, or buy today (only allowed from `rest`).
   - `sold' = hold + p` — sell the share held yesterday.
   - `rest' = max(rest, sold)` — keep resting, or finish yesterday's cooldown.
3. Return `max(sold, rest)` (ending while holding is never optimal).

## Code

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # State: Buying or Selling?
        # If Buy -> i + 1
        # If Sell -> i + 2

        dp = {}  # key=(i, buying) val=max_profit

        def dfs(i, buying):
            if i >= len(prices):
                return 0
            if (i, buying) in dp:
                return dp[(i, buying)]

            cooldown = dfs(i + 1, buying)
            if buying:
                buy = dfs(i + 1, not buying) - prices[i]
                dp[(i, buying)] = max(buy, cooldown)
            else:
                sell = dfs(i + 2, not buying) + prices[i]
                dp[(i, buying)] = max(sell, cooldown)
            return dp[(i, buying)]

        return dfs(0, True)
```

## Complexity

- **Time:** `O(n)` — one pass over the prices.
- **Space:** `O(1)` — three state variables.

## Other Approaches

- **Memoized DFS on `(i, canBuy)`:** at each day choose buy/sell (jumping `i + 2` after a sell) or skip — Time `O(n)`, Space `O(n)`.
- **Two arrays `buy[i]`, `sell[i]`:** `buy[i] = max(buy[i-1], sell[i-2] - p)` — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Stock problems with extra rules (cooldown, fee, k transactions) become a small finite-state DP: name the states, write the transitions, update them simultaneously each day.
