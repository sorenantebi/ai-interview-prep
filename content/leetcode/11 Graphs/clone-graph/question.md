---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/clone-graph/
neetcode: https://neetcode.io/problems/clone-graph
---
# Clone Graph

**Topic:** Graphs · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/clone-graph/) · [NeetCode](https://neetcode.io/problems/clone-graph)

## Problem

You are given a reference to one node of a connected, undirected graph. Return a **deep copy** (clone) of the whole graph.

Each node has an integer `val` and a list `neighbors` of its adjacent nodes:

```text
class Node:
    val: int
    neighbors: List[Node]
```

For testing, node values are `1..n` and equal to their 1-based index; the graph is described as an adjacency list where entry `i` lists the neighbors of node `i + 1`. The given node is always the node with `val = 1` (or `None` for an empty graph). The returned clone must contain completely new node objects with the same structure — no node of the original graph may appear in the copy.

## Examples

**Example 1**
```text
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation: 4 nodes in a cycle 1-2-3-4-1.
```

**Example 2**
```text
Input: adjList = [[]]
Output: [[]]
Explanation: A single node with no neighbors.
```

**Example 3**
```text
Input: adjList = []
Output: []
Explanation: Empty graph.
```

## Constraints

- Number of nodes is in the range `[0, 100]`
- `1 <= Node.val <= 100`, all values are unique
- No repeated edges and no self-loops
- The graph is connected and all nodes are reachable from the given node
