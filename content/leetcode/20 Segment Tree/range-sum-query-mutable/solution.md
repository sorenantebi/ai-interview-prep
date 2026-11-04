---
topic: "Segment Tree"
difficulty: Medium
leetcode: https://leetcode.com/problems/range-sum-query-mutable/
---
# Range Sum Query - Mutable - Solution

## Intuition

A plain prefix-sum array answers range queries in `O(1)` but makes an update cost `O(n)`, since every later prefix changes. Storing only the raw array flips the trade-off. A segment tree balances both: each node stores the sum of a segment, so an update touches one leaf-to-root path and a query combines `O(log n)` nodes.

## Approach

1. Let `n = len(nums)`. Allocate an array `tree` of size `2n`. Leaves live at indices `n .. 2n-1`, holding `nums[i]` at `n + i`.
2. Build the internal nodes bottom-up: for `i` from `n-1` down to `1`, set `tree[i] = tree[2i] + tree[2i+1]`.
3. `update(index, val)`: set the leaf `tree[n + index] = val`, then walk up, recomputing each parent as the sum of its two children until reaching the root.
4. `sumRange(left, right)`: convert to a half-open interval `[l, r)` on the leaves (`l = left + n`, `r = right + n + 1`). While `l < r`: if `l` is a right child (odd), add `tree[l]` and move `l` forward; if `r` is odd, move `r` back and add `tree[r]`; then halve both indices.
5. Return the accumulated sum.

## Code

```python
from typing import List, Optional

class NumArray:

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.tree = [0] * self.n + nums
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, val: int) -> None:
        i = index + self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def sumRange(self, left: int, right: int) -> int:
        l, r = left + self.n, right + self.n + 1
        total = 0
        while l < r:
            if l & 1:
                total += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                total += self.tree[r]
            l //= 2
            r //= 2
        return total


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index, val)
# param_2 = obj.sumRange(left, right)
```

## Complexity

- **Time:** `O(n)` to build, `O(log n)` per `update` and per `sumRange` — an update walks one root-to-leaf path, and a query visits at most two nodes per level.
- **Space:** `O(n)` — the tree array holds `2n` values.

## Other Approaches

- **Binary Indexed Tree (Fenwick Tree):** store partial sums indexed by lowest set bit; update by adding the delta, query via prefix sums — Time `O(log n)` per operation / Space `O(n)`
- **Sqrt Decomposition:** split the array into blocks of size about `√n` with cached block sums; update fixes one block, query sums partial and full blocks — Time `O(√n)` per operation / Space `O(n)`
- **Brute Force:** keep the raw array, update in place and sum the range on each query — Time `O(1)` update, `O(n)` query / Space `O(1)` extra
