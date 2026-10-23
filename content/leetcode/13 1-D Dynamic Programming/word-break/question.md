---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/word-break/
neetcode: https://neetcode.io/problems/word-break
---
# Word Break

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/word-break/) · [NeetCode](https://neetcode.io/problems/word-break)

## Problem

Given a string `s` and a list of strings `wordDict`, return `true` if `s` can be split into a sequence of one or more dictionary words (concatenated with no gaps), and `false` otherwise. A dictionary word may be used any number of times.

## Examples

**Example 1**
```text
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
```

**Example 2**
```text
Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: "apple" is reused.
```

**Example 3**
```text
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
```

## Constraints

- `1 <= s.length <= 300`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 20`
- `s` and the words contain only lowercase English letters; all words are unique.
