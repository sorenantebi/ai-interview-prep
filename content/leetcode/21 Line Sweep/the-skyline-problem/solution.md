---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/the-skyline-problem/
---
# The Skyline Problem - Solution

## Intuition

The skyline height can only change at a building's left or right edge. Sweeping from left to right, the skyline height at any x is the maximum height among the buildings currently "active" (those covering x). A max-heap gives that maximum quickly, and expired buildings can be removed lazily when they surface at the top.

## Approach

1. Build a sorted list of all distinct x coordinates where something happens (every left and right edge).
2. Sweep through these x values in order, keeping a pointer `i` into `buildings` (already sorted by left edge).
3. For each x, push every building with `left <= x` onto a max-heap as `(-height, right)`.
4. Pop from the heap top while its `right <= x`, since that building has ended.
5. The current height is the top of the heap's height, or `0` if the heap is empty.
6. If this height differs from the last height in the result, append `[x, height]`. This also merges equal-height consecutive segments.
7. Return the result.

## Code

```python
from typing import List, Optional
import heapq

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        xs = sorted({x for l, r, _ in buildings for x in (l, r)})
        res = []
        heap = []
        i = 0
        n = len(buildings)
        for x in xs:
            while i < n and buildings[i][0] <= x:
                heapq.heappush(heap, (-buildings[i][2], buildings[i][1]))
                i += 1
            # lazy deletion: drop buildings that have already ended
            while heap and heap[0][1] <= x:
                heapq.heappop(heap)
            h = -heap[0][0] if heap else 0
            if not res or res[-1][1] != h:
                res.append([x, h])
        return res
```

## Complexity

- **Time:** `O(n log n)` — sorting the `2n` coordinates costs `O(n log n)`, and each building is pushed and popped at most once, each in `O(log n)`.
- **Space:** `O(n)` — the coordinate list, the heap, and the output each hold at most `O(n)` entries.

## Other Approaches

- **Divide and conquer (merge skylines):** recursively compute the skyline of each half and merge them like merge sort, tracking the current heights of both sides — Time `O(n log n)` / Space `O(n)`
- **Sweep over events with a sorted multiset:** create `(x, ±height)` events, sort them, and keep active heights in a balanced tree or multiset — Time `O(n log n)` / Space `O(n)`
- **Brute force over coordinates:** for each distinct x, scan all buildings for the maximum covering height — Time `O(n²)` / Space `O(n)`
