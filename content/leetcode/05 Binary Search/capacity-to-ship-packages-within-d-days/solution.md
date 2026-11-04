---
topic: "Binary Search"
difficulty: Medium
leetcode: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
neetcode: https://neetcode.io/problems/capacity-to-ship-packages-within-d-days
---
# Capacity To Ship Packages Within D Days - Solution

## Intuition

If a capacity `c` lets us ship everything within `days` days, any larger capacity also works. That monotonic property means we can binary search on the answer instead of searching over package groupings. For a fixed capacity, a greedy simulation (fill each day as much as possible, in order) tells us the minimum number of days needed.

## Approach

1. The capacity must be at least `max(weights)` (every package has to fit) and at most `sum(weights)` (everything ships in one day). Use these as the search bounds.
2. For a candidate capacity `mid`, simulate greedily: add packages to the current day until the next one would exceed `mid`, then start a new day.
3. If the simulated day count is `<= days`, `mid` is feasible, so try smaller capacities (`hi = mid`).
4. Otherwise `mid` is too small, so try larger capacities (`lo = mid + 1`).
5. When `lo == hi`, that value is the minimal feasible capacity.

## Code

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        l, r = max(weights), sum(weights)
        min_cap = r

        def canShip(cap):
            ships, curCap = 1, cap
            for w in weights:
                if curCap - w < 0:
                    ships += 1
                    curCap = cap
                curCap -= w
            return ships <= days

        while l <= r:
            cap = (l + r) // 2
            if canShip(cap):
                min_cap = min(min_cap, cap)
                r = cap - 1
            else:
                l = cap + 1

        return min_cap
```

## Complexity

- **Time:** `O(n * log(S))` — each feasibility check is `O(n)`, and the search range has size at most `S = sum(weights)`, so about `log(S)` iterations.
- **Space:** `O(1)` — only a few counters are used.

## Other Approaches

- **Linear scan over capacities:** try each capacity from `max(weights)` upward and return the first feasible one — Time `O(n * S)` / Space `O(1)`
- **Dynamic programming over partitions:** `dp[i][k]` is the minimal max-group-sum for the first `i` packages in `k` days — Time `O(n^2 * days)` / Space `O(n * days)`

## C++

```cpp
/*
    Shipping capacity at the least needs to be
    as much as the highest weight on the conveyor
    belt and at the maximum can be total of all 
    the weights on the conveyor belt. 

    
    Time Complexity -> O(nlogn)
    Space Complexity -> O(1)
*/
class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {

        int high = 0;
        int low = 0;
        
        for (int i = 0; i < weights.size(); i++) {
            high += weights[i];
            low = max(low, weights[i]);
        }
        
        int answer = high;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canShipWithinDays(weights, days, mid)) {
                high = mid - 1;
                answer = min(answer, mid);
            } else low = mid + 1;
            
        }

        return answer;
    }

private:
    bool canShipWithinDays(vector<int>&weights, int days, int max) {
        int sum = 0;
        
        for (int i = 0; i < weights.size() - 1; i++) {
            sum += weights[i];
            
            if (sum + weights[i + 1] > max) {
                sum = 0;
                days--;
            }
        }

        return days > 0;
    }
};
```
