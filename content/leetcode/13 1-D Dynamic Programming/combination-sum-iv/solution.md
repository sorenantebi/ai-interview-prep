---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/combination-sum-iv/
neetcode: https://neetcode.io/problems/combination-sum-iv
---
# Combination Sum IV - Solution

## Intuition

Since order matters, the count of sequences summing to `t` depends on the last number chosen. If the last number is `n`, the rest forms a sequence summing to `t - n`. Summing over all choices of `n` gives a simple recurrence on smaller targets.

## Approach

1. Let `dp[t]` be the number of ordered sequences from `nums` that sum to `t`.
2. Set `dp[0] = 1` (the empty sequence).
3. For each `t` from 1 to `target`, add `dp[t - n]` for every `n` in `nums` with `n <= t`.
4. Return `dp[target]`.

The outer loop over targets and inner loop over numbers is what makes different orderings count separately.

## Code

```python
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        cache = {0: 1}

        for total in range(1, target + 1):
            cache[total] = 0
            for n in nums:
                cache[total] += cache.get(total - n, 0)
        return cache[target]

        def dfs(total):
            if total == target:
                return 1
            if total > target:
                return 0
            if total in cache:
                return cache[total]

            cache[total] = 0
            for n in nums:
                cache[total] += dfs(total + n)
            return cache[total]

        return dfs(0)
```

## Complexity

- **Time:** `O(target * len(nums))` — each of the `target` states loops over all numbers.
- **Space:** `O(target)` — the `dp` array.

## Other Approaches

- **Top-down memoization:** recurse on the remaining target with a cache — Time `O(target * len(nums))` / Space `O(target)`
- **Brute-force recursion:** enumerate every sequence without caching — Time exponential / Space `O(target)` recursion depth

## C++

```cpp
/*
    Given an array of distinct integers nums and a target integer 'target', 
    return the number of possible combinations that add up to target.
    
    Ex. nums = [1,2,3] target = 4
    Possible Combinations: (1,1,1,1) (1,1,2) (1,2,1) (1,3) (2,1,1,)
    (2,2) (3,1). 
    So, total number of combinations possible is 7.

    Time: O(n * m)
    Space: O(m)
*/

class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
    sort(nums.begin(), nums.end());
    vector<unsigned int> dp(target+1, 0);
    dp[0] = 1;
    for(int total=1; total<=target; total++) {
        for(int i=0; i<nums.size(); i++) {
            if(nums[i] <= total) dp[total] += dp[total - nums[i]];
            else break;
        }
    }
    return dp[target];
    }
};
```
