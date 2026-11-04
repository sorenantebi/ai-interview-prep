---
topic: "Union Find"
difficulty: Hard
leetcode: https://leetcode.com/problems/number-of-islands-ii/
neetcode: https://neetcode.io/problems/number-of-islands-ii
---
# Number of Islands II - Solution

## Intuition

Land is only ever added, never removed, so islands only appear or merge. This is the ideal setting for Union Find. Each new land cell starts as its own island (count + 1), and every successful merge with a neighboring island reduces the count by 1.

## Approach

1. Keep a `parent` array of size `m * n`, where cell `(r, c)` has id `r * n + c`. Use `-1` to mean "still water".
2. For each position, if it is already land (duplicate position), append the current count and continue.
3. Otherwise mark it as land (`parent[id] = id`) and increment the island count.
4. For each of the 4 neighbors that is in bounds and is land, `union` it with the new cell. Each union that actually joins two different roots decrements the count.
5. Append the current count to the answer.

## Code

```python
from typing import List, Optional

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        parent = [-1] * (m * n)
        rank = [0] * (m * n)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        count = 0
        res = []
        for r, c in positions:
            idx = r * n + c
            if parent[idx] != -1:
                res.append(count)
                continue
            parent[idx] = idx
            count += 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and parent[nr * n + nc] != -1:
                    if union(idx, nr * n + nc):
                        count -= 1
            res.append(count)
        return res
```

## Complexity

- **Time:** `O(k · α(mn))` — each of the `k` operations does at most 4 unions, each nearly constant time with path compression and union by rank (this also meets the `O(k log(mn))` follow-up).
- **Space:** `O(m · n)` — the `parent` and `rank` arrays.

## Other Approaches

- **Re-run DFS/BFS after each addition:** recount islands on the whole grid every time — Time `O(k · m · n)` / Space `O(m · n)`
- **Union Find with hash map:** store parents only for land cells in a dictionary — Time `O(k · α(mn))` / Space `O(k)`
