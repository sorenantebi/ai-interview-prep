---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/
neetcode: https://neetcode.io/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree
---
# Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree - Solution

## Intuition

Compute the MST weight once with Kruskal's algorithm. Then test each edge individually: if excluding it makes the MST heavier (or the graph disconnected), it is critical. Otherwise, if forcing it into the tree still yields the optimal weight, it is pseudo-critical. With at most 200 edges and 100 nodes, running Kruskal once per edge is cheap.

## Approach

1. Attach the original index to each edge and sort by weight.
2. Write a Kruskal helper that takes an edge to skip and an edge to force. It unions the forced edge first, then processes the rest in sorted order. It returns the total weight, or infinity if the graph is not connected.
3. Compute `base` with nothing skipped and nothing forced.
4. For each edge `i`:
   - If Kruskal with `i` skipped gives a weight greater than `base`, `i` is critical.
   - Otherwise, if Kruskal with `i` forced gives weight equal to `base`, `i` is pseudo-critical.
5. Return `[critical, pseudo]`.

## Code

```python
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.rank = [1] * n

    def find(self, v1):
        while v1 != self.par[v1]:
            self.par[v1] = self.par[self.par[v1]]
            v1 = self.par[v1]
        return v1

    def union(self, v1, v2):
        p1, p2 = self.find(v1), self.find(v2)
        if p1 == p2:
            return False
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
            self.rank[p1] += self.rank[p2]
        else:
            self.par[p1] = p2
            self.rank[p2] += self.rank[p1]
        return True

class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # Time: O(E^2) - UF operations are assumed to be approx O(1)
        for i, e in enumerate(edges):
            e.append(i) # [v1, v2, weight, original_index]

        edges.sort(key=lambda e: e[2])

        mst_weight = 0
        uf = UnionFind(n)
        for v1, v2, w, i in edges:
            if uf.union(v1, v2):
                mst_weight += w

        critical, pseudo = [], []
        for n1, n2, e_weight, i in edges:
            # Try without curr edge
            weight = 0
            uf = UnionFind(n)
            for v1, v2, w, j in edges:
                if i != j and uf.union(v1, v2):
                    weight += w
            if max(uf.rank) != n or weight > mst_weight:
                critical.append(i)
                continue
            
            # Try with curr edge
            uf = UnionFind(n)
            uf.union(n1, n2)
            weight = e_weight
            for v1, v2, w, j in edges:
                if uf.union(v1, v2):
                    weight += w
            if weight == mst_weight:
                pseudo.append(i)
        return [critical, pseudo]
```

## Complexity

- **Time:** `O(E² · α(N))` — Kruskal runs `O(E)` times after a single `O(E log E)` sort, each pass is `O(E · α(N))`.
- **Space:** `O(E + N)` — sorted edge list plus the union-find array.

## Other Approaches

- **Kruskal with weight-group bridge finding:** process edges in groups of equal weight, build a graph on the component representatives, and find bridges (critical) versus non-bridge edges (pseudo-critical) with Tarjan's algorithm — Time `O(E log E)` / Space `O(E + N)`
