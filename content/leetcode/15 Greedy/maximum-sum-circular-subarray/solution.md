---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/maximum-sum-circular-subarray/
neetcode: https://neetcode.io/problems/maximum-sum-circular-subarray
---
# Maximum Sum Circular Subarray - Solution

## Intuition

The best subarray is either a normal one (no wrap-around) or one that wraps around. A wrapping subarray is the whole array minus a contiguous middle segment, so its sum is `total - (sum of that middle segment)`. To maximize it, minimize the middle segment. Both cases are solved with Kadane's algorithm: one for the maximum subarray, one for the minimum subarray.

The only catch is when every element is negative: the minimum subarray would be the entire array, leaving an empty wrap-around subarray, which is not allowed. In that case the answer is just the maximum subarray.

## Approach

1. Walk through the array once, tracking `total`, the running Kadane maximum (`cur_max`) with its best (`best_max`), and the running Kadane minimum (`cur_min`) with its best (`best_min`).
2. If `best_max < 0`, all elements are negative, so return `best_max`.
3. Otherwise return `max(best_max, total - best_min)`.

## Code

```python
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        globMax, globMin = nums[0], nums[0]
        curMax, curMin = 0, 0
        total = 0
        
        for i, n in enumerate(nums):
            curMax = max(curMax + n, n)
            curMin = min(curMin + n, n)
            total += n
            globMax = max(curMax, globMax)
            globMin = min(curMin, globMin)

        return max(globMax, total - globMin) if globMax > 0 else globMax
```

## Complexity

- **Time:** `O(n)` — a single pass over the array.
- **Space:** `O(1)` — only a few running variables are kept.

## Other Approaches

- **Prefix sums + monotonic deque:** over the doubled array, find the max of `prefix[j] - prefix[i]` with window length at most `n` — Time `O(n)` / Space `O(n)`
- **Brute force:** try every start and length up to `n` with wrap-around indexing — Time `O(n^2)` / Space `O(1)`
