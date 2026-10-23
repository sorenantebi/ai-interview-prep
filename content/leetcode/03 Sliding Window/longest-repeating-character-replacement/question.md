---
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-repeating-character-replacement/
neetcode: https://neetcode.io/problems/longest-repeating-substring-with-replacement
---
# Longest Repeating Character Replacement

**Topic:** Sliding Window · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/longest-repeating-character-replacement/) · [NeetCode](https://neetcode.io/problems/longest-repeating-substring-with-replacement)

## Problem

You are given a string `s` of uppercase English letters and an integer `k`. You may perform at most `k` operations, each replacing one character of `s` with any uppercase letter. Return the length of the longest substring that can be made to consist of a single repeated letter after these operations.

## Examples

**Example 1**
```text
Input: s = "ABAB", k = 2
Output: 4
Explanation: replace both A's (or both B's)
```

**Example 2**
```text
Input: s = "AABABBA", k = 1
Output: 4
Explanation: replace s[3] with 'B' to get "AABBBBA", which contains "BBBB"
```

## Constraints

- `1 <= s.length <= 10^5`
- `s` consists of uppercase English letters
- `0 <= k <= s.length`
