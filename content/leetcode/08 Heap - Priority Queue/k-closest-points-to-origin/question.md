---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/k-closest-points-to-origin/
neetcode: https://neetcode.io/problems/k-closest-points-to-origin
---
# K Closest Points to Origin

**Topic:** Heap / Priority Queue · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/) · [NeetCode](https://neetcode.io/problems/k-closest-points-to-origin)

## Problem

Given a list of points on a 2D plane, `points[i] = [xi, yi]`, and an integer `k`, return the `k` points that are nearest to the origin `(0, 0)` using Euclidean distance `sqrt(x^2 + y^2)`.

The answer may be returned in any order. It is guaranteed to be unique apart from ordering (no ties at the boundary).

## Examples

**Example 1**
```text
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation: squared distances are 10 and 8, so [-2,2] is closer
```

**Example 2**
```text
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: [[-2,4],[3,3]] is also accepted
```

## Constraints

- `1 <= k <= points.length <= 10^4`
- `-10^4 <= xi, yi <= 10^4`
