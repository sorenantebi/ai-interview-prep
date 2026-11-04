---
video: https://www.youtube.com/watch?v=Pzg3bCDY87w
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/open-the-lock/
neetcode: https://neetcode.io/problems/open-the-lock
---
# Open the Lock

**Topic:** Graphs · **Difficulty:** Medium

## Problem

A lock has 4 circular wheels, each with 10 slots labeled `'0'` through `'9'`. Wheels rotate freely and wrap around, so `'9'` can be turned to `'0'` and `'0'` to `'9'`. A move turns one wheel by one slot.

The lock starts at `'0000'`, a string describing the state of the 4 wheels.

You are given a list of `deadends`. If the lock ever displays any of these codes, the wheels stop turning and the lock can no longer be opened.

Given a `target` value that unlocks the lock, return the minimum number of moves required to open it, or `-1` if it is impossible.

## Examples

**Example 1**
```text
Input: deadends = ["0201","0101","0102","1212","2002"], target = "0202"
Output: 6
```
A valid sequence is "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202". The sequence "0000" -> "0001" -> "0002" -> "0102" -> "0202" is invalid because the lock gets stuck at the dead end "0102".

**Example 2**
```text
Input: deadends = ["8888"], target = "0009"
Output: 1
```
Turn the last wheel backwards: "0000" -> "0009".

**Example 3**
```text
Input: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
Output: -1
```
The target cannot be reached without getting stuck.

## Constraints

- `1 <= deadends.length <= 500`
- `deadends[i].length == 4`
- `target.length == 4`
- `target` will not be in the list `deadends`.
- `target` and `deadends[i]` consist of digits only.
