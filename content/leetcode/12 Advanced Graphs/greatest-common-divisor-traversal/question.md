---
video: https://www.youtube.com/watch?v=jZ-RVp5CVYY
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/greatest-common-divisor-traversal/
neetcode: https://neetcode.io/problems/greatest-common-divisor-traversal
---
# Greatest Common Divisor Traversal

**Topic:** Advanced Graphs · **Difficulty:** Hard

## Problem

You are given a 0-indexed integer array `nums`. You may move between indices of the array: you can go from index `i` to index `j` (with `i != j`) if and only if `gcd(nums[i], nums[j]) > 1`, where `gcd` is the greatest common divisor.

Determine whether, for every pair of indices `i < j`, there is a sequence of traversals that leads from `i` to `j`.

Return `true` if every pair of indices is reachable from one another, or `false` otherwise.

## Examples

**Example 1**
```text
Input: nums = [2,3,6]
Output: true
```
Explanation: Index 0 reaches index 1 via 0 -> 2 -> 1, since gcd(2, 6) = 2 > 1 and gcd(6, 3) = 3 > 1. Indices 0 and 2, and indices 1 and 2, are directly connected.

**Example 2**
```text
Input: nums = [3,9,5]
Output: false
```
Explanation: No sequence of traversals leads from index 0 to index 2.

**Example 3**
```text
Input: nums = [4,3,12,8]
Output: true
```
Explanation: Every one of the 6 index pairs can be connected through some sequence of traversals.

## Constraints

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
