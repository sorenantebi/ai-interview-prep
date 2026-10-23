---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-in-rotated-sorted-array/
neetcode: https://neetcode.io/problems/find-target-in-rotated-sorted-array
---
# Search In Rotated Sorted Array

**Topic:** Binary Search · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array/) · [NeetCode](https://neetcode.io/problems/find-target-in-rotated-sorted-array)

## Problem

An integer array `nums`, sorted in ascending order with **distinct** values, may have been rotated at an unknown pivot index `k` (`0 <= k < n`), turning it into `[nums[k], ..., nums[n-1], nums[0], ..., nums[k-1]]`. For example `[0,1,2,4,5,6,7]` rotated at index 3 becomes `[4,5,6,7,0,1,2]`.

Given the rotated array `nums` and an integer `target`, return the index of `target` in `nums`, or `-1` if it is absent. The algorithm must run in `O(log n)` time.

## Examples

**Example 1**
```text
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

**Example 2**
```text
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

**Example 3**
```text
Input: nums = [1], target = 0
Output: -1
```

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i], target <= 10^4`
- All values in `nums` are unique
- `nums` is an ascending array that is possibly rotated
