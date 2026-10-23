---
topic: "Sliding Window"
difficulty: Easy
leetcode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
neetcode: https://neetcode.io/problems/buy-and-sell-crypto
---
# Best Time to Buy And Sell Stock - Solution

**Question:** Best Time to Buy And Sell Stock - Question · **Difficulty:** Easy

## Intuition

For every possible selling day, the best buying day is the cheapest day before it. Scan once while tracking the minimum price seen so far; the profit for selling today is `price - minSoFar`. This is a sliding window whose left edge jumps to any new minimum.

## Approach

1. Set `min_price = inf`, `best = 0`.
2. For each `p` in `prices`:
   - Update `min_price = min(min_price, p)`.
   - Update `best = max(best, p - min_price)`.
3. Return `best`.

## Code

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        res = 0
        
        lowest = prices[0]
        for price in prices:
            if price < lowest:
                lowest = price
            res = max(res, price - lowest)
        return res
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — two variables.

## Other Approaches

- **Brute force:** try every buy/sell pair — Time `O(n^2)`, Space `O(1)`.
- **Two pointers (l = buy, r = sell):** move `l` to `r` whenever `prices[r] < prices[l]` — Time `O(n)`, Space `O(1)`; equivalent to the running minimum.

## Key Takeaway

"Best pair with i < j" problems often reduce to tracking a running min/max of the prefix while scanning.
