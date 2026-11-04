---
video: https://www.youtube.com/watch?v=oUnF7o88_Xc
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/
neetcode: https://neetcode.io/problems/search-in-rotated-sorted-array-ii
---
# Search in Rotated Sorted Array II

**Topic:** Binary Search · **Difficulty:** Medium

## Problem

An integer array `nums` was originally sorted in non-decreasing order, and its values are not necessarily distinct. Before reaching your function, it was rotated at an unknown pivot index `k` (`0 <= k < nums.length`), so the array became `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,4,4,5,6,6,7]` rotated at pivot index `5` becomes `[4,5,6,6,7,0,1,2,4,4]`.

Given the rotated array `nums` and an integer `target`, return `true` if `target` is in `nums`, and `false` otherwise.

Try to minimize the number of operation steps overall.

Follow-up: this is similar to Search in Rotated Sorted Array, but `nums` may contain duplicates. Does this affect the runtime complexity? How and why?

## Examples

**Example 1**
```text
Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true
```

**Example 2**
```text
Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false
```

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is guaranteed to be rotated at some pivot.
- `-10^4 <= target <= 10^4`
