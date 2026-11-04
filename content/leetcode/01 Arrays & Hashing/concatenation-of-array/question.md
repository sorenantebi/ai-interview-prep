---
video: https://www.youtube.com/watch?v=68isPRHgcFQ
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/concatenation-of-array/
neetcode: https://neetcode.io/problems/concatenation-of-array
---
# Concatenation of Array

**Topic:** Arrays & Hashing · **Difficulty:** Easy

## Problem

You are given an integer array `nums` of length `n`. Build a new array `ans` of length `2n` such that, for every index `i` with `0 <= i < n` (0-indexed), `ans[i] == nums[i]` and `ans[i + n] == nums[i]`.

In other words, `ans` is `nums` followed by another copy of `nums`. Return `ans`.

## Examples

**Example 1**
```text
Input: nums = [1,2,1]
Output: [1,2,1,1,2,1]
```

**Example 2**
```text
Input: nums = [1,3,2,1]
Output: [1,3,2,1,1,3,2,1]
```

## Constraints

- `n == nums.length`
- `1 <= n <= 1000`
- `1 <= nums[i] <= 1000`
