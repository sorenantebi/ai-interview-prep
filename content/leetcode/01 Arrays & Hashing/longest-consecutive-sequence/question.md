---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-consecutive-sequence/
neetcode: https://neetcode.io/problems/longest-consecutive-sequence
---
# Longest Consecutive Sequence

**Topic:** Arrays & Hashing · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/) · [NeetCode](https://neetcode.io/problems/longest-consecutive-sequence)

## Problem

Given an unsorted integer array `nums`, return the length of the longest run of consecutive integers (values `x, x+1, x+2, ...`) whose members all appear in `nums`. The values do not need to be adjacent in the array, and duplicates count only once. Your algorithm should run in `O(n)` time.

## Examples

**Example 1**
```text
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: the run 1,2,3,4 has length 4.
```

**Example 2**
```text
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
```

**Example 3**
```text
Input: nums = [1,0,1,2]
Output: 3
```

## Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
