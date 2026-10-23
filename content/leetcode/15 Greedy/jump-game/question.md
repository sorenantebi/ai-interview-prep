---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/jump-game/
neetcode: https://neetcode.io/problems/jump-game
---
# Jump Game

**Topic:** Greedy · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/jump-game/) · [NeetCode](https://neetcode.io/problems/jump-game)

## Problem

You are given an integer array `nums`. You start at index `0`, and `nums[i]` is the **maximum** jump length from index `i` (you may jump any distance from `0` up to `nums[i]`). Return `true` if you can reach the last index, otherwise `false`.

## Examples

**Example 1**
```text
Input: nums = [2,3,1,1,4]
Output: true
Explanation: 0 -> 1 -> 4
```

**Example 2**
```text
Input: nums = [3,2,1,0,4]
Output: false
Explanation: Every path lands on index 3, whose jump length is 0.
```

## Constraints

- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^5`
