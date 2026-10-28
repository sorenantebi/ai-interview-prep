---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/house-robber-ii/
neetcode: https://neetcode.io/problems/house-robber-ii
---
# House Robber II - Solution

**Question:** House Robber II - Question · **Difficulty:** Medium

## Intuition

The circle only adds one constraint: you can't take both the first and the last house. So at least one of them is excluded — solve the linear House Robber on `nums[1:]` and on `nums[:-1]` and take the better result. A single house is a special case (both slices would be empty).

## Approach

1. If there is one house, return its value.
2. Define the linear helper `rob_line(arr)` with the rolling `max(skip, take)` DP.
3. Return `max(rob_line(nums[:-1]), rob_line(nums[1:]))`.

## Code

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        return max(nums[0], self.helper(nums[1:]), self.helper(nums[:-1]))

    def helper(self, nums):
        rob1, rob2 = 0, 0

        for n in nums:
            newRob = max(rob1 + n, rob2)
            rob1 = rob2
            rob2 = newRob
        return rob2
```

## Complexity

- **Time:** `O(n)` — two linear passes.
- **Space:** `O(n)` for the slices (`O(1)` if you pass index ranges instead).

## Other Approaches

- **Memoised recursion with a "took first house" flag:** state `(i, took_first)` — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Break a circular constraint by splitting into a few linear cases (exclude the first element / exclude the last) and reuse the linear solution.

## C++

```cpp
/*
    Given int array in a circle, return max amount can rob (can't rob adj houses)
    Ex. nums = [2,3,2] -> 3, can't rob house 1 & 3 b/c circular adj, so rob 2

    Recursion w/ memo -> DP, rob either 2 away + here, or 1 away, try both ranges
    Recurrence relation: robFrom[i] = max(robFrom[i-2] + nums[i], robFrom[i-1])

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        
        if (n == 1) {
            return nums[0];
        }
        
        int range1 = robber(nums, 0, n - 2);
        int range2 = robber(nums, 1, n - 1);
        
        return max(range1, range2);
    }
private:
    int robber(vector<int>& nums, int start, int end) {
        int prev = 0;
        int curr = 0;
        int next = 0;
        
        for (int i = start; i <= end; i++) {
            next = max(prev + nums[i], curr);
            prev = curr;
            curr = next;
        }
        
        return curr;
    }
};
```
