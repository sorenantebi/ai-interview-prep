---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
neetcode: https://neetcode.io/problems/best-time-to-buy-and-sell-stock-ii
---
# Best Time to Buy and Sell Stock II - Solution

## Intuition

Any rise from one peak-valley run can be split into day-to-day rises that sum to the same total. For example, going from 1 to 5 over days with prices 1, 2, 3, 4, 5 yields the same profit as collecting 1+1+1+1. So we never need to track explicit buy and sell days: we can simply collect every positive day-over-day gain and skip every drop.

## Approach

1. Initialize `profit = 0`.
2. Iterate over the array from the second day onward.
3. If `prices[i] > prices[i - 1]`, add the difference to `profit`.
4. Return `profit`.

## Code

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                max_profit += prices[i] - prices[i-1]
        return max_profit
```

## Complexity

- **Time:** `O(n)` — a single pass over the array.
- **Space:** `O(1)` — only a running total is stored.

## Other Approaches

- **Peak-valley scanning:** find each local minimum and the following local maximum and add their difference — Time `O(n)` / Space `O(1)`
- **Dynamic programming (hold / not hold):** track the best profit while holding and while not holding a share each day — Time `O(n)` / Space `O(1)`
- **Recursion with memoization:** try buy, sell, or skip at each day with state (day, holding) — Time `O(n)` / Space `O(n)`

## C++

```cpp
 /*
    Approach: 
    If stock price is going up tomorrow just buy it today and sell it tomorrow.
    
    Time complexity : O(n)
    Space complexity: O(1)

    n is number of days.
*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int ans =0;
        
        // look into the next day and if you are making profit just buy it today.
        for(int i =1;i<prices.size();i++){
            if(prices[i]>prices[i-1]) ans += (prices[i]-prices[i-1]);
        }
        return ans;
    }
};
```
