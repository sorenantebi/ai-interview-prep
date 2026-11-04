---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/
---
# Most Stones Removed with Same Row or Column

**Topic:** Union Find · **Difficulty:** Medium

## Problem

`n` stones are placed at integer coordinate points on a 2D plane. No two stones occupy the same point.

A stone can be removed if there is another stone that has not yet been removed in the same row or the same column.

You are given an array `stones` of length `n`, where `stones[i] = [xi, yi]` is the location of the `i`-th stone. Return the largest number of stones that can be removed.

## Examples

**Example 1**
```text
Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
Output: 5
```
One way to remove 5 stones: remove [2,2] (same row as [2,1]), then [2,1] (same column as [0,1]), then [1,2] (same row as [1,0]), then [1,0] (same column as [0,0]), then [0,1] (same row as [0,0]). Stone [0,0] cannot be removed because no other stone remains in its row or column.

**Example 2**
```text
Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
Output: 3
```
Stones [0,0] and [1,1] remain at the end: [1,1] shares no row or column with any other stone, and [0,0] is the last one left of its group.

**Example 3**
```text
Input: stones = [[0,0]]
Output: 0
```
A lone stone cannot be removed.

## Constraints

- `1 <= stones.length <= 1000`
- `0 <= xi, yi <= 10^4`
- No two stones are at the same coordinate point.
