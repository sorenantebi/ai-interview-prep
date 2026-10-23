---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/container-with-most-water/
neetcode: https://neetcode.io/problems/max-water-container
---
# Container With Most Water

**Topic:** Two Pointers · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/container-with-most-water/) · [NeetCode](https://neetcode.io/problems/max-water-container)

## Problem

You are given an integer array `height` of length `n`. Picture `n` vertical lines where line `i` goes from `(i, 0)` up to `(i, height[i])`. Choose two lines that, together with the x-axis, form a container; the water it holds is `min(height[i], height[j]) * (j - i)`. Return the maximum amount of water any such container can hold. The container may not be tilted.

## Examples

**Example 1**
```text
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: lines at index 1 (8) and 8 (7): min(8,7) * 7 = 49
```

**Example 2**
```text
Input: height = [1,1]
Output: 1
```

## Constraints

- `2 <= height.length <= 10^5`
- `0 <= height[i] <= 10^4`
