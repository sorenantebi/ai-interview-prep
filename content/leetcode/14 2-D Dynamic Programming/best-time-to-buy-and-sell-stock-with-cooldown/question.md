---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
neetcode: https://neetcode.io/problems/buy-and-sell-crypto-with-cooldown
---
# Best Time to Buy And Sell Stock With Cooldown

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · [NeetCode](https://neetcode.io/problems/buy-and-sell-crypto-with-cooldown)

## Problem

You are given an array `prices` where `prices[i]` is the price of a stock on day `i`. Find the maximum profit you can achieve. You may complete as many transactions as you like (buy one share and later sell it, repeatedly), subject to:

- You can hold at most one share at a time (you must sell before buying again).
- After selling, you must wait one day (**cooldown**) before buying again — you cannot buy on the day right after a sale.

Return the maximum profit (`0` if no profitable trade exists).

## Examples

**Example 1**
```text
Input: prices = [1,2,3,0,2]
Output: 3
Explanation: buy, sell, cooldown, buy, sell -> (2-1) + (2-0) = 3
```

**Example 2**
```text
Input: prices = [1]
Output: 0
```

## Constraints

- `1 <= prices.length <= 5000`
- `0 <= prices[i] <= 1000`
