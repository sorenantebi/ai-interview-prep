---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber/
neetcode: https://neetcode.io/problems/house-robber
---
# House Robber - Solution

**Question:** House Robber - Question · **Difficulty:** Medium

## Intuition

At each house you either skip it (keep the best total up to the previous house) or take it (best total up to two houses back plus this house). So `best(i) = max(best(i - 1), best(i - 2) + nums[i])`, which only needs two rolling values.

## Approach

1. `prev2 = best up to i - 2`, `prev1 = best up to i - 1`, both 0.
2. For each value `x`: `cur = max(prev1, prev2 + x)`; shift `prev2, prev1 = prev1, cur`.
3. Return `prev1`.

## Code

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        rob1, rob2 = 0, 0

        for n in nums:
            temp = max(n + rob1, rob2)
            rob1 = rob2
            rob2 = temp
        return rob2
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — two variables.

## Other Approaches

- **Memoised recursion:** `f(i) = max(f(i+1), nums[i] + f(i+2))` — Time `O(n)`, Space `O(n)`.
- **Brute force:** try all non-adjacent subsets — Time `O(2^n)`, Space `O(n)`.

## Key Takeaway

"Take it or skip it with an adjacency restriction" is the canonical `max(skip, take + dp[i-2])` DP; it reappears in House Robber II, Delete and Earn, and many others.

## C++

```cpp
/*
    Given int array, return max amount can rob (can't rob adjacent houses)
    Ex. nums = [1,2,3,1] -> 4, rob house 1 then house 3: 1 + 3 = 4

    Recursion w/ memoization -> DP, rob either 2 away + here, or 1 away
    Recurrence relation: robFrom[i] = max(robFrom[i-2] + nums[i], robFrom[i-1])

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int rob(vector<int>& nums) {
        int prev = 0;
        int curr = 0;
        int next = 0;
        
        for (int i = 0; i < nums.size(); i++) {
            next = max(prev + nums[i], curr);
            prev = curr;
            curr = next;
        }
        
        return curr;
    }
};
```
