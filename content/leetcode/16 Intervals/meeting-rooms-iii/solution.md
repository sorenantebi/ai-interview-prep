---
topic: "Intervals"
difficulty: Hard
leetcode: https://leetcode.com/problems/meeting-rooms-iii/
neetcode: https://neetcode.io/problems/meeting-rooms-iii
---
# Meeting Rooms III - Solution

## Intuition

Process meetings in order of start time and simulate. Two min-heaps do the work: one holds the free room numbers (so the lowest is always at the top), the other holds `(end_time, room)` for busy rooms. When no room is free, the earliest-finishing busy room gets the delayed meeting, and the meeting is shifted to start at that room's end time.

## Approach

1. Sort `meetings` by start time.
2. Keep a min-heap `free` of room numbers, initially `0..n-1`, and a min-heap `busy` of `(end_time, room)`. Keep a `count` array per room.
3. For each meeting `[start, end]`:
   - Move every room from `busy` whose end time is `<= start` back into `free`.
   - If `free` is non-empty, pop the lowest room and schedule the meeting as `[start, end)`.
   - Otherwise pop the earliest-ending room `(t, room)` from `busy` and schedule the meeting at `t` with the same duration, so it ends at `t + (end - start)`.
   - Increment `count[room]` and push the new end time onto `busy`.
4. Return the lowest-indexed room with the maximum count.

## Code

```python
class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()

        available = [i for i in range(n)]
        used = []
        count = [0] * n

        for start, end in meetings:
            while used and start >= used[0][0]:
                _, room = heapq.heappop(used)
                heapq.heappush(available, room)

            if not available:
                end_time, room = heapq.heappop(used)
                end = end_time + (end - start)
                heapq.heappush(available, room)

            room = heapq.heappop(available)
            heapq.heappush(used, (end, room))
            count[room] += 1

        return count.index(max(count))
```

## Complexity

- **Time:** `O(m log m + m log n)` — sorting `m` meetings, then each meeting does a constant number of heap operations on heaps of size at most `n`.
- **Space:** `O(n)` — the two heaps and the count array hold at most `n` rooms (excluding the sort).

## Other Approaches

- **Array scan per meeting:** track each room's free-at time in an array and scan all `n` rooms for every meeting — Time `O(m log m + m·n)` / Space `O(n)`
