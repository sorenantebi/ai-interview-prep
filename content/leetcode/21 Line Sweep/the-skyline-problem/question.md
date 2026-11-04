---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/the-skyline-problem/
---
# The Skyline Problem

**Topic:** Line Sweep · **Difficulty:** Hard

## Problem

A city's skyline is the outer contour of the silhouette formed by all its buildings when viewed from a distance. You are given the locations and heights of all the buildings and must return the skyline they form together.

Each building is described by `buildings[i] = [left_i, right_i, height_i]`, where:

- `left_i` is the x coordinate of the left edge of the i-th building.
- `right_i` is the x coordinate of the right edge of the i-th building.
- `height_i` is the height of the i-th building.

All buildings are perfect rectangles standing on an absolutely flat surface at height 0.

The skyline must be returned as a list of "key points" `[[x1, y1], [x2, y2], ...]` sorted by x-coordinate. Each key point is the left endpoint of a horizontal segment of the skyline, except the last point, which always has y-coordinate `0` and marks where the rightmost building ends. Any ground between the leftmost and rightmost buildings is part of the skyline's contour.

There must be no two consecutive horizontal segments of equal height in the output. For instance, `[..., [2, 3], [4, 5], [7, 5], [11, 5], [12, 7], ...]` is not acceptable; the three segments of height 5 must be merged into one: `[..., [2, 3], [4, 5], [12, 7], ...]`.

## Examples

**Example 1**
```text
Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
```

**Example 2**
```text
Input: buildings = [[0,2,3],[2,5,3]]
Output: [[0,3],[5,0]]
```

## Constraints

- `1 <= buildings.length <= 10^4`
- `0 <= left_i < right_i <= 2^31 - 1`
- `1 <= height_i <= 2^31 - 1`
- `buildings` is sorted by `left_i` in non-decreasing order.
