---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/coin-change/
neetcode: https://neetcode.io/problems/coin-change
---
# Coin Change

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/coin-change/) · [NeetCode](https://neetcode.io/problems/coin-change)

## Problem

You have coins of the denominations in `coins` (an unlimited supply of each) and a target `amount`. Return the fewest coins whose values add up to exactly `amount`. If no combination works, return `-1`. An amount of `0` needs `0` coins.

## Examples

**Example 1**
```text
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1.
```

**Example 2**
```text
Input: coins = [2], amount = 3
Output: -1
```

**Example 3**
```text
Input: coins = [1], amount = 0
Output: 0
```

## Constraints

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`
