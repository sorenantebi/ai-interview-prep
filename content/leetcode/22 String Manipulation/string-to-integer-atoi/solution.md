---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/string-to-integer-atoi/
---
# String to Integer (atoi) - Solution

## Intuition

The problem is a straightforward state machine: skip whitespace, read an optional sign, then accumulate digits until something else appears. The only subtlety is overflow: rather than building a huge number and clamping afterward, check before each multiplication whether the next digit would push the value past the 32-bit limit.

## Approach

1. Set an index `i = 0` and skip all leading spaces.
2. If `i` is in range and `s[i]` is `'+'` or `'-'`, record the sign and advance.
3. While `s[i]` is a digit, compute its value as `ord(s[i]) - ord('0')`.
4. Before updating `result = result * 10 + digit`, check whether `result > INT_MAX // 10`, or `result == INT_MAX // 10` and `digit > 7`. If so, return `INT_MAX` for positive or `INT_MIN` for negative.
5. Otherwise update the result and advance.
6. Return `sign * result`.

## Code

```python
from typing import List, Optional

class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        n = len(s)
        i = 0

        while i < n and s[i] == ' ':
            i += 1

        sign = 1
        if i < n and s[i] in '+-':
            if s[i] == '-':
                sign = -1
            i += 1

        result = 0
        while i < n and '0' <= s[i] <= '9':
            digit = ord(s[i]) - ord('0')
            # Detect overflow before it happens; INT_MAX ends in 7
            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
                return INT_MAX if sign == 1 else INT_MIN
            result = result * 10 + digit
            i += 1

        return sign * result
```

## Complexity

- **Time:** `O(n)` — each character is visited at most once.
- **Space:** `O(1)` — only a few integer variables are used.

## Other Approaches

- **Accumulate then clamp:** Build the full number (Python has arbitrary-precision ints), then clamp to `[INT_MIN, INT_MAX]` at the end — Time `O(n)` / Space `O(1)` (the integer can grow up to ~200 digits).
- **Regex / strip-based parsing:** Strip leading whitespace and match `^[+-]?\d+` to extract the numeric prefix, then convert manually and clamp — Time `O(n)` / Space `O(n)`.
