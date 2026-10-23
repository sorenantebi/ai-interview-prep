---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/word-search/
neetcode: https://neetcode.io/problems/search-for-word
---
# Word Search

**Topic:** Backtracking · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/word-search/) · [NeetCode](https://neetcode.io/problems/search-for-word)

## Problem

Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` can be traced in the grid, otherwise `false`.

The word is traced by starting at any cell and moving to horizontally or vertically adjacent cells, one letter at a time. A single cell may not be used more than once within the same path.

## Examples

**Example 1**
```text
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
```

**Example 2**
```text
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true
```

**Example 3**
```text
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false
Explanation: the 'B' cell would have to be reused
```

## Constraints

- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` and `word` contain only English letters (upper and lower case)
- Follow-up: can search pruning make it faster on larger boards?
