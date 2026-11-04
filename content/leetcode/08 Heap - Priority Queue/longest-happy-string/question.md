---
video: https://www.youtube.com/watch?v=8u-H6O_XQKE
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-happy-string/
neetcode: https://neetcode.io/problems/longest-happy-string
---
# Longest Happy String

**Topic:** Heap - Priority Queue · **Difficulty:** Medium

## Problem

A string is called *happy* if all of the following hold:

- It contains only the letters `'a'`, `'b'`, and `'c'`.
- It does not contain `"aaa"`, `"bbb"`, or `"ccc"` as a substring.
- It contains at most `a` occurrences of `'a'`.
- It contains at most `b` occurrences of `'b'`.
- It contains at most `c` occurrences of `'c'`.

Given three integers `a`, `b`, and `c`, return the longest possible happy string. If there are multiple longest happy strings, return any of them. If no happy string exists, return the empty string `""`.

A substring is a contiguous sequence of characters within a string.

## Examples

**Example 1**
```text
Input: a = 1, b = 1, c = 7
Output: "ccaccbcc"
Explanation: "ccbccacc" would also be a correct answer.
```

**Example 2**
```text
Input: a = 7, b = 1, c = 0
Output: "aabaa"
Explanation: It is the only correct answer in this case.
```

## Constraints

- `0 <= a, b, c <= 100`
- `a + b + c > 0`
