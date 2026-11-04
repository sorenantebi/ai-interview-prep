---
topic: "Union Find"
difficulty: Hard
leetcode: https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/
---
# Remove Max Number of Edges to Keep Graph Fully Traversable - Solution

## Intuition

Full traversal for a person means their usable edges connect all `n` nodes, so the minimum they need is a spanning tree with `n - 1` edges. Type 3 edges serve both people at once, so they are always preferable to a type 1 or type 2 edge. Process type 3 edges first, then fill the gaps separately for Alice and Bob. Every edge that does not merge two components is redundant and can be removed.

## Approach

1. Keep two union-find structures, one for Alice and one for Bob.
2. Go through all type 3 edges first. If the edge merges components in either structure, union it in both and keep it; otherwise count it as removable.
3. Go through type 1 edges using Alice's structure only, and type 2 edges using Bob's only. An edge that does not merge two components is removable.
4. Track the number of components for each person. If either is not exactly 1 at the end, return `-1`.
5. Otherwise return the count of removable edges.

## Code

```python
from typing import List

class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        class DSU:
            def __init__(self, size: int):
                self.parent = list(range(size + 1))
                self.rank = [0] * (size + 1)
                self.components = size

            def find(self, x: int) -> int:
                while self.parent[x] != x:
                    self.parent[x] = self.parent[self.parent[x]]
                    x = self.parent[x]
                return x

            def union(self, a: int, b: int) -> bool:
                ra, rb = self.find(a), self.find(b)
                if ra == rb:
                    return False
                if self.rank[ra] < self.rank[rb]:
                    ra, rb = rb, ra
                self.parent[rb] = ra
                if self.rank[ra] == self.rank[rb]:
                    self.rank[ra] += 1
                self.components -= 1
                return True

        alice, bob = DSU(n), DSU(n)
        removed = 0

        for t, u, v in edges:
            if t == 3:
                # both unions must run, so don't short-circuit with `or`
                a = alice.union(u, v)
                b = bob.union(u, v)
                if not (a or b):
                    removed += 1

        for t, u, v in edges:
            if t == 1:
                if not alice.union(u, v):
                    removed += 1
            elif t == 2:
                if not bob.union(u, v):
                    removed += 1

        if alice.components != 1 or bob.components != 1:
            return -1
        return removed
```

## Complexity

- **Time:** `O(E · α(n))` — each edge is processed a constant number of times with near-constant union-find operations.
- **Space:** `O(n)` — two union-find arrays of size `n + 1`.

## Other Approaches

- **Single DSU pass with sorting by type:** same idea, sort edges by type descending first — Time `O(E log E)` / Space `O(n)`
- **DFS/BFS spanning forests:** build a spanning forest from type 3 edges via traversal, then extend per person — Time `O(n + E)` / Space `O(n + E)`
