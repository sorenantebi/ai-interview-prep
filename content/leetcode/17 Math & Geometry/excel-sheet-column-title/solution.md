---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/excel-sheet-column-title/
neetcode: https://neetcode.io/problems/excel-sheet-column-title
---
# Excel Sheet Column Title - Solution

## Intuition

This is a base-26 conversion, except there is no zero digit: the digits run from `A` (1) to `Z` (26). Subtracting 1 before each division shifts the digits to the range 0-25, which makes the usual repeated modulo and division work.

## Approach

1. Start with an empty list of characters.
2. While `columnNumber > 0`:
   1. Decrement `columnNumber` by 1 to make it zero-based.
   2. Take `columnNumber % 26` and map it to a letter (`0 -> 'A'`, ..., `25 -> 'Z'`); append it.
   3. Set `columnNumber //= 26`.
3. The letters were produced from least to most significant, so reverse them and join into a string.

## Code

```python
class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        # Time: O(logn) - Log base 26 of n
        res = ""
        while columnNumber > 0:
            remainder = (columnNumber - 1) % 26
            res += chr(ord('A') + remainder)
            columnNumber = (columnNumber - 1) // 26

        return res[::-1] # reverse output
```

## Complexity

- **Time:** `O(log n)` — each iteration divides `columnNumber` by 26, so there are about `log_26(n)` iterations.
- **Space:** `O(log n)` — the output string has about `log_26(n)` characters.

## Other Approaches

- **Recursion:** `convertToTitle(n - 1 divided by 26)` plus the last letter, same idea written recursively — Time `O(log n)` / Space `O(log n)` call stack
- **Prepend to string:** build the result by prepending each letter instead of reversing at the end — Time `O(log² n)` / Space `O(log n)`
