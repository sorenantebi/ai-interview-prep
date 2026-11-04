---
video: https://www.youtube.com/watch?v=Pcd1ii9P9ZI
topic: "Arrays & Hashing"
difficulty: Easy
leetcode: https://leetcode.com/problems/remove-element/
neetcode: https://neetcode.io/problems/remove-element
---
# Remove Element

**Topic:** Arrays & Hashing · **Difficulty:** Easy

## Problem

Given an integer array `nums` and an integer `val`, remove every occurrence of `val` from `nums` in-place. The relative order of the remaining elements may change. Let `k` be the number of elements in `nums` that are not equal to `val`.

To be accepted, you must:

- Rearrange `nums` so that its first `k` elements are exactly the elements that are not equal to `val`. The contents of the remaining positions, and the size of the array, do not matter.
- Return `k`.

The judge checks your answer by confirming that `k` equals the expected length, then sorting the first `k` elements of `nums` and comparing them against the expected sorted array containing no occurrences of `val`.

## Examples

**Example 1**
```text
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
```
The function returns `k = 2`, with the first two elements of `nums` being `2`. Anything beyond index `k` is irrelevant.

**Example 2**
```text
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
```
The function returns `k = 5`, with the first five elements containing `0, 0, 1, 3, 4` in any order. Anything beyond index `k` is irrelevant.

## Constraints

- `0 <= nums.length <= 100`
- `0 <= nums[i] <= 50`
- `0 <= val <= 100`
