---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/valid-palindrome/
neetcode: https://neetcode.io/problems/is-palindrome
---
# Valid Palindrome

**Topic:** Two Pointers · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/valid-palindrome/) · [NeetCode](https://neetcode.io/problems/is-palindrome)

## Problem

A phrase counts as a palindrome if, after lowercasing all letters and discarding every character that is not a letter or digit, it reads the same forwards and backwards. Given a string `s`, return `true` if it is a palindrome under this definition and `false` otherwise. An empty string (after filtering) is a palindrome.

## Examples

**Example 1**
```text
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: filtered string is "amanaplanacanalpanama"
```

**Example 2**
```text
Input: s = "race a car"
Output: false
```

**Example 3**
```text
Input: s = " "
Output: true
Explanation: nothing remains after filtering, and "" is a palindrome
```

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters
