---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/redundant-connection/
neetcode: https://neetcode.io/problems/redundant-connection
---
# Redundant Connection - Solution

**Question:** Redundant Connection - Question · **Difficulty:** Medium

## Intuition

Add edges one by one with **Union-Find**. The first edge whose endpoints are already connected closes the (only) cycle. Since the graph has exactly one cycle and every cycle edge is processed before or at that moment, the edge that closes it is the last cycle edge in the input — exactly the edge the problem asks for.

## Approach

1. Initialize Union-Find over nodes `1..n`.
2. For each edge `[a, b]` in order: if `find(a) == find(b)`, return `[a, b]`.
3. Otherwise union the two sets.

## Code

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        par = [i for i in range(len(edges) + 1)]
        rank = [1] * (len(edges) + 1)

        def find(n):
            p = par[n]
            while p != par[p]:
                par[p] = par[par[p]]
                p = par[p]
            return p

        # return False if already unioned
        def union(n1, n2):
            p1, p2 = find(n1), find(n2)

            if p1 == p2:
                return False
            if rank[p1] > rank[p2]:
                par[p2] = p1
                rank[p1] += rank[p2]
            else:
                par[p1] = p2
                rank[p2] += rank[p1]
            return True

        for n1, n2 in edges:
            if not union(n1, n2):
                return [n1, n2]
```

## Complexity

- **Time:** `O(n * α(n))` — one find/union per edge.
- **Space:** `O(n)` — parent and rank arrays.

## Other Approaches

- **DFS per edge:** before adding each edge, DFS to check whether `a` can already reach `b` — Time `O(n^2)`, Space `O(n)`.
- **Find the cycle, then pick the last cycle edge:** DFS to extract cycle nodes, then scan edges backwards for the last one on the cycle — Time `O(n)`, Space `O(n)`.

## Key Takeaway

In an incrementally built undirected graph, "this edge connects two already-connected nodes" is the Union-Find signature of a cycle.
