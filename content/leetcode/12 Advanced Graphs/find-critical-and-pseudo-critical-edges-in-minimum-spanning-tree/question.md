---
video: https://www.youtube.com/watch?v=83JnUxrLKJU
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/
neetcode: https://neetcode.io/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree
---
# Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

**Topic:** Advanced Graphs · **Difficulty:** Hard

## Problem

You are given a weighted, undirected, connected graph with `n` vertices numbered `0` to `n - 1`, and an array `edges` where `edges[i] = [ai, bi, weighti]` is a bidirectional edge of weight `weighti` between nodes `ai` and `bi`. A minimum spanning tree (MST) is a subset of the edges that connects all vertices, contains no cycles, and has the smallest possible total weight.

Find all the critical and pseudo-critical edges with respect to the MSTs of the graph.

- A **critical** edge is an MST edge whose removal from the graph would increase the MST weight (it appears in every MST).
- A **pseudo-critical** edge is an edge that appears in some MSTs but not in all of them.

Return a list of two lists: the indices of the critical edges, followed by the indices of the pseudo-critical edges. Indices may be returned in any order.

## Examples

**Example 1**
```text
Input: n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
Output: [[0,1],[2,3,4,5]]
```
Edges 0 and 1 appear in every MST, so they are critical. Edges 2, 3, 4 and 5 appear only in some MSTs, so they are pseudo-critical.

**Example 2**
```text
Input: n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]
Output: [[],[0,1,2,3]]
```
All four edges have equal weight, so any three of them form an MST. Every edge is therefore pseudo-critical.

## Constraints

- `2 <= n <= 100`
- `1 <= edges.length <= min(200, n * (n - 1) / 2)`
- `edges[i].length == 3`
- `0 <= ai < bi < n`
- `1 <= weighti <= 1000`
- All pairs `(ai, bi)` are distinct.
