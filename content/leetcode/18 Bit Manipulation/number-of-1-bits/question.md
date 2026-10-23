---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/number-of-1-bits/
neetcode: https://neetcode.io/problems/number-of-one-bits
---
# Number of 1 Bits

**Topic:** Bit Manipulation · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/number-of-1-bits/) · [NeetCode](https://neetcode.io/problems/number-of-one-bits)

## Problem

Given a positive integer `n`, return the number of `1` bits in its binary representation. This count is also called the **Hamming weight** or population count.

(Older versions of this problem passed `n` as a 32-bit unsigned integer, so values up to `2^32 - 1` should also work.)

## Examples

**Example 1**
```text
Input: n = 11
Output: 3
Explanation: 11 = 0b1011 has three set bits.
```

**Example 2**
```text
Input: n = 128
Output: 1
Explanation: 128 = 0b10000000
```

**Example 3**
```text
Input: n = 2147483645
Output: 30
Explanation: 0b1111111111111111111111111111101 has thirty set bits.
```

## Constraints

- `1 <= n <= 2^31 - 1`
