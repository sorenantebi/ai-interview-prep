---
video: https://www.youtube.com/watch?v=qB0zZpBJlh8
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/decode-string/
neetcode: https://neetcode.io/problems/decode-string
---
# Decode String

**Topic:** Stack · **Difficulty:** Medium

## Problem

You are given an encoded string `s`. Decode it and return the result.

The encoding rule is `k[encoded_string]`, which means the `encoded_string` inside the square brackets is repeated exactly `k` times. `k` is always a positive integer.

You may assume the input is always valid: there are no extra white spaces and the square brackets are well-formed. The original data contains no digits; digits appear only as repeat counts `k`. For example, inputs like `3a` or `2[4]` will not occur.

The test cases are generated so that the length of the output never exceeds `10^5`.

## Examples

**Example 1**
```text
Input: s = "3[a]2[bc]"
Output: "aaabcbc"
```

**Example 2**
```text
Input: s = "3[a2[c]]"
Output: "accaccacc"
```

**Example 3**
```text
Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

## Constraints

- `1 <= s.length <= 30`
- `s` consists of lowercase English letters, digits, and square brackets `'[]'`.
- `s` is guaranteed to be a valid input.
- All the integers in `s` are in the range `[1, 300]`.
