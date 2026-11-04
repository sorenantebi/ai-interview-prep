---
video: https://www.youtube.com/watch?v=wQGQnyv_9hI
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-height-trees/
neetcode: https://neetcode.io/problems/minimum-height-trees
---
# Minimum Height Trees

**Topic:** Graphs · **Difficulty:** Medium

## Problem

A tree is an undirected graph in which any two vertices are connected by exactly one path. Equivalently, it is a connected graph with no simple cycles.

You are given a tree with `n` nodes labelled `0` to `n - 1`, and an array `edges` of `n - 1` edges, where `edges[i] = [ai, bi]` is an undirected edge between nodes `ai` and `bi`. Any node may be chosen as the root. Rooting the tree at node `x` gives a rooted tree of some height `h`, where the height is the number of edges on the longest downward path from the root to a leaf. Among all possible roots, the rooted trees with the smallest height are called minimum height trees (MHTs).

Return a list of the root labels of all MHTs. The answer may be returned in any order.

## Examples

**Example 1**
```text
Input: n = 4, edges = [[1,0],[1,2],[1,3]]
Output: [1]
```
Rooting at node 1 gives height 1, and it is the only MHT.

**Example 2**
```text
Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
Output: [3,4]
```

## Constraints

- `1 <= n <= 2 * 10^4`
- `edges.length == n - 1`
- `0 <= ai, bi < n`
- `ai != bi`
- All pairs `(ai, bi)` are distinct.
- The given input is guaranteed to be a tree with no repeated edges.
