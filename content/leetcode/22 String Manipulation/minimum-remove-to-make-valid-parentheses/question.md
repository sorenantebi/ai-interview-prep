---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/
---
# Minimum Remove to Make Valid Parentheses

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

You are given a string `s` made up of `'('`, `')'`, and lowercase English letters.

Remove the smallest possible number of parentheses (either `'('` or `')'`, from any positions) so that the remaining string has valid parentheses, and return any such valid string.

A parentheses string is valid if and only if it:

- is the empty string, or contains only lowercase letters, or
- can be written as `AB` (`A` concatenated with `B`), where `A` and `B` are valid strings, or
- can be written as `(A)`, where `A` is a valid string.

## Examples

**Example 1**
```text
Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"
Explanation: "lee(t(co)de)" and "lee(t(c)ode)" would also be accepted.
```

**Example 2**
```text
Input: s = "a)b(c)d"
Output: "ab(c)d"
```

**Example 3**
```text
Input: s = "))(("
Output: ""
Explanation: An empty string is also valid.
```

## Constraints

- `1 <= s.length <= 10^5`
- `s[i]` is either `'('`, `')'`, or a lowercase English letter.
