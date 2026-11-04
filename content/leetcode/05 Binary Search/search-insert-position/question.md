---
video: https://www.youtube.com/watch?v=K-RYzDZkzCI
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/search-insert-position/
neetcode: https://neetcode.io/problems/search-insert-position
---
# Search Insert Position

**Topic:** Binary Search · **Difficulty:** Easy

## Problem

You are given a sorted array of distinct integers `nums` (ascending order) and an integer `target`. Return the index of `target` if it is present in the array. Otherwise, return the index at which `target` would have to be inserted to keep the array sorted.

Your algorithm must run in `O(log n)` time.

## Examples

**Example 1**
```text
Input: nums = [1,3,5,6], target = 5
Output: 2
```

**Example 2**
```text
Input: nums = [1,3,5,6], target = 2
Output: 1
```

**Example 3**
```text
Input: nums = [1,3,5,6], target = 7
Output: 4
```

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains distinct values sorted in ascending order.
- `-10^4 <= target <= 10^4`
