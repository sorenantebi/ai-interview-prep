---
video: https://www.youtube.com/watch?v=XQlxCCx2vI4
topic: "Advanced Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/path-with-minimum-effort/
neetcode: https://neetcode.io/problems/path-with-minimum-effort
---
# Path With Minimum Effort

**Topic:** Advanced Graphs · **Difficulty:** Medium

## Problem

You are a hiker preparing for an upcoming hike. You are given `heights`, a 2D array of size `rows x columns`, where `heights[row][col]` is the height of cell `(row, col)`. You start in the top-left cell `(0, 0)` and want to reach the bottom-right cell `(rows - 1, columns - 1)` (0-indexed). You may move up, down, left, or right, and you want a route that requires the minimum effort.

The effort of a route is the maximum absolute difference in heights between two consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the bottom-right cell.

## Examples

**Example 1**
```text
Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
```
The route `[1,3,5,3,5]` has a maximum absolute difference of 2 between consecutive cells. This is better than the route `[1,2,2,2,5]`, whose maximum absolute difference is 3.

**Example 2**
```text
Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
```
The route `[1,2,3,4,5]` has a maximum absolute difference of 1 between consecutive cells, which is better than the route `[1,3,5,3,5]`.

**Example 3**
```text
Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
```
This route does not require any effort.

## Constraints

- `rows == heights.length`
- `columns == heights[i].length`
- `1 <= rows, columns <= 100`
- `1 <= heights[i][j] <= 10^6`
