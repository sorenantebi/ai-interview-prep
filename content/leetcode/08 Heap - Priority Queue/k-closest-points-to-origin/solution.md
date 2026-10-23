---
topic: "Heap / Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/k-closest-points-to-origin/
neetcode: https://neetcode.io/problems/k-closest-points-to-origin
---
# K Closest Points to Origin - Solution

**Question:** K Closest Points to Origin - Question · **Difficulty:** Medium

## Intuition

We need the `k` smallest distances, not a full ordering. Keep a **max-heap of size `k`** keyed by squared distance: any point farther than the current worst of the best `k` is discarded. Squared distance preserves ordering, so `sqrt` is unnecessary.

## Approach

1. For each point compute `d = x*x + y*y`.
2. Push `(-d, x, y)` onto a heap (negated to make it a max-heap).
3. If the heap grows beyond `k`, pop — this removes the farthest point currently kept.
4. Return the coordinates left in the heap.

## Code

```python
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        minHeap = []
        for x, y in points:
            dist = (x ** 2) + (y ** 2)
            minHeap.append((dist, x, y))
        
        heapq.heapify(minHeap)
        res = []
        for _ in range(k):
            _, x, y = heapq.heappop(minHeap)
            res.append((x, y))
        return res
```

## Complexity

- **Time:** `O(n log k)` — each of the `n` points costs at most one push and one pop on a heap of size `k + 1`.
- **Space:** `O(k)` — the heap (output also `O(k)`).

## Other Approaches

- **Sort by distance:** `sorted(points, key=dist)[:k]` — Time `O(n log n)`, Space `O(n)`.
- **Quickselect on distance:** partition until the first `k` are the closest — Time `O(n)` average / `O(n^2)` worst, Space `O(1)` extra.

## Key Takeaway

For "k smallest", keep a max-heap of size `k` (and vice versa); compare squared distances to avoid floating point.
