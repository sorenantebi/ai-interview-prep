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

## C++

```cpp
/*
    Given array prices, return max profit w/ 1 buy & 1 sell
    Ex. prices = [7,1,5,3,6,4] -> 5 (buy at $1, sell at $6)

    For each, get diff b/w that & min value before, store max

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxP = 0, l = 0, r = 0;
        while (r < prices.size()){
            if (prices[r] > prices[l])
                maxP = max(maxP, prices[r] - prices[l]);
            else
                l = r;
            ++r;
        }
        return maxP;
    }
};
```
