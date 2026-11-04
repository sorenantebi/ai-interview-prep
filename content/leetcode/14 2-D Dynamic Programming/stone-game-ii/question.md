---
video: https://www.youtube.com/watch?v=I-z-u0zfQtg
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/stone-game-ii/
neetcode: https://neetcode.io/problems/stone-game-ii
---
# Stone Game II

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium

## Problem

Alice and Bob play a game with piles of stones arranged in a row. Each pile `piles[i]` contains a positive integer number of stones. The goal is to finish with the most stones.

The players alternate turns, with Alice going first. On a turn, a player takes all the stones from the first `X` remaining piles, where `1 <= X <= 2M`. After the move, `M` is updated to `max(M, X)`. Initially `M = 1`.

The game ends when all the stones have been taken.

Assuming both players play optimally, return the maximum number of stones Alice can get.

## Examples

**Example 1**
```text
Input: piles = [2,7,9,4,4]
Output: 10
```
Explanation: If Alice takes one pile first, Bob takes two piles, and then Alice takes the last two piles, Alice gets 2 + 4 + 4 = 10 stones. If Alice takes two piles first, Bob can take all three remaining piles, leaving Alice with 2 + 7 = 9 stones. So the answer is 10.

**Example 2**
```text
Input: piles = [1,2,3,4,5,100]
Output: 104
```

## Constraints

- `1 <= piles.length <= 100`
- `1 <= piles[i] <= 10^4`
