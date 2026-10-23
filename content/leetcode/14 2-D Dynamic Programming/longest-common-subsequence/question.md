---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-common-subsequence/
neetcode: https://neetcode.io/problems/longest-common-subsequence
---
# Longest Common Subsequence

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/longest-common-subsequence/) · [NeetCode](https://neetcode.io/problems/longest-common-subsequence)

## Problem

Given two strings `text1` and `text2`, return the length of their longest common subsequence, or `0` if they share no characters.

A subsequence is obtained from a string by deleting zero or more characters without changing the order of the remaining characters (e.g. `"ace"` is a subsequence of `"abcde"`). A common subsequence is one that is a subsequence of both strings.

## Examples

**Example 1**
```text
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: "ace" is the longest common subsequence.
```

**Example 2**
```text
Input: text1 = "abc", text2 = "abc"
Output: 3
```

**Example 3**
```text
Input: text1 = "abc", text2 = "def"
Output: 0
```

## Constraints

- `1 <= text1.length, text2.length <= 1000`
- Both strings consist only of lowercase English letters.
