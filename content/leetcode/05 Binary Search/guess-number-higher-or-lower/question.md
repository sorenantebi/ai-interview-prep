---
video: https://www.youtube.com/watch?v=xW4QsTtaCa4
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/guess-number-higher-or-lower/
neetcode: https://neetcode.io/problems/guess-number-higher-or-lower
---
# Guess Number Higher or Lower

**Topic:** Binary Search · **Difficulty:** Easy

## Problem

We are playing a guessing game. A number is picked from `1` to `n`, and you must find it. The picked number stays the same for the whole game.

Each time you guess wrong, you are told whether the picked number is higher or lower than your guess.

You may call a pre-defined API `int guess(int num)`, which returns one of three values:

- `-1`: your guess is higher than the picked number (`num > pick`).
- `1`: your guess is lower than the picked number (`num < pick`).
- `0`: your guess is equal to the picked number (`num == pick`).

Return the number that was picked.

## Examples

**Example 1**
```text
Input: n = 10, pick = 6
Output: 6
```

**Example 2**
```text
Input: n = 1, pick = 1
Output: 1
```

**Example 3**
```text
Input: n = 2, pick = 1
Output: 1
```

## Constraints

- `1 <= n <= 2^31 - 1`
- `1 <= pick <= n`
