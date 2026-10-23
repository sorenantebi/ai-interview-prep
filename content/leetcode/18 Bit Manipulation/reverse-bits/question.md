---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/reverse-bits/
neetcode: https://neetcode.io/problems/reverse-bits
---
# Reverse Bits

**Topic:** Bit Manipulation · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/reverse-bits/) · [NeetCode](https://neetcode.io/problems/reverse-bits)

## Problem

Given an integer `n`, treat it as a **32-bit unsigned** value. Reverse the order of its 32 bits, so bit 0 swaps with bit 31, bit 1 with bit 30, and so on. Return the resulting integer.

(LeetCode's current version only gives even `n` in `[0, 2^31 - 2]`. A general solution handles any 32-bit unsigned input.)

## Examples

**Example 1**
```text
Input: n = 43261596
Output: 964176192
Explanation: 00000010100101000001111010011100 reversed is 00111001011110000010100101000000
```

**Example 2**
```text
Input: n = 2147483644
Output: 1073741822
Explanation: 01111111111111111111111111111100 reversed is 00111111111111111111111111111110
```

## Constraints

- `0 <= n <= 2^32 - 1` (32-bit unsigned input)
- Follow-up: if this function is called many times, how would you optimize it?
