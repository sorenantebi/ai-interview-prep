---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/car-fleet/
neetcode: https://neetcode.io/problems/car-fleet
---
# Car Fleet - Solution

**Question:** Car Fleet - Question · **Difficulty:** Medium

## Intuition

Process cars from closest to the target to farthest. Each car's solo arrival time is `(target - position) / speed`. If a car behind would arrive no later than the fleet directly ahead of it, it catches that fleet and merges; otherwise it arrives strictly later and starts a new fleet that becomes the new blocker.

## Approach

1. Pair each position with its speed and sort by position descending.
2. Compute each car's arrival time `(target - p) / s`.
3. Keep a stack of fleet arrival times. For each car, if the stack is empty or its time is greater than the top, push it (new fleet); otherwise it merges into the fleet ahead.
4. Return the stack size.

## Code

```python
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = [(p, s) for p, s in zip(position, speed)]
        pair.sort(reverse=True)
        stack = []
        for p, s in pair:  # Reverse Sorted Order
            stack.append((target - p) / s)
            if len(stack) >= 2 and stack[-1] <= stack[-2]:
                stack.pop()
        return len(stack)
```

## Complexity

- **Time:** `O(n log n)` — dominated by sorting.
- **Space:** `O(n)` — the sorted pairs and the stack.

## Other Approaches

- **Single variable instead of stack:** only the last fleet's time matters, so track `slowest` time and count increments when `t > slowest` — Time `O(n log n)`, Space `O(n)` for sorting (O(1) extra otherwise).

## Key Takeaway

Sort by position and reason from the front: a car's fate depends only on the fleet immediately ahead, compared via arrival times rather than simulating motion.

## C++

```cpp
/*
    n cars 1 road, diff pos/speeds, faster cars slow down -> car fleet, return # fleets
    Ex. target = 12, pos = [10,8,0,5,3], speeds = [2,4,1,1,3] -> 3 (10 & 8, 0, 5 & 3)

    Sort by start pos, calculate time for each car to finish, loop backwards
    If car behind finishes faster then catches up to fleet, else creates new fleet

    Time: O(n log n)
    Speed: O(n)
*/

class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        
        vector<pair<int, double>> cars;
        for (int i = 0; i < n; i++) {
            double time = (double) (target - position[i]) / speed[i];
            cars.push_back({position[i], time});
        }
        sort(cars.begin(), cars.end());
        
        double maxTime = 0.0;
        int result = 0;
        
        for (int i = n - 1; i >= 0; i--) {
            double time = cars[i].second;
            if (time > maxTime) {
                maxTime = time;
                result++;
            }
        }
        
        return result;
    }
};
```
