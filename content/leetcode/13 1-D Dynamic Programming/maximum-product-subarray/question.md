---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/maximum-product-subarray/
neetcode: https://neetcode.io/problems/maximum-product-subarray
---
# Maximum Product Subarray

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/maximum-product-subarray/) · [NeetCode](https://neetcode.io/problems/maximum-product-subarray)

## Problem

Given an integer array `nums`, find the non-empty contiguous subarray whose elements have the largest product, and return that product. The answer is guaranteed to fit in a 32-bit integer.

## Examples

**Example 1**
```text
Input: nums = [2,3,-2,4]
Output: 6
Explanation: The subarray [2,3] has product 6.
```

**Example 2**
```text
Input: nums = [-2,0,-1]
Output: 0
Explanation: [-2,-1] is not contiguous, so the best is 0.
```

## Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-10 <= nums[i] <= 10`
- The product of any subarray fits in a 32-bit integer.
