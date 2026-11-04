---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/rectangle-area-ii/
---
# Rectangle Area II

**Topic:** Line Sweep · **Difficulty:** Hard

## Problem

You are given a list of axis-aligned rectangles. Each `rectangles[i] = [xi1, yi1, xi2, yi2]` describes one rectangle, where `(xi1, yi1)` is its bottom-left corner and `(xi2, yi2)` is its top-right corner.

Compute the total area of the plane covered by the union of all the rectangles. Any region covered by two or more rectangles must be counted only once.

Because the answer can be very large, return it modulo `10^9 + 7`.

## Examples

**Example 1**
```text
Input: rectangles = [[0,0,2,2],[1,0,2,3],[1,0,3,1]]
Output: 6
```
Explanation: A total area of 6 is covered by all three rectangles. The first and second rectangles overlap from (1,1) to (2,2), and all three overlap from (1,0) to (2,1).

**Example 2**
```text
Input: rectangles = [[0,0,1000000000,1000000000]]
Output: 49
```
Explanation: The area is 10^18, and 10^18 modulo (10^9 + 7) is 49.

## Constraints

- `1 <= rectangles.length <= 200`
- `rectangles[i].length == 4`
- `0 <= xi1, yi1, xi2, yi2 <= 10^9`
- `xi1 <= xi2`
- `yi1 <= yi2`
- All rectangles have non-zero area.
