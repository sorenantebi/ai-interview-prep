---
topic: "Heap / Priority Queue"
difficulty: Easy
leetcode: https://leetcode.com/problems/last-stone-weight/
neetcode: https://neetcode.io/problems/last-stone-weight
---
# Last Stone Weight - Solution

**Question:** Last Stone Weight - Question · **Difficulty:** Easy

## Intuition

Each round needs the two current maximums, and the result (if any) goes back into the pool. That "repeatedly extract max and re-insert" pattern is exactly what a **max-heap** does efficiently. Python only has a min-heap, so store negated weights.

## Approach

1. Build a max-heap by negating every weight and heapifying.
2. While at least two stones remain, pop the heaviest `y` and the next `x`.
3. If `y > x`, push `y - x` back.
4. Return the remaining stone's weight, or `0` if the heap is empty.

## Code

```python
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = [-s for s in stones]
        heapq.heapify(stones)

        while len(stones) > 1:
            first = heapq.heappop(stones)
            second = heapq.heappop(stones)
            if second > first:
                heapq.heappush(stones, first - second)

        stones.append(0)
        return abs(stones[0])

# There's a private _heapify_max method.
# https://github.com/python/cpython/blob/1170d5a292b46f754cd29c245a040f1602f70301/Lib/heapq.py#L198
class Solution(object):
    def lastStoneWeight(self, stones):
        heapq._heapify_max(stones)
        while len(stones) > 1:
            max_stone = heapq._heappop_max(stones)
            diff = max_stone - stones[0]
            if diff:
                heapq._heapreplace_max(stones, diff)
            else:
                heapq._heappop_max(stones)
        
        stones.append(0)
        return stones[0]
```

## Complexity

- **Time:** `O(n log n)` — at most `n - 1` rounds, each with `O(log n)` heap operations.
- **Space:** `O(n)` — the heap (a copy of the input).

## Other Approaches

- **Sort every round:** re-sort the list and take the last two — Time `O(n^2 log n)`, Space `O(1)` extra.
- **Bucket / counting by weight:** since weights are `<= 1000`, walk a count array from the top — Time `O(n + W)`, Space `O(W)`.

## Key Takeaway

"Repeatedly take the largest items and put a result back" is a max-heap simulation; in Python, negate values to use `heapq` as a max-heap.
