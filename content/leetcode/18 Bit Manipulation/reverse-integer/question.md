---
topic: "Bit Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-integer/
neetcode: https://neetcode.io/problems/reverse-integer
---
# Reverse Integer

**Topic:** Bit Manipulation · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/reverse-integer/) · [NeetCode](https://neetcode.io/problems/reverse-integer)

## Problem

Given a signed 32-bit integer `x`, return `x` with its decimal digits reversed, keeping its sign. If the reversed value falls outside the signed 32-bit range `[-2^31, 2^31 - 1]`, return `0`.

Assume the environment cannot store 64-bit integers, so the overflow must be detected without computing the full out-of-range value.

## Examples

**Example 1**
```text
Input: x = 123
Output: 321
```

**Example 2**
```text
Input: x = -123
Output: -321
```

**Example 3**
```text
Input: x = 120
Output: 21
```

## Constraints

- `-2^31 <= x <= 2^31 - 1`
