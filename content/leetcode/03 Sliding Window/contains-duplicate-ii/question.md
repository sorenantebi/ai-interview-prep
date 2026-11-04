---
video: https://www.youtube.com/watch?v=ypn0aZ0nrL4
topic: "Sliding Window"
difficulty: Easy
leetcode: https://leetcode.com/problems/contains-duplicate-ii/
neetcode: https://neetcode.io/problems/contains-duplicate-ii
---
# Contains Duplicate II

**Topic:** Sliding Window · **Difficulty:** Easy

## Problem

You are given an integer array `nums` and an integer `k`. Return `true` if there exist two distinct indices `i` and `j` such that `nums[i] == nums[j]` and `abs(i - j) <= k`. Otherwise, return `false`.

## Examples

**Example 1**
```text
Input: nums = [1,2,3,1], k = 3
Output: true
```

**Example 2**
```text
Input: nums = [1,0,1,1], k = 1
Output: true
```

**Example 3**
```text
Input: nums = [1,2,3,1,2,3], k = 2
Output: false
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `0 <= k <= 10^5`
