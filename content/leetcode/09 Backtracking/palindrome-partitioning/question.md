---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/palindrome-partitioning/
neetcode: https://neetcode.io/problems/palindrome-partitioning
---
# Palindrome Partitioning

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/palindrome-partitioning/) · [NeetCode](https://neetcode.io/problems/palindrome-partitioning)

## Problem

Given a string `s`, split it into one or more contiguous pieces such that **every piece is a palindrome** (reads the same forwards and backwards). Return all possible ways to do this; each way is a list of the pieces in order. The ways can be returned in any order.

## Examples

**Example 1**
```text
Input: s = "aab"
Output: [["a","a","b"],["aa","b"]]
```

**Example 2**
```text
Input: s = "a"
Output: [["a"]]
```

## Constraints

- `1 <= s.length <= 16`
- `s` consists of lowercase English letters
