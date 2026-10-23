---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/alien-dictionary/
neetcode: https://neetcode.io/problems/foreign-dictionary
---
# Alien Dictionary

**Topic:** Advanced Graphs · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/alien-dictionary/) · [NeetCode](https://neetcode.io/problems/foreign-dictionary)

## Problem

An alien language uses a subset of lowercase English letters, but in an unknown order. You are given a list of `words` that is claimed to be sorted lexicographically according to the alien alphabet.

Return a string containing every unique letter that appears in `words`, arranged in an order consistent with the sorting. If the given ordering is impossible (contradictory), return `""`. If multiple orders are valid, return any of them.

Notes on lexicographic order: the first position where two words differ decides their order; if one word is a prefix of the other, the shorter word must come first (so `["abc", "ab"]` is invalid).

(LeetCode 269 is a premium problem; NeetCode hosts it as "Foreign Dictionary".)

## Examples

**Example 1**
```text
Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"
```

**Example 2**
```text
Input: words = ["z","x"]
Output: "zx"
```

**Example 3**
```text
Input: words = ["z","x","z"]
Output: ""
Explanation: z < x and x < z is a contradiction.
```

## Constraints

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` consists of lowercase English letters only.
