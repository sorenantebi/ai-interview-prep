---
video: https://www.youtube.com/watch?v=HsLG5QW9CFQ
topic: "1-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/stone-game-iii/
neetcode: https://neetcode.io/problems/stone-game-iii
---
# Stone Game III

**Topic:** 1-D Dynamic Programming · **Difficulty:** Hard

## Problem

Alice and Bob play a game with stones arranged in a row. Each stone has an integer value given by the array `stoneValue`.

They alternate turns, with Alice going first. On a turn, the current player takes 1, 2, or 3 stones from the front of the remaining row. A player's score is the sum of the values of the stones they have taken, starting from 0.

The game ends when all stones have been taken. The player with the higher score wins; equal scores result in a tie. Both players play optimally.

Return `"Alice"` if Alice wins, `"Bob"` if Bob wins, or `"Tie"` if they finish with the same score.

## Examples

**Example 1**
```text
Input: stoneValue = [1,2,3,7]
Output: "Bob"
```
Alice always loses. Her best move is to take three stones for a score of 6, after which Bob takes 7 and wins.

**Example 2**
```text
Input: stoneValue = [1,2,3,-9]
Output: "Alice"
```
Alice must take all three stones on her first move so that Bob is forced to take -9 and ends with a negative score.

**Example 3**
```text
Input: stoneValue = [1,2,3,6]
Output: "Tie"
```
Alice cannot win. She can force a draw by taking the first three stones; any other move makes her lose.

## Constraints

- `1 <= stoneValue.length <= 5 * 10^4`
- `-1000 <= stoneValue[i] <= 1000`
