---
video: https://www.youtube.com/watch?v=3lpNp5Ojvrw
topic: "1-D Dynamic Programming"
difficulty: Easy
leetcode: https://leetcode.com/problems/n-th-tribonacci-number/
neetcode: https://neetcode.io/problems/n-th-tribonacci-number
---
# N-th Tribonacci Number

**Topic:** 1-D Dynamic Programming · **Difficulty:** Easy

## Problem

The Tribonacci sequence `T` is defined by `T0 = 0`, `T1 = 1`, `T2 = 1`, and for every `n >= 0`:

`T(n+3) = T(n) + T(n+1) + T(n+2)`

Given an integer `n`, return the value of `T(n)`.

## Examples

**Example 1**
```text
Input: n = 4
Output: 4
```
Explanation: `T3 = 0 + 1 + 1 = 2`, then `T4 = 1 + 1 + 2 = 4`.

**Example 2**
```text
Input: n = 25
Output: 1389537
```

## Constraints

- `0 <= n <= 37`
- The answer is guaranteed to fit within a 32-bit integer, i.e. `answer <= 2^31 - 1`.
