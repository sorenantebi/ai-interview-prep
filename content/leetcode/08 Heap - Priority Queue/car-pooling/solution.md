---
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/car-pooling/
neetcode: https://neetcode.io/problems/car-pooling
---
# Car Pooling - Solution

## Intuition

Process the trips in order of pickup location while tracking who is currently in the car. A min-heap keyed on drop-off location tells us which passengers should leave before the next pickup. If occupancy ever exceeds capacity after a pickup, the answer is `false`.

## Approach

1. Sort `trips` by pickup location `from`.
2. Keep a min-heap of `(to, numPassengers)` for the groups currently in the car, and a running count `load`.
3. For each trip, pop every group from the heap whose drop-off `to <= from` of the current trip and subtract their passengers from `load`. The `<=` handles drop-offs happening before pickups at the same kilometer.
4. Add the current trip's passengers to `load` and push `(to, numPassengers)`.
5. If `load > capacity`, return `false`.
6. If all trips are processed without exceeding capacity, return `true`.

## Code

```python
from typing import List, Optional
import heapq

class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        heap = []
        load = 0

        for num, start, end in sorted(trips, key=lambda t: t[1]):
            # drop off everyone whose destination is at or before this pickup
            while heap and heap[0][0] <= start:
                load -= heapq.heappop(heap)[1]

            load += num
            if load > capacity:
                return False
            heapq.heappush(heap, (end, num))

        return True
```

## Complexity

- **Time:** `O(n log n)` — sorting the trips costs `O(n log n)`, and each trip is pushed to and popped from the heap at most once, each in `O(log n)`.
- **Space:** `O(n)` — the heap can hold every trip at once.

## Other Approaches

- **Difference array / prefix sum:** add `num` at index `from` and subtract it at index `to` in an array of size 1001, then sweep and check the running sum against `capacity` — Time `O(n + L)` / Space `O(L)`, where `L` is the max location (1000).
- **Sorted events:** create `(location, ±passengers)` events, sort them with drop-offs first on ties, and sweep — Time `O(n log n)` / Space `O(n)`.

## C++

```cpp
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> minHeap;
        for (int i=0; i<trips.size(); ++i) {
            int numPassengers=trips[i][0], from=trips[i][1], to=trips[i][2];
            minHeap.push({from, numPassengers});
            minHeap.push({to, -numPassengers});
        }

        int currCapacity = 0;
        while (!minHeap.empty()) {
            int currTime = minHeap.top().first;
            while (!minHeap.empty() and minHeap.top().first == currTime) {
                auto [time, numPassengers] = minHeap.top();
                minHeap.pop();
                currCapacity += numPassengers;
            }
            if (currCapacity > capacity)
                return false;
        }

        return true;
    }
};
```
