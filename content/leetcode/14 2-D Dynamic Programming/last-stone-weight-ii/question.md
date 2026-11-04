---
video: https://www.youtube.com/watch?v=gdXkkmzvR3c
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/last-stone-weight-ii/
neetcode: https://neetcode.io/problems/last-stone-weight-ii
---
# Last Stone Weight II

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium

## Problem

You are given an integer array `stones`, where `stones[i]` is the weight of the `i`-th stone.

A game is played with the stones. On each turn, choose any two stones and smash them together. Suppose their weights are `x` and `y` with `x <= y`. The result is:

- If `x == y`, both stones are destroyed.
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` gets the new weight `y - x`.

At the end of the game, at most one stone remains.

Return the smallest possible weight of the remaining stone. If no stones remain, return `0`.

## Examples

**Example 1**
```text
Input: stones = [2,7,4,1,8,1]
Output: 1
```
Explanation: Combine 2 and 4 to get 2, giving `[2,7,1,8,1]`. Combine 7 and 8 to get 1, giving `[2,1,1,1]`. Combine 2 and 1 to get 1, giving `[1,1,1]`. Combine 1 and 1 to get 0, giving `[1]`, which is the optimal value.

**Example 2**
```text
Input: stones = [31,26,33,21,40]
Output: 5
```

## Constraints

- `1 <= stones.length <= 30`
- `1 <= stones[i] <= 100`
