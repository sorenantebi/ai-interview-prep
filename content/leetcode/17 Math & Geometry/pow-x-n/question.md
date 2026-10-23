---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/powx-n/
neetcode: https://neetcode.io/problems/pow-x-n
---
# Pow(x, n)

**Topic:** Math & Geometry · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/powx-n/) · [NeetCode](https://neetcode.io/problems/pow-x-n)

## Problem

Implement `pow(x, n)`, which returns `x` raised to the integer power `n` (that is, `x^n`). The exponent `n` can be negative, in which case the result is `1 / x^(-n)`. Do not use a built-in power function. Results are accepted if they are within a small floating-point tolerance of the true value.

## Examples

**Example 1**
```text
Input: x = 2.00000, n = 10
Output: 1024.00000
```

**Example 2**
```text
Input: x = 2.10000, n = 3
Output: 9.26100
```

**Example 3**
```text
Input: x = 2.00000, n = -2
Output: 0.25000
Explanation: 2^-2 = 1 / 2^2 = 1/4 = 0.25
```

## Constraints

- `-100.0 < x < 100.0`
- `-2^31 <= n <= 2^31 - 1`
- `n` is an integer.
- Either `x` is not zero or `n > 0`.
- `-10^4 <= x^n <= 10^4`
