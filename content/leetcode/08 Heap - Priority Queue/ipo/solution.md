---
topic: "Heap - Priority Queue"
difficulty: Hard
leetcode: https://leetcode.com/problems/ipo/
neetcode: https://neetcode.io/problems/ipo
---
# IPO - Solution

## Intuition

Capital only grows, so any project that becomes affordable stays affordable. At each step the best move is greedy: among all currently affordable projects, take the one with the largest profit. Taking it can only unlock more projects, never fewer.

## Approach

1. Pair each project as `(capital, profit)` and sort by capital.
2. Keep a max-heap of profits for affordable projects, and a pointer `i` into the sorted list.
3. Repeat up to `k` times:
   - Push the profits of all projects with `capital <= w` onto the heap, advancing `i`.
   - If the heap is empty, stop: nothing is affordable.
   - Pop the largest profit and add it to `w`.
4. Return `w`.

## Code

```python
class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        # O(nlogn)
        maxProfit = [] # only projects we can afford
        minCapital = [(c, p) for c, p in zip(capital, profits)]
        heapq.heapify(minCapital)

        for i in range(k):
            
            while minCapital and minCapital[0][0] <= w:
                c, p = heapq.heappop(minCapital)
                heapq.heappush(maxProfit, -1 * p)
            if not maxProfit:
                break
            w += -1 * heapq.heappop(maxProfit)
        return w
```

## Complexity

- **Time:** `O(n log n + k log n)` — sorting plus at most `n` pushes and `k` pops, each `O(log n)`.
- **Space:** `O(n)` — sorted list and heap.

## Other Approaches

- **Two heaps:** a min-heap keyed by capital feeds a max-heap keyed by profit; same idea as above without a full sort — Time `O((n + k) log n)` / Space `O(n)`
- **Brute force greedy:** each round scan all projects for the most profitable affordable one — Time `O(k · n)` / Space `O(n)`
