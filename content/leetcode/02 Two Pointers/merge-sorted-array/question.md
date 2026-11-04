---
video: https://www.youtube.com/watch?v=P1Ic85RarKY
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/merge-sorted-array/
neetcode: https://neetcode.io/problems/merge-sorted-array
---
# Merge Sorted Array

**Topic:** Two Pointers · **Difficulty:** Easy

## Problem

You are given two integer arrays `nums1` and `nums2`, both sorted in non-decreasing order, along with two integers `m` and `n` giving the number of valid elements in `nums1` and `nums2` respectively.

Merge `nums2` into `nums1` so that `nums1` becomes a single array sorted in non-decreasing order. The result must be stored inside `nums1` itself; the function returns nothing.

To make room for the merged result, `nums1` has length `m + n`. Its first `m` elements are the ones to merge, and its last `n` elements are placeholders set to `0` that should be ignored. `nums2` has length `n`.

**Follow up:** Can you do it in `O(m + n)` time?

## Examples

**Example 1**
```text
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
```
The arrays being merged are `[1,2,3]` and `[2,5,6]`.

**Example 2**
```text
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
```
The arrays being merged are `[1]` and `[]`.

**Example 3**
```text
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
```
The arrays being merged are `[]` and `[1]`. The `0` in `nums1` is only a placeholder to make room for the result.

## Constraints

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`
