---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/count-of-smaller-numbers-after-self/
---
# Count of Smaller Numbers After Self

**Topic:** Segment Tree · **Difficulty:** Hard

## Problem

Given an integer array `nums`, return an integer array `counts` of the same length, where `counts[i]` is the number of elements to the right of `nums[i]` that are strictly smaller than `nums[i]`.

## Examples

**Example 1**
```text
Input: nums = [5,2,6,1]
Output: [2,1,1,0]
```
To the right of 5 there are 2 smaller elements (2 and 1). To the right of 2 there is 1 (1). To the right of 6 there is 1 (1). To the right of 1 there are none.

**Example 2**
```text
Input: nums = [-1]
Output: [0]
```

**Example 3**
```text
Input: nums = [-1,-1]
Output: [0,0]
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
