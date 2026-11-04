---
video: https://www.youtube.com/watch?v=i5I_wrbUdzM
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/greatest-common-divisor-of-strings/
neetcode: https://neetcode.io/problems/greatest-common-divisor-of-strings
---
# Greatest Common Divisor of Strings

**Topic:** Math & Geometry · **Difficulty:** Easy

## Problem

A string `t` *divides* a string `s` if `s` can be built by concatenating `t` with itself one or more times (`s = t + t + ... + t`).

Given two strings `str1` and `str2`, return the longest string `x` that divides both `str1` and `str2`. If no such string exists, return an empty string.

## Examples

**Example 1**
```text
Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"
```

**Example 2**
```text
Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"
```

**Example 3**
```text
Input: str1 = "LEET", str2 = "CODE"
Output: ""
```

**Example 4**
```text
Input: str1 = "AAAAAB", str2 = "AAA"
Output: ""
```

## Constraints

- `1 <= str1.length, str2.length <= 1000`
- `str1` and `str2` consist of English uppercase letters.
