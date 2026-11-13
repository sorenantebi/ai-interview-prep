---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/basic-calculator-ii/
---
# Basic Calculator II

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

Given a string `s` representing an arithmetic expression, evaluate it and return its value. The expression contains non-negative integers and the operators `+`, `-`, `*`, `/`, separated by any number of spaces. Integer division truncates toward zero.

You may assume the expression is always valid, and that all intermediate results lie in the range `[-2^31, 2^31 - 1]`.

You are not allowed to use any built-in function that evaluates strings as mathematical expressions, such as `eval()`.

## Examples

**Example 1**
```text
Input: s = "3+2*2"
Output: 7
```

**Example 2**
```text
Input: s = " 3/2 "
Output: 1
```

**Example 3**
```text
Input: s = " 3+5 / 2 "
Output: 5
```

## Constraints

- `1 <= s.length <= 3 * 10^5`
- `s` consists of integers and operators (`'+'`, `'-'`, `'*'`, `'/'`) separated by some number of spaces.
- `s` represents a valid expression.
- All the integers in the expression are non-negative integers in the range `[0, 2^31 - 1]`.
- The answer is guaranteed to fit in a 32-bit integer.
