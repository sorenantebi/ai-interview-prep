---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/generate-parentheses/
neetcode: https://neetcode.io/problems/generate-parentheses
---
# Generate Parentheses

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/generate-parentheses/) · [NeetCode](https://neetcode.io/problems/generate-parentheses)

## Problem

Given an integer `n`, return every string made of exactly `n` opening and `n` closing parentheses that is **well-formed** (every `'('` is matched by a later `')'`, and no prefix has more `')'` than `'('`). The strings may be returned in any order.

## Examples

**Example 1**
```text
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

**Example 2**
```text
Input: n = 1
Output: ["()"]
```

## Constraints

- `1 <= n <= 8`
