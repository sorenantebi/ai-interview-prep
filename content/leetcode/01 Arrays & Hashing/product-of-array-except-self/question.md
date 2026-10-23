---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/product-of-array-except-self/
neetcode: https://neetcode.io/problems/products-of-array-discluding-self
---
# Product of Array Except Self

**Topic:** Arrays & Hashing · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/product-of-array-except-self/) · [NeetCode](https://neetcode.io/problems/products-of-array-discluding-self)

## Problem

Given an integer array `nums`, return an array `answer` where `answer[i]` equals the product of every element of `nums` except `nums[i]`. Your algorithm must run in `O(n)` time and must **not** use division. All prefix and suffix products are guaranteed to fit in a 32-bit integer.

## Examples

**Example 1**
```text
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

**Example 2**
```text
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
Explanation: only the position holding 0 gets a non-zero product.
```

**Example 3**
```text
Input: nums = [2,5]
Output: [5,2]
```

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- Prefix/suffix products fit in a 32-bit integer.
- Follow-up: solve it with `O(1)` extra space (the output array does not count).
