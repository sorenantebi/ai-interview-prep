---
topic: "Segment Tree"
difficulty: Hard
leetcode: https://leetcode.com/problems/falling-squares/
---
# Falling Squares - Solution

## Intuition

A new square lands on the highest point under its footprint `[left, left + side)`. Its top is therefore `(max height in that range) + side`. Every point in the range now has that height, which is at least the old maximum. So we need two operations over a range of the X-axis: query the maximum, and raise everything to a value.

Coordinates go up to 10^8, but only the square edges matter. We compress them and treat each gap between consecutive edges as one elementary cell. A segment tree over these cells then handles both operations in logarithmic time.

Because squares only touch at a boundary (half-open intervals), a square that merely brushes another covers no shared cell, matching the "does not count as landing" rule.

## Approach

1. Collect every `left` and `left + side`, sort and deduplicate them into `xs`. Cell `i` stands for the interval `[xs[i], xs[i+1])`, so there are `len(xs) - 1` cells.
2. Build a segment tree with two arrays: `mx[node]` is the maximum height in the node's range, and `tag[node]` is the largest height assigned to the node's whole range.
3. For each square, map its edges to cell indices `l = idx[left]` and `r = idx[left + side] - 1`.
4. Query the max over `[l, r]`. When descending through a partial node, include its `tag`, since the tag applies to the whole range.
5. Compute `h = query + side` and update `[l, r]` with `h`. Because `h` is at least every existing height in the range, a max-assign is equivalent to an overwrite. Fully covered nodes update `mx` and `tag`. Other nodes recompute `mx` from their children and their own tag.
6. Keep a running global maximum and append it to the answer after each drop.

Tags are never pushed down; they are consulted during queries instead.

## Code

```python
from typing import List, Optional

class Solution:
    def fallingSquares(self, positions: List[List[int]]) -> List[int]:
        xs = sorted({x for left, side in positions for x in (left, left + side)})
        idx = {x: i for i, x in enumerate(xs)}
        m = len(xs) - 1
        mx = [0] * (4 * m)
        tag = [0] * (4 * m)

        def update(node: int, lo: int, hi: int, l: int, r: int, h: int) -> None:
            if l <= lo and hi <= r:
                mx[node] = max(mx[node], h)
                tag[node] = max(tag[node], h)
                return
            mid = (lo + hi) // 2
            if l <= mid:
                update(2 * node, lo, mid, l, r, h)
            if r > mid:
                update(2 * node + 1, mid + 1, hi, l, r, h)
            mx[node] = max(tag[node], mx[2 * node], mx[2 * node + 1])

        def query(node: int, lo: int, hi: int, l: int, r: int) -> int:
            if l <= lo and hi <= r:
                return mx[node]
            res = tag[node]  # tag covers the node's whole range, including the queried part
            mid = (lo + hi) // 2
            if l <= mid:
                res = max(res, query(2 * node, lo, mid, l, r))
            if r > mid:
                res = max(res, query(2 * node + 1, mid + 1, hi, l, r))
            return res

        ans = []
        best = 0
        for left, side in positions:
            l = idx[left]
            r = idx[left + side] - 1
            h = query(1, 0, m - 1, l, r) + side
            update(1, 0, m - 1, l, r, h)
            best = max(best, h)
            ans.append(best)
        return ans
```

## Complexity

- **Time:** `O(n log n)` — sorting the `2n` coordinates costs `O(n log n)`, and each of the `n` squares does one query and one update, each `O(log n)`.
- **Space:** `O(n)` — the compressed coordinates and the two segment tree arrays are all `O(n)`.

## Other Approaches

- **Brute force over previous squares:** for each new square, check overlap with every earlier square and take the max top plus the side length — Time `O(n²)` / Space `O(n)`
- **Sorted boundary map (offline-free interval map):** keep a sorted list of height-intervals, then split and overwrite the covered range for each drop — Time `O(n²)` worst case / Space `O(n)`
