---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/longest-increasing-subsequence-ii/
---
# Longest Increasing Subsequence II - Solution

## Intuition

Let `dp[v]` be the length of the longest valid subsequence ending with value `v`. When processing a number `x`, the previous element of the subsequence must lie in `[x - k, x - 1]`, so `dp[x] = 1 + max(dp[x-k .. x-1])`. This is a range-maximum query followed by a point update, which a segment tree handles in `O(log M)`, where `M` is the maximum value.

## Approach

1. Build a segment tree over values `1..max(nums)` storing the maximum `dp` value, initialised to 0.
2. For each `x` in `nums`, in order, query the maximum over `[max(1, x - k), x - 1]`.
3. Set `dp[x] = query + 1` and update position `x` with the maximum of its current value and the new value.
4. The answer is the largest `dp` value seen (the root of the tree).

## Code

```python
from typing import List, Optional

class Solution:
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        size = 1
        while size < max(nums) + 1:
            size *= 2
        tree = [0] * (2 * size)

        def query(lo: int, hi: int) -> int:
            # max over the inclusive range [lo, hi]
            res = 0
            lo += size
            hi += size + 1
            while lo < hi:
                if lo & 1:
                    res = max(res, tree[lo])
                    lo += 1
                if hi & 1:
                    hi -= 1
                    res = max(res, tree[hi])
                lo >>= 1
                hi >>= 1
            return res

        def update(pos: int, val: int) -> None:
            pos += size
            tree[pos] = max(tree[pos], val)
            pos >>= 1
            while pos:
                tree[pos] = max(tree[2 * pos], tree[2 * pos + 1])
                pos >>= 1

        for x in nums:
            best = query(max(0, x - k), x - 1) if x > 0 else 0
            update(x, best + 1)
        return tree[1]
```

## Complexity

- **Time:** `O(n log M)` — each element does one range query and one point update on a tree of size `M = max(nums)`.
- **Space:** `O(M)` — the segment tree stores about `2M` entries.

## Other Approaches

- **Brute-force DP:** for each element, scan all earlier elements and take the best valid predecessor — Time `O(n^2)` / Space `O(n)`
- **Coordinate-compressed segment tree:** compress values and binary search the lower bound `x - k` to shrink the tree when values are sparse — Time `O(n log n)` / Space `O(n)`
