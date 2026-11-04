---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/create-sorted-array-through-instructions/
---
# Create Sorted Array through Instructions - Solution

## Intuition

For each insertion we only need two counts: how many already-inserted values are strictly less than `x`, and how many are strictly greater. Both are prefix/suffix sums over a frequency table of values, with point updates after each insertion. A Fenwick tree (a compact form of a segment tree for prefix sums) supports both operations in `O(log M)`, where `M` is the maximum value.

## Approach

1. Create a Fenwick tree of size `max(instructions)` that stores the frequency of each value inserted so far.
2. For each `x` at index `i` (so `i` elements are already inserted):
   - `less = query(x - 1)`, the count of values `< x`.
   - `lessOrEqual = query(x)`, the count of values `<= x`.
   - `greater = i - lessOrEqual`.
3. Add `min(less, greater)` to the total.
4. Update the tree at position `x` by `+1`.
5. Return the total modulo `10^9 + 7`.

## Code

```python
from typing import List, Optional

class Solution:
    def createSortedArray(self, instructions: List[int]) -> int:
        MOD = 10**9 + 7
        size = max(instructions)
        tree = [0] * (size + 1)

        def update(i: int) -> None:
            while i <= size:
                tree[i] += 1
                i += i & -i

        def query(i: int) -> int:
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & -i
            return total

        cost = 0
        for i, x in enumerate(instructions):
            less = query(x - 1)
            greater = i - query(x)
            cost += min(less, greater)
            update(x)
        return cost % MOD
```

## Complexity

- **Time:** `O(n log M)` — each of the `n` elements does two queries and one update, each taking `O(log M)`.
- **Space:** `O(M)` — the Fenwick tree has one slot per possible value.

## Other Approaches

- **Segment tree over values:** same idea with an explicit segment tree for range counts — Time `O(n log M)` / Space `O(M)`
- **Merge sort with counting:** count smaller/greater earlier elements for each index during merge sort — Time `O(n log n)` / Space `O(n)`
- **Sorted list with binary search:** `bisect` to find counts, then `insort` — Time `O(n^2)` worst case due to insertion shifts / Space `O(n)`
