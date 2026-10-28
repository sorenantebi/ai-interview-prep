---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/maximum-product-subarray/
neetcode: https://neetcode.io/problems/maximum-product-subarray
---
# Maximum Product Subarray - Solution

**Question:** Maximum Product Subarray - Question · **Difficulty:** Medium

## Intuition

A negative number turns the smallest (most negative) product into the largest one, so tracking only the running maximum (as in Kadane's) isn't enough. Track both the **maximum and minimum** product of a subarray ending at the current index; the new values come from `x`, `x * max`, or `x * min`.

## Approach

1. Initialise `cur_max = cur_min = best = nums[0]`.
2. For each subsequent `x`, compute the candidates `x`, `x * cur_max`, `x * cur_min`.
3. `cur_max = max(candidates)`, `cur_min = min(candidates)` (computed from the old values simultaneously).
4. Update `best = max(best, cur_max)`; return `best`.

## Code

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # O(n)/O(1) : Time/Memory
        res = nums[0]
        curMin, curMax = 1, 1

        for n in nums:

            tmp = curMax * n
            curMax = max(n * curMax, n * curMin, n)
            curMin = min(tmp, n * curMin, n)
            res = max(res, curMax)
        return res
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — three running values.

## Other Approaches

- **Prefix/suffix products:** max over running products from the left and from the right, resetting to 1 after a zero — Time `O(n)`, Space `O(1)`.
- **Brute force:** product of every subarray — Time `O(n^2)`, Space `O(1)`.

## Key Takeaway

When sign flips can swap the best and worst, carry both the running max and running min (Kadane's variant for products).

## C++

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int res = nums[0];
        int curMin = 1, curMax = 1;
        
        for(int i = 0; i < nums.size(); i++)
        {
            int n = nums[i];
                
            int tmp = curMax * n;
            curMax = max(max(n * curMax, n * curMin), n);
            curMin = min(min(tmp, n * curMin), n);
            res = max(res, curMax);
        }
        
        return res;
    }
};
```
