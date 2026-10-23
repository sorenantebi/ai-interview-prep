---
topic: "Intervals"
difficulty: Hard
leetcode: https://leetcode.com/problems/minimum-interval-to-include-each-query/
neetcode: https://neetcode.io/problems/minimum-interval-including-query
---
# Minimum Interval to Include Each Query - Solution

**Question:** Minimum Interval to Include Each Query - Question · **Difficulty:** Hard

## Intuition

Answer the queries offline in increasing order. Sort intervals by left endpoint; as the query value grows, push every interval that has started (`left <= q`) into a min-heap keyed by size. Intervals at the top whose `right < q` can never contain this or any later (larger) query, so they are discarded lazily. The heap top is then the smallest interval containing `q`.

## Approach

1. Sort `intervals` by `left`; create the list of query values sorted ascending.
2. For each query `q` in sorted order:
   - Push `(size, right)` for all intervals with `left <= q` (pointer `i` advances monotonically).
   - Pop from the heap while the top's `right < q` (it ended before `q`).
   - The answer for `q` is the top's size, or `-1` if the heap is empty.
3. Store answers in a dict keyed by query value and map them back to the original order (duplicate queries share an answer).

## Code

```python
class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort()
        minHeap = []
        res = {}
        i = 0
        for q in sorted(queries):
            while i < len(intervals) and intervals[i][0] <= q:
                l, r = intervals[i]
                heapq.heappush(minHeap, (r - l + 1, r))
                i += 1

            while minHeap and minHeap[0][1] < q:
                heapq.heappop(minHeap)
            res[q] = minHeap[0][0] if minHeap else -1
        return [res[q] for q in queries]
```

## Complexity

- **Time:** `O(n log n + q log q)` — sorting both arrays; each interval is pushed and popped at most once (`O(n log n)`).
- **Space:** `O(n + q)` — the heap and the answer map.

## Other Approaches

- **Brute force:** for each query scan all intervals — Time `O(n · q)`, Space `O(1)` extra.
- **Sort intervals by size + union-find / ordered set over sorted queries:** assign each interval (smallest first) to all still-unanswered queries in its range, skipping answered ones — Time `O((n + q) log q)`, Space `O(q)`.

## Key Takeaway

Offline query processing: sort queries and events together, sweep once, and use a heap with lazy deletion to keep "the best currently-valid candidate" on top.
