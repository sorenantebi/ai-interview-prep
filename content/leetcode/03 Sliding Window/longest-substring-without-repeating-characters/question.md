---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-substring-without-repeating-characters/
neetcode: https://neetcode.io/problems/longest-substring-without-duplicates
---
# Longest Substring Without Repeating Characters

**Topic:** Sliding Window · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · [NeetCode](https://neetcode.io/problems/longest-substring-without-duplicates)

## Problem

Given a string `s`, return the length of the longest **substring** (contiguous) in which no character appears more than once.

## Examples

**Example 1**
```text
Input: s = "abcabcbb"
Output: 3
Explanation: "abc"
```

**Example 2**
```text
Input: s = "bbbbb"
Output: 1
```

**Example 3**
```text
Input: s = "pwwkew"
Output: 3
Explanation: "wke"; "pwke" is a subsequence, not a substring
```

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` may contain letters, digits, symbols and spaces
