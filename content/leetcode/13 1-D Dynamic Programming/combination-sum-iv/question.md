---
video: https://www.youtube.com/watch?v=dw2nMCxG0ik
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum-iv/
neetcode: https://neetcode.io/problems/combination-sum-iv
---
# Combination Sum IV

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium

## Problem

You are given an array `nums` of distinct positive integers and an integer `target`. Return the number of sequences of elements from `nums` (each element may be used any number of times) that add up to `target`.

Sequences with the same numbers in a different order count as different combinations. The test cases are generated so that the answer fits in a 32-bit integer.

**Follow up:** What if negative numbers were allowed in the array? How would that change the problem, and what limitation would need to be added to the question to allow them?

## Examples

**Example 1**
```text
Input: nums = [1,2,3], target = 4
Output: 7
```
The possible sequences are (1,1,1,1), (1,1,2), (1,2,1), (1,3), (2,1,1), (2,2), (3,1). Different orderings are counted separately.

**Example 2**
```text
Input: nums = [9], target = 3
Output: 0
```

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 1000`
- All elements of `nums` are unique.
- `1 <= target <= 1000`
