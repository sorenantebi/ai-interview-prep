---
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-anagram/
neetcode: https://neetcode.io/problems/is-anagram
---
# Valid Anagram

**Topic:** Arrays & Hashing · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/valid-anagram/) · [NeetCode](https://neetcode.io/problems/is-anagram)

## Problem

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, otherwise return `false`. Two strings are anagrams when one can be produced by rearranging the characters of the other, using every character exactly as many times as it appears (so both strings must have identical character counts).

## Examples

**Example 1**
```text
Input: s = "listen", t = "silent"
Output: true
```

**Example 2**
```text
Input: s = "apple", t = "paple"
Output: true
```

**Example 3**
```text
Input: s = "car", t = "cat"
Output: false
```

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` contain only lowercase English letters.
- Follow-up: how would you adapt the solution if inputs could contain arbitrary Unicode characters?
