---
topic: "Two Pointers"
difficulty: Hard
leetcode: https://leetcode.com/problems/trapping-rain-water/
neetcode: https://neetcode.io/problems/trapping-rain-water
---
# Trapping Rain Water

**Topic:** Two Pointers · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/trapping-rain-water/) · [NeetCode](https://neetcode.io/problems/trapping-rain-water)

## Problem

You are given `n` non-negative integers `height` describing an elevation map where every bar has width `1`. After rain, water collects in the dips between bars. Compute the total units of water trapped. The water above position `i` is `min(max height to its left, max height to its right) - height[i]`, if positive.

## Examples

**Example 1**
```text
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

**Example 2**
```text
Input: height = [4,2,0,3,2,5]
Output: 9
```

## Constraints

- `1 <= height.length <= 2 * 10^4`
- `0 <= height[i] <= 10^5`
