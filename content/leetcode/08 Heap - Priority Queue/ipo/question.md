---
video: https://www.youtube.com/watch?v=1IUzNJ6TPEM
topic: "Heap - Priority Queue"
difficulty: Hard
leetcode: https://leetcode.com/problems/ipo/
neetcode: https://neetcode.io/problems/ipo
---
# IPO

**Topic:** Heap - Priority Queue · **Difficulty:** Hard

## Problem

LeetCode is about to go public and wants to raise its capital beforehand by completing a few projects. It can finish at most `k` distinct projects.

You are given `n` projects. The `i`-th project yields a pure profit of `profits[i]` and requires a minimum capital of `capital[i]` to start. You begin with `w` capital. Each time you finish a project, its profit is added to your current capital.

Choose at most `k` distinct projects so that your final capital is maximized, and return that final capital. The answer is guaranteed to fit in a 32-bit signed integer.

## Examples

**Example 1**
```text
Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
Output: 4
```
Explanation: With capital 0, only project 0 can be started. After it, capital is 1, so project 1 or 2 can be started. Picking project 2 gives the most: 0 + 1 + 3 = 4.

**Example 2**
```text
Input: k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
Output: 6
```

## Constraints

- `1 <= k <= 10^5`
- `0 <= w <= 10^9`
- `n == profits.length`
- `n == capital.length`
- `1 <= n <= 10^5`
- `0 <= profits[i] <= 10^4`
- `0 <= capital[i] <= 10^9`
