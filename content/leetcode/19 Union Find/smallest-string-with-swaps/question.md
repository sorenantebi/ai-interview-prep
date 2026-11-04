---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/smallest-string-with-swaps/
---
# Smallest String With Swaps

**Topic:** Union Find · **Difficulty:** Medium

## Problem

You are given a string `s` and an array `pairs` of index pairs, where `pairs[i] = [a, b]` denotes two (0-indexed) positions in the string.

You may swap the characters at the two indices of any pair in `pairs`, any number of times and in any order.

Return the lexicographically smallest string that `s` can be turned into after performing these swaps.

## Examples

**Example 1**
```text
Input: s = "dcab", pairs = [[0,3],[1,2]]
Output: "bacd"
```
Swap s[0] and s[3], giving "bcad". Then swap s[1] and s[2], giving "bacd".

**Example 2**
```text
Input: s = "dcab", pairs = [[0,3],[1,2],[0,2]]
Output: "abcd"
```
Swap s[0] and s[3], giving "bcad". Swap s[0] and s[2], giving "acbd". Swap s[1] and s[2], giving "abcd".

**Example 3**
```text
Input: s = "cba", pairs = [[0,1],[1,2]]
Output: "abc"
```
Swap s[0] and s[1], giving "bca". Swap s[1] and s[2], giving "bac". Swap s[0] and s[1], giving "abc".

## Constraints

- `1 <= s.length <= 10^5`
- `0 <= pairs.length <= 10^5`
- `0 <= pairs[i][0], pairs[i][1] < s.length`
- `s` only contains lower case English letters.
