---
video: https://www.youtube.com/watch?v=LI7YR-bwNYY
topic: "Backtracking"
difficulty: Easy
leetcode: https://leetcode.com/problems/sum-of-all-subset-xor-totals/
neetcode: https://neetcode.io/problems/sum-of-all-subset-xor-totals
---
# Sum of All Subset XOR Totals

**Topic:** Backtracking · **Difficulty:** Easy

## Problem

The XOR total of an array is the bitwise XOR of all its elements, or `0` if the array is empty. For example, the XOR total of `[2,5,6]` is `2 XOR 5 XOR 6 = 1`.

Given an array `nums`, return the sum of the XOR totals of every subset of `nums`.

Subsets that contain the same elements but are formed from different positions are counted separately. A subset of an array is any array obtained by deleting some (possibly zero) of its elements.

## Examples

**Example 1**
```text
Input: nums = [1,3]
Output: 6
```
The subsets are `[]` (0), `[1]` (1), `[3]` (3) and `[1,3]` (2), and 0 + 1 + 3 + 2 = 6.

**Example 2**
```text
Input: nums = [5,1,6]
Output: 28
```
The eight subsets have XOR totals 0, 5, 1, 6, 4, 3, 7 and 2, which sum to 28.

**Example 3**
```text
Input: nums = [3,4,5,6,7,8]
Output: 480
```

## Constraints

- `1 <= nums.length <= 12`
- `1 <= nums[i] <= 20`
