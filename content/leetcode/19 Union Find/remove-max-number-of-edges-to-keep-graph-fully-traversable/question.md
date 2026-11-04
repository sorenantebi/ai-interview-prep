---
video: https://www.youtube.com/watch?v=booGwg5wYm4
topic: "Union Find"
difficulty: Hard
leetcode: https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/
---
# Remove Max Number of Edges to Keep Graph Fully Traversable

**Topic:** Union Find · **Difficulty:** Hard

## Problem

Alice and Bob share an undirected graph with `n` nodes and three kinds of edges:

- Type 1: only Alice can traverse it.
- Type 2: only Bob can traverse it.
- Type 3: both Alice and Bob can traverse it.

You are given an array `edges`, where `edges[i] = [type_i, u_i, v_i]` is a bidirectional edge of type `type_i` between nodes `u_i` and `v_i`.

Find the maximum number of edges that can be removed so that, afterwards, the graph is still fully traversable by both Alice and Bob. The graph is fully traversable by a person if, starting from any node, they can reach every other node using the edges they are allowed to traverse.

Return the maximum number of edges that can be removed, or `-1` if Alice and Bob cannot both fully traverse the graph even with all edges present.

## Examples

**Example 1**
```text
Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
Output: 2
```
Removing the edges `[1,1,2]` and `[1,1,3]` keeps the graph fully traversable by both. Removing any further edge breaks it, so the answer is 2.

**Example 2**
```text
Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
Output: 0
```
Removing any edge makes the graph not fully traversable.

**Example 3**
```text
Input: n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]
Output: -1
```
Alice cannot reach node 4 from the other nodes, and Bob cannot reach node 1, so the graph can never be fully traversed.

## Constraints

- `1 <= n <= 10^5`
- `1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)`
- `edges[i].length == 3`
- `1 <= type_i <= 3`
- `1 <= u_i < v_i <= n`
- All tuples `(type_i, u_i, v_i)` are distinct.
