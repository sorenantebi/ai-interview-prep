---
topic: "Advanced Graphs"
difficulty: Hard
leetcode: https://leetcode.com/problems/build-a-matrix-with-conditions/
neetcode: https://neetcode.io/problems/build-a-matrix-with-conditions
---
# Build a Matrix With Conditions - Solution

## Intuition

Row and column constraints are independent. Each set of conditions is a set of "must come before" edges between numbers, so a topological sort gives a valid ordering. The position of a number in the row ordering is its row, and its position in the column ordering is its column. If either graph has a cycle, no answer exists.

## Approach

1. Build a directed graph from `rowConditions` and topologically sort it (Kahn's algorithm). If fewer than `k` nodes are produced, there is a cycle, so return `[]`.
2. Do the same for `colConditions`.
3. Record each number's index in the row order and in the column order.
4. Create a `k x k` zero matrix and place each number `v` at `[rowPos[v]][colPos[v]]`.

## Code

```python
from typing import List, Optional
from collections import deque

class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topo_sort(edges: List[List[int]]) -> List[int]:
            adj = [[] for _ in range(k + 1)]
            indeg = [0] * (k + 1)
            for u, v in edges:
                adj[u].append(v)
                indeg[v] += 1
            queue = deque(i for i in range(1, k + 1) if indeg[i] == 0)
            order = []
            while queue:
                node = queue.popleft()
                order.append(node)
                for nxt in adj[node]:
                    indeg[nxt] -= 1
                    if indeg[nxt] == 0:
                        queue.append(nxt)
            # shorter than k means a cycle blocked some nodes
            return order if len(order) == k else []

        row_order = topo_sort(rowConditions)
        col_order = topo_sort(colConditions)
        if not row_order or not col_order:
            return []

        col_pos = {v: i for i, v in enumerate(col_order)}
        res = [[0] * k for _ in range(k)]
        for r, v in enumerate(row_order):
            res[r][col_pos[v]] = v
        return res
```

## Complexity

- **Time:** `O(k^2 + n + m)` — two topological sorts cost `O(k + n + m)`, and allocating the `k x k` matrix costs `O(k^2)`.
- **Space:** `O(k^2 + n + m)` — the output matrix plus the adjacency lists.

## Other Approaches

- **DFS topological sort with cycle detection:** run a three-color DFS on each graph and reverse the post-order — Time `O(k^2 + n + m)` / Space `O(k^2 + n + m)`
