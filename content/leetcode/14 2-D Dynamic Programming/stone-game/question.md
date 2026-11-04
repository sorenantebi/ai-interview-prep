---
video: https://www.youtube.com/watch?v=uhgdXOlGYqE
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/stone-game/
neetcode: https://neetcode.io/problems/stone-game
---
# Stone Game

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium

## Problem

Alice and Bob play a game with piles of stones arranged in a row. The number of piles is even, and each pile `piles[i]` contains a positive integer number of stones.

The goal is to finish with the most stones. The total number of stones is odd, so there can be no tie.

Alice and Bob alternate turns, with Alice going first. On each turn, a player takes an entire pile from either the beginning or the end of the row. This continues until no piles remain, and the player holding the most stones wins.

Assuming both players play optimally, return `true` if Alice wins the game, or `false` if Bob wins.

## Examples

**Example 1**
```text
Input: piles = [5,3,4,5]
Output: true
```
Alice can take the first 5, leaving [3, 4, 5]. If Bob takes 3, Alice takes 5 and ends with 10. If Bob takes the last 5, Alice takes 4 and ends with 9. Either way Alice wins.

**Example 2**
```text
Input: piles = [3,7,2,3]
Output: true
```

## Constraints

- `2 <= piles.length <= 500`
- `piles.length` is even.
- `1 <= piles[i] <= 500`
- `sum(piles[i])` is odd.
