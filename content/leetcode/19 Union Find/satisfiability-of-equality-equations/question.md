---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/satisfiability-of-equality-equations/
---
# Satisfiability of Equality Equations

**Topic:** Union Find · **Difficulty:** Medium

## Problem

You are given an array of strings `equations` describing relationships between variables. Each string `equations[i]` has length 4 and takes one of two forms: `"xi==yi"` or `"xi!=yi"`. Here, `xi` and `yi` are lowercase letters (not necessarily different) that each represent a one-letter variable name.

Return `true` if it is possible to assign integers to the variable names so that all the given equations are satisfied, or `false` otherwise.

## Examples

**Example 1**
```text
Input: equations = ["a==b","b!=a"]
Output: false
```
Explanation: If we assign a = 1 and b = 1, then the first equation is satisfied, but not the second. There is no way to assign the variables to satisfy both equations.

**Example 2**
```text
Input: equations = ["b==a","a==b"]
Output: true
```
Explanation: We could assign a = 1 and b = 1 to satisfy both equations.

## Constraints

- `1 <= equations.length <= 500`
- `equations[i].length == 4`
- `equations[i][0]` is a lowercase letter.
- `equations[i][1]` is either `'='` or `'!'`.
- `equations[i][2]` is `'='`.
- `equations[i][3]` is a lowercase letter.
