---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/zigzag-conversion/
---
# Zigzag Conversion

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

A string is written in a zigzag pattern across a given number of rows: characters are placed going down the rows one by one, then diagonally back up, then down again, and so on. For example, `"PAYPALISHIRING"` on 3 rows looks like this:

```text
P   A   H   N
A P L S I I G
Y   I   R
```

The result is obtained by reading the rows one after another, from the top row to the bottom row, each from left to right: `"PAHNAPLSIIGYIR"`.

Given a string `s` and an integer `numRows`, return the string produced by writing `s` in this zigzag pattern on `numRows` rows and reading it line by line.

## Examples

**Example 1**
```text
Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
```

**Example 2**
```text
Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
```
Explanation:
```text
P     I    N
A   L S  I G
Y A   H R
P     I
```

**Example 3**
```text
Input: s = "A", numRows = 1
Output: "A"
```

## Constraints

- `1 <= s.length <= 1000`
- `s` consists of English letters (lower-case and upper-case), `','` and `'.'`.
- `1 <= numRows <= 1000`
