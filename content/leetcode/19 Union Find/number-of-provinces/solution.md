---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/number-of-provinces/
---
# Number of Provinces - Solution

## Intuition

Each province is a connected component of the graph whose adjacency matrix is `isConnected`. Start with every city in its own component (`n` provinces); each time a direct connection merges two different components, the province count drops by one.

## Approach

1. Create a Union Find structure with `n` nodes and set `count = n`.
2. For every pair `i < j`, if `isConnected[i][j] == 1`, union `i` and `j`.
3. A union that joins two different roots decrements `count`.
4. Return `count`.

## Code

```python
from typing import List, Optional

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        count = n
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    ri, rj = find(i), find(j)
                    if ri == rj:
                        continue
                    if rank[ri] < rank[rj]:
                        ri, rj = rj, ri
                    parent[rj] = ri
                    if rank[ri] == rank[rj]:
                        rank[ri] += 1
                    count -= 1
        return count
```

## Complexity

- **Time:** `O(n^2 · α(n))` — every cell of the upper triangle is visited once, and each union/find is near-constant amortized.
- **Space:** `O(n)` — the `parent` and `rank` arrays.

## Other Approaches

- **DFS:** visit unvisited cities and flood-fill their component, counting the number of starts — Time `O(n^2)` / Space `O(n)`
- **BFS:** same idea as DFS using a queue — Time `O(n^2)` / Space `O(n)`
