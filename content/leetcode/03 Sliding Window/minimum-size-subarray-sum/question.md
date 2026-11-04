---
video: https://www.youtube.com/watch?v=aYqYMIqZx5s
topic: "Sliding Window"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-size-subarray-sum/
neetcode: https://neetcode.io/problems/minimum-size-subarray-sum
---
# Minimum Size Subarray Sum

**Topic:** Sliding Window · **Difficulty:** Medium

## Problem

You are given an array `nums` of positive integers and a positive integer `target`. Return the smallest length of a contiguous subarray whose sum is greater than or equal to `target`. If no such subarray exists, return `0`.

## Examples

**Example 1**
```text
Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
```
The subarray `[4,3]` has the minimal length under the problem constraint.

**Example 2**
```text
Input: target = 4, nums = [1,4,4]
Output: 1
```

**Example 3**
```text
Input: target = 11, nums = [1,1,1,1,1,1,1,1]
Output: 0
```

## Constraints

- `1 <= target <= 10^9`
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^4`

**Follow up:** If you have figured out the `O(n)` solution, try coding another solution with `O(n log n)` time complexity.
