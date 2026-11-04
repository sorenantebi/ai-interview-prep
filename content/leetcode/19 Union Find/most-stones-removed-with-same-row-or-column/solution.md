---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/
---
# Most Stones Removed with Same Row or Column - Solution

## Intuition

Stones that share a row or column form a connected group. Within one connected group, you can always remove every stone except one (remove them in reverse order of a DFS traversal, leaving the root). Stones in different groups never interact. So the answer is `n - (number of connected components)`.

## Approach

1. Treat each row and each column as a node in a union-find structure. Columns are offset by `10001` so they don't collide with rows.
2. For each stone `[x, y]`, union node `x` with node `y + 10001`. This connects every stone sharing that row or column.
3. Count the distinct roots among all the row/column nodes that appeared in stones. Each root corresponds to one component of stones.
4. Return `len(stones) - components`.

## Code

```python
from typing import List, Optional

class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        parent = {}

        def find(x: int) -> int:
            if x not in parent:
                parent[x] = x
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for x, y in stones:
            union(x, y + 10001)  # offset keeps columns distinct from rows

        components = len({find(x) for x in list(parent)})
        return len(stones) - components
```

## Complexity

- **Time:** `O(n · α(n))` — one union per stone, with near-constant amortized cost per operation thanks to path compression.
- **Space:** `O(n)` — the parent map holds at most one entry per distinct row and column, so at most `2n` nodes.

## Other Approaches

- **DFS over stones:** build connectivity by checking shared row/column between stones, count components, return `n - components` — Time `O(n²)` / Space `O(n)`
- **DFS over row/column graph:** build an adjacency map from rows to columns, traverse components — Time `O(n)` / Space `O(n)`
