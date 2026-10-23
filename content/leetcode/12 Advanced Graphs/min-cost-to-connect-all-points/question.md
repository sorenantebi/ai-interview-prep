---
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/min-cost-to-connect-all-points/
neetcode: https://neetcode.io/problems/min-cost-to-connect-points
---
# Min Cost to Connect All Points

**Topic:** Advanced Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/) · [NeetCode](https://neetcode.io/problems/min-cost-to-connect-points)

## Problem

You are given `points`, an array of distinct integer coordinates on a 2D plane where `points[i] = [x_i, y_i]`. Connecting two points `[x_i, y_i]` and `[x_j, y_j]` costs their Manhattan distance `|x_i - x_j| + |y_i - y_j|`.

Return the minimum total cost needed so that all points are connected, i.e. there is exactly one simple path between any two points (a spanning tree).

## Examples

**Example 1**
```text
Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
```

**Example 2**
```text
Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18
```

**Example 3**
```text
Input: points = [[0,0]]
Output: 0
```

## Constraints

- `1 <= points.length <= 1000`
- `-10^6 <= x_i, y_i <= 10^6`
- All points are distinct.
