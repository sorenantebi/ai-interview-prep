---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-increasing-subsequence/
neetcode: https://neetcode.io/problems/longest-increasing-subsequence
---
# Longest Increasing Subsequence

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/) · [NeetCode](https://neetcode.io/problems/longest-increasing-subsequence)

## Problem

Given an integer array `nums`, return the length of its longest **strictly increasing subsequence**. A subsequence keeps the original order but may skip elements.

## Examples

**Example 1**
```text
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: One example is [2,3,7,101].
```

**Example 2**
```text
Input: nums = [0,1,0,3,2,3]
Output: 4
```

**Example 3**
```text
Input: nums = [7,7,7,7,7,7,7]
Output: 1
```

## Constraints

- `1 <= nums.length <= 2500`
- `-10^4 <= nums[i] <= 10^4`
