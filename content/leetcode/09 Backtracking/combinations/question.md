---
video: https://www.youtube.com/watch?v=q0s6m7AiM7o
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/combinations/
neetcode: https://neetcode.io/problems/combinations
---
# Combinations

**Topic:** Backtracking · **Difficulty:** Medium

## Problem

Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen from the range `[1, n]`.

The answer may be returned in any order. Combinations are unordered, so `[1,2]` and `[2,1]` count as the same combination.

## Examples

**Example 1**
```text
Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
```
There are 4 choose 2 = 6 combinations in total.

**Example 2**
```text
Input: n = 1, k = 1
Output: [[1]]
```
There is 1 choose 1 = 1 combination in total.

## Constraints

- `1 <= n <= 20`
- `1 <= k <= n`
