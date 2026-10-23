---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/hand-of-straights/
neetcode: https://neetcode.io/problems/hand-of-straights
---
# Hand of Straights - Solution

**Question:** Hand of Straights - Question · **Difficulty:** Medium

## Intuition

The smallest remaining card can only be the **start** of a group (nothing smaller is left to precede it). So repeatedly take the smallest value `v` with count `c > 0` and open `c` groups starting at `v`, which consumes `c` copies of each of `v, v+1, ..., v+groupSize-1`. If any of those has fewer than `c` copies, it fails.

## Approach

1. If `len(hand) % groupSize != 0`, return `False`.
2. Count cards with a `Counter`.
3. Iterate over the distinct values in sorted order. For value `v` with remaining count `c > 0`, for each `k` in `v .. v + groupSize - 1`: if `count[k] < c`, return `False`; else `count[k] -= c`.
4. Return `True`.

## Code

```python
class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False

        count = {}
        for n in hand:
            count[n] = 1 + count.get(n, 0)

        minH = list(count.keys())
        heapq.heapify(minH)
        while minH:
            first = minH[0]
            for i in range(first, first + groupSize):
                if i not in count:
                    return False
                count[i] -= 1
                if count[i] == 0:
                    if i != minH[0]:
                        return False
                    heapq.heappop(minH)
        return True
```

## Complexity

- **Time:** `O(n log n)` — sorting the distinct values dominates; the inner loop runs `groupSize` steps only for values that start groups (at most `n / groupSize` of them), so it is `O(n)` in total.
- **Space:** `O(n)` — the counter.

## Other Approaches

- **Min-heap of distinct values:** pop the minimum, build one group at a time, and fail if a value runs out out of order — Time `O(n log n)`, Space `O(n)`.
- **Sort + repeatedly build groups one by one from the smallest card:** Time `O(n log n + n * groupSize)`, Space `O(n)`.

## Key Takeaway

In "partition into consecutive runs" problems the minimum remaining element is forced to be a run start — process greedily from the smallest value.
