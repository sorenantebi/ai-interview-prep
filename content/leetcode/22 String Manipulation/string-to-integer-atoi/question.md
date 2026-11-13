---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/string-to-integer-atoi/
---
# String to Integer (atoi)

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

Implement `myAtoi(string s)`, which converts a string to a 32-bit signed integer.

The algorithm is as follows:

1. **Whitespace:** Ignore any leading whitespace (`" "`).
2. **Signedness:** Check whether the next character is `'-'` or `'+'`. If it is, that determines the sign; otherwise assume the number is positive.
3. **Conversion:** Read digits, skipping leading zeros, until a non-digit character or the end of the string is reached. If no digits were read, the result is `0`.
4. **Rounding:** If the integer is outside the 32-bit signed range `[-2^31, 2^31 - 1]`, clamp it to the range. Values below `-2^31` become `-2^31`, and values above `2^31 - 1` become `2^31 - 1`.

Return the resulting integer.

**Note:** You must not use any built-in function that converts a string to a number (such as `atoi`, `stoi`, `Integer.parseInt`, `int()`, `parseInt`, `Number()`). Perform the conversion manually.

## Examples

**Example 1**
```text
Input: s = "42"
Output: 42
```

**Example 2**
```text
Input: s = " -042"
Output: -42
```

**Example 3**
```text
Input: s = "1337c0d3"
Output: 1337
```

**Example 4**
```text
Input: s = "0-1"
Output: 0
```

**Example 5**
```text
Input: s = "words and 987"
Output: 0
```

## Constraints

- `0 <= s.length <= 200`
- `s` consists of English letters (lower-case and upper-case), digits (`0-9`), `' '`, `'+'`, `'-'`, and `'.'`.
