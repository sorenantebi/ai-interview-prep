---
video: https://www.youtube.com/watch?v=hUe0cUKV-YY
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/matchsticks-to-square/
neetcode: https://neetcode.io/problems/matchsticks-to-square
---
# Matchsticks to Square

**Topic:** Backtracking · **Difficulty:** Medium

## Problem

You are given an integer array `matchsticks`, where `matchsticks[i]` is the length of the `i`-th matchstick. Use all of the matchsticks to form one square. You may not break any stick, but you may link sticks together end to end, and each matchstick must be used exactly once.

Return `true` if you can form such a square, and `false` otherwise.

## Examples

**Example 1**
```text
Input: matchsticks = [1,1,2,2,2]
Output: true
```
Explanation: You can form a square with side length 2. One side of the square is made of two sticks of length 1.

**Example 2**
```text
Input: matchsticks = [3,3,3,3,4]
Output: false
```
Explanation: You cannot find a way to form a square using all the matchsticks.

## Constraints

- `1 <= matchsticks.length <= 15`
- `1 <= matchsticks[i] <= 10^8`
