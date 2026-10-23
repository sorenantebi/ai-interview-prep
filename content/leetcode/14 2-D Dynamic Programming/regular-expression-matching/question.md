---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/regular-expression-matching/
neetcode: https://neetcode.io/problems/regular-expression-matching
---
# Regular Expression Matching

**Topic:** 2-D Dynamic Programming · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/regular-expression-matching/) · [NeetCode](https://neetcode.io/problems/regular-expression-matching)

## Problem

Implement regular-expression matching for a string `s` against a pattern `p` that supports two special characters:

- `.` matches any single character.
- `*` matches zero or more copies of the element **immediately before it**.

The match must cover the **entire** input string (not just a part of it). Return `true` if `s` matches `p`.

It is guaranteed that every `*` in `p` is preceded by a valid character (a letter or `.`).

## Examples

**Example 1**
```text
Input: s = "aa", p = "a"
Output: false
Explanation: "a" only matches a single 'a'.
```

**Example 2**
```text
Input: s = "aa", p = "a*"
Output: true
```

**Example 3**
```text
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means zero or more of any character.
```

## Constraints

- `1 <= s.length <= 20`
- `1 <= p.length <= 20`
- `s` contains only lowercase letters; `p` contains lowercase letters, `.`, and `*`.
- Each `*` is preceded by a valid character.
