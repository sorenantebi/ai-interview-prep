---
video: https://www.youtube.com/watch?v=8g78yfzMlao
topic: "Arrays & Hashing"
difficulty: Hard
leetcode: https://leetcode.com/problems/first-missing-positive/
neetcode: https://neetcode.io/problems/first-missing-positive
---
# First Missing Positive

**Topic:** Arrays & Hashing · **Difficulty:** Hard

## Problem

Given an unsorted integer array `nums`, return the smallest positive integer that does not appear in `nums`.

Your algorithm must run in `O(n)` time and use `O(1)` auxiliary space.

## Examples

**Example 1**
```text
Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.
```

**Example 2**
```text
Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.
```

**Example 3**
```text
Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`
