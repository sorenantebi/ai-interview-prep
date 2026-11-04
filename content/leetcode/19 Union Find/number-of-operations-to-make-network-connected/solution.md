---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-operations-to-make-network-connected/
---
# Number of Operations to Make Network Connected - Solution

## Intuition

Connecting `n` computers requires at least `n - 1` cables. If there are fewer, it is impossible. Otherwise, enough cables exist, and every redundant cable (one that closes a cycle) can be moved freely. Each move can merge two components, so if the network has `c` connected components, exactly `c - 1` moves are needed.

## Approach

1. If `len(connections) < n - 1`, return `-1`.
2. Build a Union Find over the `n` computers.
3. For each connection, union its endpoints; each successful union reduces the component count by one.
4. Return the number of components minus one.

## Code

```python
from typing import List, Optional

class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:
            return -1

        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in connections:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                components -= 1

        return components - 1
```

## Complexity

- **Time:** `O(n + m * α(n))` — one pass over the connections with near-constant amortized `find` thanks to path compression, where `m = len(connections)`.
- **Space:** `O(n)` — the parent array.

## Other Approaches

- **DFS/BFS component counting:** build an adjacency list and count connected components, then return `components - 1` — Time `O(n + m)` / Space `O(n + m)`
