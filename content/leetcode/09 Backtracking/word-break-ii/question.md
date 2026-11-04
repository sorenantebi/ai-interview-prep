---
video: https://www.youtube.com/watch?v=QgLKdluDo08
topic: "Backtracking"
difficulty: Hard
leetcode: https://leetcode.com/problems/word-break-ii/
neetcode: https://neetcode.io/problems/word-break-ii
---
# Word Break II

**Topic:** Backtracking · **Difficulty:** Hard

## Problem

Given a string `s` and a dictionary of strings `wordDict`, insert spaces into `s` so that it becomes a sentence in which every word is a valid dictionary word. Return all possible sentences, in any order.

A dictionary word may be reused any number of times in a single segmentation.

## Examples

**Example 1**
```text
Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
Output: ["cats and dog","cat sand dog"]
```

**Example 2**
```text
Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
```
Dictionary words may be reused.

**Example 3**
```text
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: []
```

## Constraints

- `1 <= s.length <= 20`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 10`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are unique.
- The input is generated so that the length of the answer does not exceed `10^5`.
