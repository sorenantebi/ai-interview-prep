---
video: https://www.youtube.com/watch?v=OVgPAJIyX6o
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/verifying-an-alien-dictionary/
neetcode: https://neetcode.io/problems/verifying-an-alien-dictionary
---
# Verifying an Alien Dictionary

**Topic:** Graphs · **Difficulty:** Easy

## Problem

An alien language uses the English lowercase letters, but possibly in a different alphabetical order. The order of the alphabet is some permutation of the 26 lowercase letters.

You are given a list of words written in this alien language and a string `order` describing the alphabet's order. Return `true` if and only if the words are sorted lexicographically according to that alien order, otherwise return `false`.

When one word is a prefix of another, the shorter word is considered smaller (as if padded with a blank character that is less than every letter).

## Examples

**Example 1**
```text
Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
Output: true
```
Explanation: 'h' comes before 'l' in this language, so the sequence is sorted.

**Example 2**
```text
Input: words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"
Output: false
```
Explanation: 'd' comes after 'l' in this language, so words[0] > words[1], hence the sequence is unsorted.

**Example 3**
```text
Input: words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"
Output: false
```
Explanation: The first three characters match, and the second word is shorter. "apple" > "app" because 'l' > the blank character, which is less than any other character.

## Constraints

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 20`
- `order.length == 26`
- All characters in `words[i]` and `order` are English lowercase letters.
