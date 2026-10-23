---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/partition-equal-subset-sum/
neetcode: https://neetcode.io/problems/partition-equal-subset-sum
---
# Partition Equal Subset Sum

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/partition-equal-subset-sum/) · [NeetCode](https://neetcode.io/problems/partition-equal-subset-sum)

## Problem

Given an array `nums` of positive integers, return `true` if the array can be split into two subsets (every element in exactly one) whose sums are equal, and `false` otherwise.

## Examples

**Example 1**
```text
Input: nums = [1,5,11,5]
Output: true
Explanation: [1,5,5] and [11] both sum to 11.
```

**Example 2**
```text
Input: nums = [1,2,3,5]
Output: false
```

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`
