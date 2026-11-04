---
topic: "Trees"
difficulty: Medium
leetcode: https://leetcode.com/problems/construct-quad-tree/
neetcode: https://neetcode.io/problems/construct-quad-tree
---
# Construct Quad Tree - Solution

## Intuition

The definition of a Quad-Tree is already recursive: a region is either uniform (a leaf) or it is split into four equal quadrants, each handled the same way. So we recurse on square sub-regions described by a top-left corner and a side length.

## Approach

1. Define `build(r, c, size)` for the square region whose top-left cell is `(r, c)` with side `size`.
2. If `size == 1`, return a leaf with the cell's value.
3. Otherwise, recursively build the four quadrants with half the size.
4. If all four children are leaves and share the same `val`, the whole region is uniform, so return a single leaf with that value (this merges the children instead of scanning the region first).
5. Otherwise return an internal node (`isLeaf = False`) holding the four children. `val` can be anything; we use `True`.
6. Return `build(0, 0, n)`.

## Code

```python
from typing import List, Optional

"""
# Definition for a QuadTree node.
class Node:
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
"""

class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        def build(r: int, c: int, size: int) -> 'Node':
            if size == 1:
                return Node(grid[r][c] == 1, True, None, None, None, None)

            half = size // 2
            tl = build(r, c, half)
            tr = build(r, c + half, half)
            bl = build(r + half, c, half)
            br = build(r + half, c + half, half)

            # Merge only when all four children are leaves with the same value
            if (tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf
                    and tl.val == tr.val == bl.val == br.val):
                return Node(tl.val, True, None, None, None, None)

            return Node(True, False, tl, tr, bl, br)

        return build(0, 0, len(grid))
```

## Complexity

- **Time:** `O(n^2)` — the recursion visits each cell exactly once at the leaves, and the total number of nodes created is bounded by a constant multiple of `n^2`.
- **Space:** `O(n^2)` — the tree can have up to `O(n^2)` nodes in the worst case (a checkerboard); the recursion stack itself is only `O(log n)`.

## Other Approaches

- **Check uniformity before splitting:** scan the region; if uniform return a leaf, else split and recurse — Time `O(n^2 log n)` / Space `O(n^2)`
- **2D prefix sums:** compute region sums in `O(1)` to test uniformity (sum equals 0 or `size^2`) before splitting — Time `O(n^2)` / Space `O(n^2)`
