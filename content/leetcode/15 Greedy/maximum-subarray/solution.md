---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/maximum-subarray/
neetcode: https://neetcode.io/problems/maximum-subarray
---
# Maximum Subarray - Solution

**Question:** Maximum Subarray - Question · **Difficulty:** Medium

## Intuition

**Kadane's algorithm:** the best subarray ending at index `i` either extends the best subarray ending at `i-1` or starts fresh at `i`. A negative running sum can only hurt what follows, so drop it.

## Approach

1. `cur = best = nums[0]`.
2. For each subsequent `x`: `cur = max(x, cur + x)`; `best = max(best, cur)`.
3. Return `best`.

## Code

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        res = nums[0]

        total = 0
        for n in nums:
            total += n
            res = max(res, total)
            if total < 0:
                total = 0
        return res
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — two running values (the slice copy can be avoided with an index loop).

## Other Approaches

- **Divide and conquer:** best of left half, right half, and the best crossing sum — Time `O(n log n)`, Space `O(log n)`.
- **Prefix sums:** answer is `max(prefix[j] - min(prefix[i]) for i < j)` — Time `O(n)`, Space `O(1)`.
- **Brute force:** check all `O(n^2)` subarrays with running sums — Time `O(n^2)`, Space `O(1)`.

## Key Takeaway

Kadane's: keep the best sum ending *here*; reset when the carried sum becomes a liability. Initialise with `nums[0]` so all-negative arrays work.

## C++

```cpp
/*
    Given int array, find contiguous subarray w/ max sum
    Ex. nums = [-2,1,-3,4,-1,2,1,-5,4] -> 6, [4,-1,2,1]

    At each point, determine if it's better to add to curr sum or start over

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int curr = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            curr = max(curr + nums[i], nums[i]);
            result = max(result, curr);
        }
        
        return result;
    }
};
```
