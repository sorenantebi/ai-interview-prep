---
video: https://www.youtube.com/watch?v=v1HpZUnQ4Yo
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/jump-game-vii/
neetcode: https://neetcode.io/problems/jump-game-vii
---
# Jump Game VII

**Topic:** Greedy · **Difficulty:** Medium

## Problem

You are given a 0-indexed binary string `s` and two integers `minJump` and `maxJump`. You start at index `0`, which is guaranteed to be `'0'`.

From index `i` you may jump to index `j` if both of the following hold:

- `i + minJump <= j <= min(i + maxJump, s.length - 1)`
- `s[j] == '0'`

Return `true` if you can reach index `s.length - 1`, otherwise return `false`.

## Examples

**Example 1**
```text
Input: s = "011010", minJump = 2, maxJump = 3
Output: true
```
Explanation: Jump from index 0 to index 3, then from index 3 to index 5.

**Example 2**
```text
Input: s = "01101110", minJump = 2, maxJump = 3
Output: false
```

## Constraints

- `2 <= s.length <= 10^5`
- `s[i]` is either `'0'` or `'1'`
- `s[0] == '0'`
- `1 <= minJump <= maxJump < s.length`
