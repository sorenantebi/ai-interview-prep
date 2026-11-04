---
topic: "Union Find"
difficulty: Medium
leetcode: https://leetcode.com/problems/satisfiability-of-equality-equations/
---
# Satisfiability of Equality Equations - Solution

## Intuition

Equality is transitive and symmetric, so all `==` equations partition the variables into groups that must share the same value. An `!=` equation is then violated only if both of its variables fall into the same group. Union-Find models these groups directly.

## Approach

1. Create a Union-Find structure over the 26 lowercase letters.
2. First pass: for every `==` equation, union the two variables.
3. Second pass: for every `!=` equation, check whether the two variables share the same root. If they do, return `false`.
4. If no `!=` equation contradicts the groups, return `true`.

Processing all `==` equations before any `!=` equation is essential, since a later equality can merge groups that an earlier inequality relied on being separate.

## Code

```python
from typing import List, Optional

class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        parent = list(range(26))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            parent[find(a)] = find(b)

        for eq in equations:
            if eq[1] == '=':
                union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))

        for eq in equations:
            if eq[1] == '!':
                if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                    return False

        return True
```

## Complexity

- **Time:** `O(n · α(26))` — each equation triggers a constant number of find/union operations, which are effectively constant time with path compression over 26 nodes.
- **Space:** `O(1)` — the parent array always has 26 entries regardless of input size.

## Other Approaches

- **DFS / BFS on a graph:** build an adjacency list from `==` equations, label connected components, then check each `!=` pair against the labels — Time `O(n)` / Space `O(1)` (26 nodes, at most 26² edges)
- **Union by rank in addition to path compression:** same idea with slightly stronger amortized guarantees — Time `O(n · α(26))` / Space `O(1)`
