---
video: https://www.youtube.com/watch?v=BHr381Guz3Y
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/rotate-array/
neetcode: https://neetcode.io/problems/rotate-array
---
# Rotate Array

**Topic:** Two Pointers · **Difficulty:** Medium

## Problem

Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative. The rotation must modify `nums` in place; nothing needs to be returned.

As a follow-up, try to find as many solutions as you can (there are at least three), and see whether you can do it in place with `O(1)` extra space.

## Examples

**Example 1**
```text
Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
```
Rotating one step at a time: `[7,1,2,3,4,5,6]`, then `[6,7,1,2,3,4,5]`, then `[5,6,7,1,2,3,4]`.

**Example 2**
```text
Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
```
Rotating one step at a time: `[99,-1,-100,3]`, then `[3,99,-1,-100]`.

## Constraints

- `1 <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `0 <= k <= 10^5`
