---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
neetcode: https://neetcode.io/problems/combinations-of-a-phone-number
---
# Letter Combinations of a Phone Number

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) · [NeetCode](https://neetcode.io/problems/combinations-of-a-phone-number)

## Problem

On a classic phone keypad each digit from `2` to `9` maps to a group of letters:

```text
2: abc   3: def   4: ghi   5: jkl
6: mno   7: pqrs  8: tuv   9: wxyz
```

Given a string `digits` containing only characters `'2'`–`'9'`, return every letter string the digits could represent (choose one letter per digit, in order). Return the answer in any order. If `digits` is empty, return an empty list.

## Examples

**Example 1**
```text
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**Example 2**
```text
Input: digits = ""
Output: []
```

**Example 3**
```text
Input: digits = "2"
Output: ["a","b","c"]
```

## Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is in `'2'`–`'9'`
