---
video: https://www.youtube.com/watch?v=Uei1fwDoyKk
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/evaluate-division/
neetcode: https://neetcode.io/problems/evaluate-division
---
# Evaluate Division

**Topic:** Graphs · **Difficulty:** Medium

## Problem

You are given an array of variable pairs `equations` and an array of real numbers `values`, where `equations[i] = [Ai, Bi]` and `values[i]` mean that `Ai / Bi = values[i]`. Each `Ai` and `Bi` is a string representing a single variable.

You are also given a list of `queries`, where `queries[j] = [Cj, Dj]` asks for the value of `Cj / Dj`.

Return the answers to all queries. If an answer cannot be determined, return `-1.0`.

Notes:
- The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction among the equations.
- Variables that do not occur in the equations are undefined, so any query involving them has the answer `-1.0` (even `x / x`).

## Examples

**Example 1**
```text
Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
```
Given `a / b = 2.0` and `b / c = 3.0`, we get `a / c = 6.0`, `b / a = 0.5`. `e` and `x` are undefined, so those queries yield `-1.0`.

**Example 2**
```text
Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
Output: [3.75000,0.40000,5.00000,0.20000]
```

**Example 3**
```text
Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
Output: [0.50000,2.00000,-1.00000,-1.00000]
```

## Constraints

- `1 <= equations.length <= 20`
- `equations[i].length == 2`
- `1 <= Ai.length, Bi.length <= 5`
- `values.length == equations.length`
- `0.0 < values[i] <= 20.0`
- `1 <= queries.length <= 20`
- `queries[i].length == 2`
- `1 <= Cj.length, Dj.length <= 5`
- `Ai`, `Bi`, `Cj`, `Dj` consist of lower case English letters and digits.
