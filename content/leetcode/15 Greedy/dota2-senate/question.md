---
video: https://www.youtube.com/watch?v=zZA5KskfMuQ
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/dota2-senate/
neetcode: https://neetcode.io/problems/dota2-senate
---
# Dota2 Senate

**Topic:** Greedy · **Difficulty:** Medium

## Problem

The Dota2 senate is made up of senators from two parties: the Radiant (`'R'`) and the Dire (`'D'`). The senate votes on a game change in rounds. In each round, every senator who still has rights acts in the given order and may do one of two things:

- **Ban a senator's right:** Make another senator lose all rights for this and all following rounds.
- **Announce victory:** If all senators who still have rights belong to the same party, announce victory and decide the change.

You are given a string `senate` where `senate[i]` is the party of the i-th senator. The procedure goes from the first senator to the last, skipping any senator who has lost their rights, and then repeats in further rounds until someone announces victory.

Every senator plays optimally for their own party. Return `"Radiant"` or `"Dire"`, depending on which party ends up announcing victory.

## Examples

**Example 1**
```text
Input: senate = "RD"
Output: "Radiant"
```
The first senator (Radiant) bans the second senator in round 1. In round 2, the first senator is the only one with rights and announces victory.

**Example 2**
```text
Input: senate = "RDD"
Output: "Dire"
```
The first senator (Radiant) bans the second senator. The third senator (Dire) bans the first senator. In round 2, the third senator is the only one left and announces victory.

## Constraints

- `n == senate.length`
- `1 <= n <= 10^4`
- `senate[i]` is either `'R'` or `'D'`.
