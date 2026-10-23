---
topic: "Linked List"
difficulty: Medium
leetcode: https://leetcode.com/problems/find-the-duplicate-number/
neetcode: https://neetcode.io/problems/find-duplicate-integer
---
# Find The Duplicate Number

**Topic:** Linked List · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/find-the-duplicate-number/) · [NeetCode](https://neetcode.io/problems/find-duplicate-integer)

## Problem

You are given an array `nums` of `n + 1` integers where every value lies in the range `[1, n]`. By the pigeonhole principle at least one value repeats; it is guaranteed that exactly **one** value is repeated (though it may appear more than twice). Return that repeated value. You must not modify `nums` and should use only constant extra space.

## Examples

**Example 1**
```text
Input: nums = [1,3,4,2,2]
Output: 2
```

**Example 2**
```text
Input: nums = [3,1,3,4,2]
Output: 3
```

**Example 3**
```text
Input: nums = [3,3,3,3,3]
Output: 3
```

## Constraints

- `1 <= n <= 10^5`
- `nums.length == n + 1`
- `1 <= nums[i] <= n`
- Exactly one integer appears two or more times
- Follow-up: do not modify `nums`, use `O(1)` extra space, and run in less than `O(n^2)` time
