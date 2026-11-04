---
video: https://www.youtube.com/watch?v=MsYZSinhuFo
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/sort-an-array/
neetcode: https://neetcode.io/problems/sort-an-array
---
# Sort an Array

**Topic:** Arrays & Hashing · **Difficulty:** Medium

## Problem

Given an array of integers `nums`, sort it in ascending order and return it.

You must solve the problem without using any built-in sorting functions, in `O(n log n)` time, and with the smallest space complexity possible.

## Examples

**Example 1**
```text
Input: nums = [5,2,3,1]
Output: [1,2,3,5]
```
Explanation: After sorting, some numbers keep their positions (for example, 2 and 3), while others move (for example, 1 and 5).

**Example 2**
```text
Input: nums = [5,1,1,2,0,0]
Output: [0,0,1,1,2,5]
```
Explanation: The values in `nums` are not necessarily unique.

## Constraints

- `1 <= nums.length <= 5 * 10^4`
- `-5 * 10^4 <= nums[i] <= 5 * 10^4`
