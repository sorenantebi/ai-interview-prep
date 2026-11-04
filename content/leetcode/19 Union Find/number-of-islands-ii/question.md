---
topic: "Union Find"
difficulty: Hard
leetcode: https://leetcode.com/problems/number-of-islands-ii/
neetcode: https://neetcode.io/problems/number-of-islands-ii
---
# Number of Islands II

**Topic:** Union Find · **Difficulty:** Hard

## Problem

You are given an `m x n` grid that starts out as all water (represented by `0`). The operation `addLand` turns a single water cell into land (`1`).

You are given an array `positions`, where `positions[i] = [ri, ci]` is the cell to turn into land in the `i`-th operation. After each operation, report the number of islands in the grid.

An island is a group of land cells connected horizontally or vertically (4-directionally). You may assume all four edges of the grid are surrounded by water.

Return an array `answer`, where `answer[i]` is the number of islands after the `i`-th `addLand` operation.

## Examples

**Example 1**
```text
Input: m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]
Output: [1,1,2,3]
```
Explanation: Initially the grid is all water. After `[0,0]` there is 1 island. After `[0,1]` it joins the first island, so there is still 1. After `[1,2]` there are 2 islands. After `[2,1]` there are 3 islands.

**Example 2**
```text
Input: m = 1, n = 1, positions = [[0,0]]
Output: [1]
```

## Constraints

- `1 <= m, n, positions.length <= 10^4`
- `1 <= m * n <= 10^4`
- `positions[i].length == 2`
- `0 <= ri < m`
- `0 <= ci < n`

Follow-up: can you solve it in time complexity `O(k log(mn))`, where `k == positions.length`?
