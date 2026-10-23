---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/coin-change-ii/
neetcode: https://neetcode.io/problems/coin-change-ii
---
# Coin Change II

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/coin-change-ii/) · [NeetCode](https://neetcode.io/problems/coin-change-ii)

## Problem

You are given an integer `amount` and an array `coins` of distinct coin denominations. Each denomination may be used an unlimited number of times. Return the number of **combinations** of coins that add up exactly to `amount` (order does not matter, so `1+2` and `2+1` count once). If the amount cannot be formed, return `0`. An `amount` of `0` has exactly one combination (use no coins).

The answer fits in a 32-bit signed integer.

## Examples

**Example 1**
```text
Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: 5 = 5 = 2+2+1 = 2+1+1+1 = 1+1+1+1+1
```

**Example 2**
```text
Input: amount = 3, coins = [2]
Output: 0
```

**Example 3**
```text
Input: amount = 10, coins = [10]
Output: 1
```

## Constraints

- `1 <= coins.length <= 300`
- `1 <= coins[i] <= 5000`, all values distinct
- `0 <= amount <= 5000`
