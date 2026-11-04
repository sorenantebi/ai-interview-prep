---
video: https://www.youtube.com/watch?v=DEJAZBq0FDA
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
neetcode: https://neetcode.io/problems/remove-duplicates-from-sorted-array
---
# Remove Duplicates from Sorted Array

**Topic:** Two Pointers · **Difficulty:** Easy

## Problem

You are given an integer array `nums` sorted in non-decreasing order. Remove the duplicates in-place so that each unique value appears only once, keeping the relative order of the elements.

Let `k` be the number of unique elements in `nums`. Return `k`. The first `k` positions of `nums` must hold the unique values in sorted order. What is stored beyond index `k - 1` does not matter.

The judge checks that the returned `k` equals the expected length and that `nums[0..k-1]` matches the expected unique values.

## Examples

**Example 1**
```text
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
```
The function returns `k = 2`, and the first two elements of `nums` are `1` and `2`. Values beyond index `k - 1` are irrelevant.

**Example 2**
```text
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
```
The function returns `k = 5`, and the first five elements of `nums` are `0`, `1`, `2`, `3` and `4`. Values beyond index `k - 1` are irrelevant.

## Constraints

- `1 <= nums.length <= 3 * 10^4`
- `-100 <= nums[i] <= 100`
- `nums` is sorted in non-decreasing order.
