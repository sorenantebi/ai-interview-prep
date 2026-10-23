---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber/
neetcode: https://neetcode.io/problems/house-robber
---
# House Robber

**Topic:** 1-D Dynamic Programming · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/house-robber/) · [NeetCode](https://neetcode.io/problems/house-robber)

## Problem

Houses along a street each hold some amount of money, given by `nums[i]`. You want to take as much money as possible, but you cannot take from two **adjacent** houses (it would trigger an alarm). Return the maximum total you can collect.

## Examples

**Example 1**
```text
Input: nums = [1,2,3,1]
Output: 4
Explanation: Take houses 0 and 2: 1 + 3.
```

**Example 2**
```text
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Take houses 0, 2, 4: 2 + 9 + 1.
```

## Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 400`
