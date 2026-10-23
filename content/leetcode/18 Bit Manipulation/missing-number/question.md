---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/missing-number/
neetcode: https://neetcode.io/problems/missing-number
---
# Missing Number

**Topic:** Bit Manipulation · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/missing-number/) · [NeetCode](https://neetcode.io/problems/missing-number)

## Problem

You are given an array `nums` of `n` **distinct** integers taken from the range `[0, n]`. Exactly one number in that range is absent from the array. Return the missing number.

Follow-up: solve it with `O(1)` extra space and `O(n)` time.

## Examples

**Example 1**
```text
Input: nums = [3,0,1]
Output: 2
```

**Example 2**
```text
Input: nums = [0,1]
Output: 2
Explanation: n = 2, so the range is [0, 2]; 2 is missing.
```

**Example 3**
```text
Input: nums = [9,6,4,2,3,5,7,0,1]
Output: 8
```

## Constraints

- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`
- All values in `nums` are unique.
