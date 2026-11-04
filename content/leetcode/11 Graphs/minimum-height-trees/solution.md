---
topic: "Graphs"
difficulty: Medium
leetcode: https://leetcode.com/problems/minimum-height-trees/
neetcode: https://neetcode.io/problems/minimum-height-trees
---
# Minimum Height Trees - Solution

## Intuition

The roots of minimum height trees are the centers of the tree, the middle node(s) of its longest path. A tree has either one or two centers. Repeatedly removing all current leaves shrinks the tree toward its center, and the last one or two nodes remaining are the answer.

## Approach

1. If `n <= 2`, every node is a valid root, so return all of them.
2. Build adjacency sets and collect all leaves (nodes of degree 1).
3. While more than 2 nodes remain, remove the current layer of leaves: subtract the layer size from the remaining count, and for each leaf delete it from its neighbor's adjacency set. Any neighbor that becomes a leaf joins the next layer.
4. When 2 or fewer nodes remain, the current layer of leaves holds the centers. Return it.

## Code

```python
from typing import List, Optional

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)

        leaves = [i for i in range(n) if len(adj[i]) == 1]
        remaining = n

        while remaining > 2:
            remaining -= len(leaves)
            next_leaves = []
            for leaf in leaves:
                neighbor = adj[leaf].pop()
                adj[neighbor].remove(leaf)
                if len(adj[neighbor]) == 1:
                    next_leaves.append(neighbor)
            leaves = next_leaves

        return leaves
```

## Complexity

- **Time:** `O(n)` — each node and edge is added and removed once.
- **Space:** `O(n)` — adjacency sets and the leaf lists.

## Other Approaches

- **Two BFS for the diameter:** BFS from any node to find the farthest node `u`, BFS from `u` to find the farthest `v`, then take the middle one or two nodes of the `u`–`v` path — Time `O(n)` / Space `O(n)`
- **Brute force BFS from every node:** compute the height for each root and keep the minimum ones — Time `O(n^2)` / Space `O(n)`
