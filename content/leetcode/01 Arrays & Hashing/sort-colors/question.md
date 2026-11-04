---
video: https://www.youtube.com/watch?v=4xbWSRZHqac
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/sort-colors/
neetcode: https://neetcode.io/problems/sort-colors
---
# Sort Colors

**Topic:** Arrays & Hashing · **Difficulty:** Medium

## Problem

You are given an array `nums` containing `n` objects colored red, white, or blue. Sort them in-place so that objects of the same color are adjacent, with the colors ordered red, then white, then blue.

The integers `0`, `1`, and `2` represent red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

**Follow up:** Can you come up with a one-pass algorithm using only constant extra space?

## Examples

**Example 1**
```text
Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
```

**Example 2**
```text
Input: nums = [2,0,1]
Output: [0,1,2]
```

## Constraints

- `n == nums.length`
- `1 <= n <= 300`
- `nums[i]` is either `0`, `1`, or `2`.
