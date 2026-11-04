---
video: https://www.youtube.com/watch?v=LECWOvTo-Sc
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-strings-alternately/
neetcode: https://neetcode.io/problems/merge-strings-alternately
---
# Merge Strings Alternately

**Topic:** Two Pointers · **Difficulty:** Easy

## Problem

You are given two strings `word1` and `word2`. Build a merged string by taking letters from the two strings in alternating order, starting with `word1`. If one string is longer than the other, append its remaining letters to the end of the merged string.

Return the merged string.

## Examples

**Example 1**
```text
Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
```

**Example 2**
```text
Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
```

**Example 3**
```text
Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
```

## Constraints

- `1 <= word1.length, word2.length <= 100`
- `word1` and `word2` consist of lowercase English letters.
