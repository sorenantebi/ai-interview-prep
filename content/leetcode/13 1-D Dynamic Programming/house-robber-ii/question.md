---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber-ii/
neetcode: https://neetcode.io/problems/house-robber-ii
---
# House Robber II

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/house-robber-ii/) · [NeetCode](https://neetcode.io/problems/house-robber-ii)

## Problem

Same as House Robber, except the houses are arranged in a **circle**: the first and last houses are adjacent. Given `nums[i]`, the money in house `i`, return the maximum amount you can take without taking from two adjacent houses.

## Examples

**Example 1**
```text
Input: nums = [2,3,2]
Output: 3
Explanation: Houses 0 and 2 are neighbours, so you can't take both.
```

**Example 2**
```text
Input: nums = [1,2,3,1]
Output: 4
```

**Example 3**
```text
Input: nums = [1,2,3]
Output: 3
```

## Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 1000`
