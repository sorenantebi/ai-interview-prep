---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/kth-largest-element-in-an-array/
neetcode: https://neetcode.io/problems/kth-largest-element-in-an-array
---
# Kth Largest Element In An Array

**Topic:** Heap / Priority Queue · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-an-array/) · [NeetCode](https://neetcode.io/problems/kth-largest-element-in-an-array)

## Problem

Given an integer array `nums` and an integer `k`, return the `k`-th largest element of the array, i.e. the element that would sit at position `k` (1-indexed) if the array were sorted in descending order. Duplicates count separately, so this is not the `k`-th largest distinct value.

Try to solve it without fully sorting the array.

## Examples

**Example 1**
```text
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

**Example 2**
```text
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
Explanation: descending order is [6,5,5,4,...], 4th is 4
```

## Constraints

- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
