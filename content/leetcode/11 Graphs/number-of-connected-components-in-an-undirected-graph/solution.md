---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
neetcode: https://neetcode.io/problems/count-connected-components
---
# Number of Connected Components In An Undirected Graph - Solution

**Question:** Number of Connected Components In An Undirected Graph - Question · **Difficulty:** Medium

## Intuition

Start by assuming every node is its own component (`n` components). Each edge that connects two **different** components merges them, reducing the count by one; edges inside a component change nothing. **Union-Find** tracks exactly this.

## Approach

1. Initialize `parent[i] = i` and `components = n`.
2. For each edge `(a, b)`, find both roots.
3. If the roots differ, union them (by size) and decrement `components`.
4. Return `components`.

## Code

```python
class UnionFind:
    def __init__(self):
        self.f = {}

    def findParent(self, x):
        y = self.f.get(x, x)
        if x != y:
            y = self.f[x] = self.findParent(y)
        return y

    def union(self, x, y):
        self.f[self.findParent(x)] = self.findParent(y)


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        dsu = UnionFind()
        for a, b in edges:
            dsu.union(a, b)
        return len(set(dsu.findParent(x) for x in range(n)))
```

## Complexity

- **Time:** `O(n + E * α(n))` — near-constant amortized union/find.
- **Space:** `O(n)` — parent and size arrays.

## Other Approaches

- **DFS/BFS:** build an adjacency list and count how many traversals are started from unvisited nodes — Time `O(n + E)`, Space `O(n + E)`.

## Key Takeaway

Counting components = `n` minus the number of successful unions; Union-Find handles this (and dynamic edge additions) elegantly.
