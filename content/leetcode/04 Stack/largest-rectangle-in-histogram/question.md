---
topic: "Stack"
difficulty: Hard
leetcode: https://leetcode.com/problems/largest-rectangle-in-histogram/
neetcode: https://neetcode.io/problems/largest-rectangle-in-histogram
---
# Largest Rectangle In Histogram

**Topic:** Stack · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/largest-rectangle-in-histogram/) · [NeetCode](https://neetcode.io/problems/largest-rectangle-in-histogram)

## Problem

You are given an array `heights` of non-negative integers representing a histogram where every bar has width `1`. Return the area of the largest axis-aligned rectangle that fits entirely inside the histogram.

## Examples

**Example 1**
```text
Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: bars of height 5 and 6 form a 2-wide rectangle of height 5
```

**Example 2**
```text
Input: heights = [2,4]
Output: 4
```

**Example 3**
```text
Input: heights = [2,1,2]
Output: 3
Explanation: height 1 across all three bars
```

## Constraints

- `1 <= heights.length <= 10^5`
- `0 <= heights[i] <= 10^4`
