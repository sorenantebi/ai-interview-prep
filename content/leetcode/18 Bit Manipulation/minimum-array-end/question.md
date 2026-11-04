---
video: https://www.youtube.com/watch?v=4pP-0UpEok4
topic: "Bit Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-array-end/
neetcode: https://neetcode.io/problems/minimum-array-end
---
# Minimum Array End

**Topic:** Bit Manipulation · **Difficulty:** Medium

## Problem

You are given two integers `n` and `x`. Construct an array `nums` of `n` positive integers that is strictly increasing, meaning `nums[i + 1] > nums[i]` for every `0 <= i < n - 1`, and whose bitwise AND over all elements equals `x`.

Return the minimum possible value of `nums[n - 1]`.

## Examples

**Example 1**
```text
Input: n = 3, x = 4
Output: 6
Explanation: nums can be [4,5,6] and its last element is 6.
```

**Example 2**
```text
Input: n = 2, x = 7
Output: 15
Explanation: nums can be [7,15] and its last element is 15.
```

## Constraints

- `1 <= n, x <= 10^8`
