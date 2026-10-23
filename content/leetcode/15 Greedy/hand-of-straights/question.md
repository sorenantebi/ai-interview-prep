---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/hand-of-straights/
neetcode: https://neetcode.io/problems/hand-of-straights
---
# Hand of Straights

**Topic:** Greedy · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/hand-of-straights/) · [NeetCode](https://neetcode.io/problems/hand-of-straights)

## Problem

You hold a hand of cards given as an integer array `hand`, where `hand[i]` is the value on the `i`-th card, and an integer `groupSize`. Decide whether the cards can be rearranged into groups such that every group has exactly `groupSize` cards and consists of `groupSize` **consecutive** values (e.g. `[4,5,6]`). Every card must be used in exactly one group. Return `true` if this is possible, otherwise `false`.

## Examples

**Example 1**
```text
Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
Output: true
Explanation: [1,2,3], [2,3,4], [6,7,8]
```

**Example 2**
```text
Input: hand = [1,2,3,4,5], groupSize = 4
Output: false
Explanation: 5 cards cannot be split into groups of 4.
```

## Constraints

- `1 <= hand.length <= 10^4`
- `0 <= hand[i] <= 10^9`
- `1 <= groupSize <= hand.length`
