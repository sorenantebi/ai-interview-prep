---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/edit-distance/
neetcode: https://neetcode.io/problems/edit-distance
---
# Edit Distance

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/edit-distance/) · [NeetCode](https://neetcode.io/problems/edit-distance)

## Problem

Given two strings `word1` and `word2`, return the minimum number of single-character operations needed to transform `word1` into `word2`. The allowed operations are:

- insert a character,
- delete a character,
- replace a character with another.

## Examples

**Example 1**
```text
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: horse -> rorse (replace h) -> rose (delete r) -> ros (delete e)
```

**Example 2**
```text
Input: word1 = "intention", word2 = "execution"
Output: 5
```

**Example 3**
```text
Input: word1 = "", word2 = "abc"
Output: 3
```

## Constraints

- `0 <= word1.length, word2.length <= 500`
- Both strings consist of lowercase English letters.
