---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/target-sum/
neetcode: https://neetcode.io/problems/target-sum
---
# Target Sum

**Topic:** 2-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/target-sum/) · [NeetCode](https://neetcode.io/problems/target-sum)

## Problem

You are given an integer array `nums` and an integer `target`. Build an expression by placing either `+` or `-` in front of **every** element of `nums` (in order) and summing them. Return the number of different sign assignments whose expression evaluates to `target`.

## Examples

**Example 1**
```text
Input: nums = [1,1,1,1,1], target = 3
Output: 5
Explanation: Exactly one of the five 1s gets a minus sign, in 5 possible positions.
```

**Example 2**
```text
Input: nums = [1], target = 1
Output: 1
```

**Example 3**
```text
Input: nums = [0,0], target = 0
Output: 4
Explanation: +0+0, +0-0, -0+0, -0-0 all count separately.
```

## Constraints

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 1000`
- `0 <= sum(nums) <= 1000`
- `-1000 <= target <= 1000`
