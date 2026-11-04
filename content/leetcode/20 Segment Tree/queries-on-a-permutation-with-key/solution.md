---
topic: "Segment Tree"
difficulty: Medium
leetcode: https://leetcode.com/problems/queries-on-a-permutation-with-key/
---
# Queries on a Permutation With Key - Solution

## Intuition

The position of a value is the number of elements currently in front of it. Moving elements to the front can be modelled with a Fenwick tree (a lightweight range-sum structure) over a timeline of slots: reserve `len(queries)` extra slots in front of the initial permutation, so that "move to front" becomes "clear the old slot and mark a new slot one step further left". The position is then a prefix sum of occupied slots.

## Approach

1. Create a Fenwick tree of size `n + m`, where `n = len(queries)`. Slots `n+1 .. n+m` initially hold the values `1..m` (one marker each); slots `1..n` are free for future front placements.
2. Store `pos[v] = n + v`, the current slot of value `v`.
3. For query `i` (0-indexed), with `v = queries[i]`: the answer is the prefix sum over slots `1 .. pos[v] - 1`, i.e. the number of occupied slots before it.
4. Remove the marker at `pos[v]`, set `pos[v] = n - i` (a fresh slot left of all occupied ones), and add a marker there.
5. Collect and return the answers.

## Code

```python
from typing import List, Optional

class Solution:
    def processQueries(self, queries: List[int], m: int) -> List[int]:
        n = len(queries)
        size = n + m
        tree = [0] * (size + 1)

        def update(i: int, delta: int) -> None:
            while i <= size:
                tree[i] += delta
                i += i & -i

        def query(i: int) -> int:
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & -i
            return total

        pos = [0] * (m + 1)
        for v in range(1, m + 1):
            pos[v] = n + v
            update(pos[v], 1)

        res = []
        for i, v in enumerate(queries):
            res.append(query(pos[v] - 1))
            update(pos[v], -1)
            pos[v] = n - i  # free slot left of everything placed so far
            update(pos[v], 1)
        return res
```

## Complexity

- **Time:** `O((n + m) log(n + m))` — building costs `m` updates, and each query does one prefix sum and two updates, each `O(log(n + m))`.
- **Space:** `O(n + m)` — the Fenwick tree and the position array.

## Other Approaches

- **Simulation with a list:** use `list.index` and `pop`/`insert(0, ...)` on `P` directly — Time `O(n * m)` / Space `O(m)`. Fast enough for `m <= 10^3`.
- **Segment tree:** same slot idea as above but with a segment tree for the range count — Time `O((n + m) log(n + m))` / Space `O(n + m)`.
