---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/meeting-rooms-ii/
neetcode: https://neetcode.io/problems/meeting-schedule-ii
---
# Meeting Rooms II - Solution

**Question:** Meeting Rooms II - Question · **Difficulty:** Medium

## Intuition

The answer is the maximum number of meetings in progress at the same moment. Sweep through the start times in order while a pointer walks the sorted end times: every start needs a room, and every end that is `<=` the current start has already freed one. The peak of "starts so far minus ends so far" is the room count.

## Approach

1. Sort all start times and all end times separately.
2. Walk the starts with index `i` and the ends with index `j`.
3. If `starts[i] < ends[j]`, a new meeting begins before any room frees: `count += 1`, `i += 1`. Otherwise a meeting has ended: `count -= 1`, `j += 1` (ties process the end first, so back-to-back meetings share a room).
4. Track the maximum `count` and return it.

## Code

```python
def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        time = []
        for start, end in intervals:
            time.append((start, 1))
            time.append((end, -1))
        
        time.sort(key=lambda x: (x[0], x[1]))
        
        count = 0
        max_count = 0
        for t in time:
            count += t[1]
            max_count = max(max_count, count)
        return max_count
```

## Complexity

- **Time:** `O(n log n)` — two sorts plus a linear sweep.
- **Space:** `O(n)` — the two sorted arrays.

## Other Approaches

- **Min-heap of end times:** sort by start; pop the heap top if it ended by the current start, then push the current end; the heap's size at the end is the answer — Time `O(n log n)`, Space `O(n)`.
- **Difference map / sweep line:** `+1` at each start, `-1` at each end, sort the keys and track the running maximum — Time `O(n log n)`, Space `O(n)`.

## Key Takeaway

"Minimum resources for overlapping intervals" = maximum overlap depth, computed by a sweep over sorted start/end events (or a min-heap of end times).
