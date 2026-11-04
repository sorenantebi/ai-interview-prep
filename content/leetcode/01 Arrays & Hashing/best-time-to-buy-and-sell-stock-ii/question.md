---
video: https://www.youtube.com/watch?v=3SJ3pUkPQMc
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
neetcode: https://neetcode.io/problems/best-time-to-buy-and-sell-stock-ii
---
# Best Time to Buy and Sell Stock II

**Topic:** Arrays & Hashing · **Difficulty:** Medium

## Problem

You are given an integer array `prices`, where `prices[i]` is the price of a stock on day `i`.

On each day you may buy and/or sell the stock. You can hold at most one share at any time, but you may buy and sell as many times as you like, including buying and selling on the same day, as long as you never hold more than one share.

Return the maximum profit you can achieve.

## Examples

**Example 1**
```text
Input: prices = [7,1,5,3,6,4]
Output: 7
```
Buy on day 2 (price = 1) and sell on day 3 (price = 5) for a profit of 4. Then buy on day 4 (price = 3) and sell on day 5 (price = 6) for a profit of 3. Total profit is 7.

**Example 2**
```text
Input: prices = [1,2,3,4,5]
Output: 4
```
Buy on day 1 (price = 1) and sell on day 5 (price = 5) for a profit of 4.

**Example 3**
```text
Input: prices = [7,6,4,3,1]
Output: 0
```
Prices only fall, so no profitable trade exists and the maximum profit is 0.

## Constraints

- `1 <= prices.length <= 3 * 10^4`
- `0 <= prices[i] <= 10^4`
