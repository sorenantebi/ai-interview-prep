---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-words-in-a-string/
---
# Reverse Words in a String

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

Given a string `s`, reverse the order of its words.

A word is a sequence of non-space characters. Words in `s` are separated by at least one space.

Return a string containing the words in reverse order, joined by a single space. The input may contain leading or trailing spaces, or multiple spaces between words, but the returned string must have exactly one space between words and no leading or trailing spaces.

**Follow-up:** If your language has a mutable string type, can you solve it in place with `O(1)` extra space?

## Examples

**Example 1**
```text
Input: s = "the sky is blue"
Output: "blue is sky the"
```

**Example 2**
```text
Input: s = "  hello world  "
Output: "world hello"
```
Explanation: The reversed string must not contain leading or trailing spaces.

**Example 3**
```text
Input: s = "a good   example"
Output: "example good a"
```
Explanation: Multiple spaces between words are reduced to a single space in the result.

## Constraints

- `1 <= s.length <= 10^4`
- `s` contains English letters (upper-case and lower-case), digits, and spaces `' '`.
- There is at least one word in `s`.
