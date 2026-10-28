---
topic: "Intervals"
difficulty: Easy
leetcode: https://leetcode.com/problems/meeting-rooms/
neetcode: https://neetcode.io/problems/meeting-schedule
---
# Meeting Rooms - Solution

**Question:** Meeting Rooms - Question · **Difficulty:** Easy

## Intuition

If meetings are sorted by start time, any conflict must occur between two **adjacent** meetings: if meeting `i` doesn't overlap meeting `i + 1`, it cannot overlap any later one either, since they start even later. So sort and compare each meeting's start with the previous meeting's end.

## Approach

1. Sort intervals by start time.
2. For each consecutive pair, if `intervals[i][0] < intervals[i - 1][1]`, the meetings overlap → return `False`.
3. If no pair conflicts, return `True` (this also covers 0 or 1 meetings).

## Code

```python
class Solution:
    """
    @param intervals: an array of meeting time intervals
    @return: if a person could attend all meetings
    """

    def canAttendMeetings(self, intervals):
        intervals.sort(key=lambda i: i[0])

        for i in range(1, len(intervals)):
            i1 = intervals[i - 1]
            i2 = intervals[i]

            if i1[1] > i2[0]:
                return False
        return True
```

## Complexity

- **Time:** `O(n log n)` — sorting dominates.
- **Space:** `O(1)` extra (besides the sort's internal buffer).

## Other Approaches

- **Compare all pairs:** check every pair for overlap — Time `O(n^2)`, Space `O(1)`.

## Key Takeaway

After sorting intervals by start, overlap checks only need adjacent pairs — a recurring simplification in interval problems.

## C++

```cpp
/*
    Given array of time intervals, determine if can attend all meetings
    Ex. intervals = [[0,30],[5,10],[15,20]] -> false

    Sort by start time, check adj meetings, if overlap return false

    Time: O(n log n)
    Space: O(1)
*/

class Solution {
public:
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        if (intervals.empty()) {
            return true;
        }
        
        sort(intervals.begin(), intervals.end());
        for (int i = 0; i < intervals.size() - 1; i++) {
            if (intervals[i][1] > intervals[i + 1][0]) {
                return false;
            }
        }
        return true;
    }
};
```
