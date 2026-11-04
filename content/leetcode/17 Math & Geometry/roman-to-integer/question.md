---
video: https://www.youtube.com/watch?v=3jdxYj3DD98
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/roman-to-integer/
neetcode: https://neetcode.io/problems/roman-to-integer
---
# Roman to Integer

**Topic:** Math & Geometry · **Difficulty:** Easy

## Problem

Roman numerals use seven symbols: `I` (1), `V` (5), `X` (10), `L` (50), `C` (100), `D` (500) and `M` (1000).

Numerals are normally written from largest to smallest, left to right, and the values are added together. For example, `II` is 2, `XII` is 12 and `XXVII` is 27.

There is one exception: six subtractive combinations are used instead of repeating a symbol four times.

- `I` before `V` or `X` gives 4 and 9.
- `X` before `L` or `C` gives 40 and 90.
- `C` before `D` or `M` gives 400 and 900.

Given a valid Roman numeral `s`, convert it to an integer.

## Examples

**Example 1**
```text
Input: s = "III"
Output: 3
Explanation: III = 3.
```

**Example 2**
```text
Input: s = "LVIII"
Output: 58
Explanation: L = 50, V = 5, III = 3.
```

**Example 3**
```text
Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
```

## Constraints

- `1 <= s.length <= 15`
- `s` contains only the characters `'I'`, `'V'`, `'X'`, `'L'`, `'C'`, `'D'`, `'M'`.
- `s` is guaranteed to be a valid Roman numeral in the range `[1, 3999]`.
