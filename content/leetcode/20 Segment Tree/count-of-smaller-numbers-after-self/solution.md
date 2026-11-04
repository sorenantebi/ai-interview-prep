---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/count-of-smaller-numbers-after-self/
---
# Count of Smaller Numbers After Self - Solution

## Intuition

Scanning from right to left, when we reach `nums[i]` we need to know how many already-seen values are strictly smaller. Since values lie in a small range (`[-10^4, 10^4]`), we can keep a tree over value space that stores how many times each value has been seen, and answer "how many seen values are less than `x`" as a prefix-sum query. Each step is one query plus one point update.

## Approach

1. Shift every value by `10^4` so indices are in `[0, 20000]`.
2. Build a tree (an iterative segment tree) of size `20001` over value space, initially all zeros.
3. Iterate `i` from `n - 1` down to `0`.
4. For `nums[i]`, query the sum over the index range `[0, v - 1]`; this is `counts[i]`.
5. Point-update index `v` by `+1`.
6. Return `counts`.

## Code

```python
from typing import List, Optional

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        OFFSET = 10 ** 4
        size = 2 * OFFSET + 1
        tree = [0] * (2 * size)

        def update(pos: int) -> None:
            pos += size
            while pos >= 1:
                tree[pos] += 1
                pos //= 2

        def query(left: int, right: int) -> int:
            # sum over half-open range [left, right)
            res = 0
            left += size
            right += size
            while left < right:
                if left & 1:
                    res += tree[left]
                    left += 1
                if right & 1:
                    right -= 1
                    res += tree[right]
                left //= 2
                right //= 2
            return res

        n = len(nums)
        counts = [0] * n
        for i in range(n - 1, -1, -1):
            v = nums[i] + OFFSET
            counts[i] = query(0, v)
            update(v)
        return counts
```

## Complexity

- **Time:** `O(n log V)` — each of the `n` elements does one query and one update, each `O(log V)` with `V = 20001`.
- **Space:** `O(V + n)` — the tree has `2V` nodes and the output has `n` entries.

## Other Approaches

- **Binary Indexed Tree (Fenwick):** same idea with a simpler prefix-sum structure over value space (or compressed ranks) — Time `O(n log V)` / Space `O(V)`
- **Merge Sort with index tracking:** while merging sorted halves, count how many right-half elements move ahead of each left-half element — Time `O(n log n)` / Space `O(n)`
- **Balanced BST / sorted list with binary search:** insert from the right and use rank queries; `bisect.insort` on a list is simple but `O(n)` per insert in the worst case — Time `O(n log n)` to `O(n²)` / Space `O(n)`
