---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/smallest-string-with-swaps/
---
# Smallest String With Swaps - Solution

## Intuition

Swaps are transitive: if index 0 can swap with 1, and 1 with 2, then the characters at 0, 1, 2 can be arranged in any order. So the indices split into connected components, and within each component the characters can be permuted freely. The smallest result sorts each component's characters and places them at that component's sorted indices.

## Approach

1. Build a union-find over the indices `0..n-1` and union the two indices of every pair.
2. Group indices by their root, visiting indices in increasing order so each group's index list is already sorted.
3. For each group, sort its characters.
4. Write the sorted characters back into the group's indices in order.
5. Join the result into a string.

## Code

```python
from typing import List, Optional

class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for a, b in pairs:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        groups = {}
        for i in range(n):
            groups.setdefault(find(i), []).append(i)

        res = [''] * n
        for indices in groups.values():
            chars = sorted(s[i] for i in indices)
            for i, c in zip(indices, chars):
                res[i] = c
        return ''.join(res)
```

## Complexity

- **Time:** `O(n log n + m α(n))` — union-find over `m` pairs is near-linear, and sorting the characters across all components costs at most `O(n log n)`.
- **Space:** `O(n)` — parent array, groups, and the result list.

## Other Approaches

- **DFS/BFS on a graph:** build an adjacency list, collect each connected component, sort its characters and indices, then assign — Time `O(n log n + m)` / Space `O(n + m)`
- **Union-find with counting sort:** per component, count letters (26 buckets) instead of comparison sorting — Time `O(26n + m α(n))` / Space `O(n)`
