---
topic: "Intervals"
difficulty: Medium
leetcode: https://leetcode.com/problems/merge-intervals/
neetcode: https://neetcode.io/problems/merge-intervals
---
# Merge Intervals - Solution

**Question:** Merge Intervals - Question · **Difficulty:** Medium

## Intuition

After sorting by start, any interval that overlaps the current merged block must come right after it — an interval can only overlap the last block if its start is `<=` that block's end. So one pass over the sorted list either extends the last block or starts a new one.

## Approach

1. Sort intervals by start.
2. Initialize `res` with the first interval.
3. For each next interval `[s, e]`: if `s <= res[-1][1]`, set `res[-1][1] = max(res[-1][1], e)`; otherwise append `[s, e]`.
4. Return `res`.

## Code

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda pair: pair[0])
        output = [intervals[0]]

        for start, end in intervals:
            lastEnd = output[-1][1]

            if start <= lastEnd:
                # merge
                output[-1][1] = max(lastEnd, end)
            else:
                output.append([start, end])
        return output
```

## Complexity

- **Time:** `O(n log n)` — dominated by sorting; the merge pass is `O(n)`.
- **Space:** `O(n)` for the output (plus `O(n)` used by Python's sort).

## Other Approaches

- **Sweep over endpoints / counting array:** mark +1 at starts and -1 after ends over the coordinate range and read off covered segments — Time `O(n + V)` where `V` is the value range, Space `O(V)`; fiddly with touching endpoints.
- **Graph of overlapping intervals + connected components:** Time `O(n^2)`, Space `O(n^2)`.

## Key Takeaway

Sort by start, then greedily extend the last merged interval with `max(end)` — the template for most interval problems.

## C++

```cpp
/*
    Given an array of intervals, merge all overlapping intervals
    Ex. intervals = [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]

    Sort by earliest start time, merge overlapping intervals (take longer end time)

    Time: O(n log n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        int n = intervals.size();
        if (n == 1) {
            return intervals;
        }
        
        sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
           return a[0] < b[0]; 
        });
        
        vector<vector<int>> result;
        
        int i = 0;
        while (i < n - 1) {
            if (intervals[i][1] >= intervals[i+1][0]) {
                intervals[i+1][0] = intervals[i][0];
                intervals[i+1][1] = max(intervals[i][1], intervals[i+1][1]);
            } else {
                result.push_back(intervals[i]);
            }
            i++;
        }
        result.push_back(intervals[i]);
        
        return result;
    }
};
```
