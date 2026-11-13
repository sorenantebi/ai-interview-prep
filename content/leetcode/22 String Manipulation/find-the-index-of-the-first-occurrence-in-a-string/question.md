---
topic: "String Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
---
# Find the Index of the First Occurrence in a String

**Topic:** String Manipulation · **Difficulty:** Easy

## Problem

You are given two strings, `haystack` and `needle`. Return the index of the first position in `haystack` where `needle` appears as a contiguous substring. If `needle` does not occur in `haystack`, return `-1`.

## Examples

**Example 1**
```text
Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6. The first occurrence is at index 0, so we return 0.
```

**Example 2**
```text
Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.
```

## Constraints

- `1 <= haystack.length, needle.length <= 10^4`
- `haystack` and `needle` consist of only lowercase English characters.
