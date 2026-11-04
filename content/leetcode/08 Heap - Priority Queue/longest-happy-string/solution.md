---
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-happy-string/
neetcode: https://neetcode.io/problems/longest-happy-string
---
# Longest Happy String - Solution

## Intuition

Greedily use the letter with the most remaining copies, since the most abundant letter is the one most likely to get stuck. The only restriction is that we cannot place a third identical letter in a row. When that happens, we place one copy of the second most abundant letter to break the run, then resume with the most abundant.

## Approach

1. Push each letter with a positive count into a max-heap (store negative counts in Python's min-heap).
2. Repeatedly pop the letter with the largest remaining count.
3. If the last two characters of the result are both that letter, it cannot be used again. Pop the next-largest letter instead. If the heap is empty, stop.
4. Append one copy of the chosen letter, decrement its count, and push it back if any copies remain.
5. If the first letter was skipped in step 3, push it back too (unchanged).
6. Return the joined result.

## Code

```python
from typing import List, Optional
import heapq

class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        heap = [(-count, ch) for count, ch in ((a, 'a'), (b, 'b'), (c, 'c')) if count > 0]
        heapq.heapify(heap)
        res = []

        while heap:
            count, ch = heapq.heappop(heap)
            if len(res) >= 2 and res[-1] == ch and res[-2] == ch:
                if not heap:
                    break
                count2, ch2 = heapq.heappop(heap)
                res.append(ch2)
                if count2 + 1 < 0:
                    heapq.heappush(heap, (count2 + 1, ch2))
                heapq.heappush(heap, (count, ch))  # blocked letter is unchanged
            else:
                res.append(ch)
                if count + 1 < 0:
                    heapq.heappush(heap, (count + 1, ch))

        return "".join(res)
```

## Complexity

- **Time:** `O((a + b + c) log 3)` = `O(a + b + c)` — each character appended costs a constant number of heap operations on a heap of at most 3 items.
- **Space:** `O(a + b + c)` — for the output string; the heap is constant size.

## Other Approaches

- **Greedy without a heap:** at each step sort the three counts and pick the largest allowed letter — Time `O(a + b + c)` / Space `O(a + b + c)`
- **Generalised greedy with counters:** track the current run length and choose the largest letter not at run length 2 — Time `O(a + b + c)` / Space `O(a + b + c)`
