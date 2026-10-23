---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/detect-squares/
neetcode: https://neetcode.io/problems/count-squares
---
# Detect Squares

**Topic:** Math & Geometry · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/detect-squares/) · [NeetCode](https://neetcode.io/problems/count-squares)

## Problem

Design a data structure that accepts a stream of points on the 2D plane and answers queries about squares.

- `add(point)` adds the point `[x, y]` to the structure. Duplicate points are allowed and are counted separately.
- `count(point)` is given a query point `[qx, qy]`. Count the ways to pick **three points already stored** so that, together with the query point, they form an **axis-aligned square with positive area**. Points chosen from the same coordinates but added at different times count as different choices.

Implement the class `DetectSquares`:

- `DetectSquares()` initializes the structure with no points.
- `void add(int[] point)` adds a point.
- `int count(int[] point)` returns the number of such squares for the query point.

## Examples

**Example 1**
```text
Input:
["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
Output:
[null, null, null, null, 1, 0, null, 2]
Explanation:
count([11,10]) -> 1, using [3,10], [11,2], [3,2].
count([14,8]) -> 0, no square possible.
After adding a second [11,2], count([11,10]) -> 2, since either copy of [11,2] can be chosen.
```

## Constraints

- `point.length == 2`
- `0 <= x, y <= 1000`
- At most `3000` calls in total to `add` and `count`.
