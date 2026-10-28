---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/partition-equal-subset-sum/
neetcode: https://neetcode.io/problems/partition-equal-subset-sum
---
# Partition Equal Subset Sum - Solution

**Question:** Partition Equal Subset Sum - Question · **Difficulty:** Medium

## Intuition

Equal halves exist iff the total is even and some subset sums to `total / 2`. That is 0/1 knapsack feasibility: `dp[t]` = "some subset of the items seen so far sums to `t`". Iterating `t` **downward** for each item ensures each number is used at most once.

## Approach

1. If `sum(nums)` is odd, return `False`. Let `target = sum // 2`.
2. `dp = [True] + [False] * target`.
3. For each `x`, for `t` from `target` down to `x`: `dp[t] = dp[t] or dp[t - x]`.
4. Return `dp[target]` (you may early-exit as soon as it becomes true).

## Code

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2:
            return False

        dp = set()
        dp.add(0)
        target = sum(nums) // 2

        for i in range(len(nums) - 1, -1, -1):
            nextDP = set()
            for t in dp:
                if (t + nums[i]) == target:
                    return True
                nextDP.add(t + nums[i])
                nextDP.add(t)
            dp = nextDP
        return False
```

## Complexity

- **Time:** `O(n · target)` — `target <= sum/2 <= 10^4`, so about `2 · 10^6` steps.
- **Space:** `O(target)` — a 1-D DP array.

## Other Approaches

- **Set of reachable sums:** `sums |= {s + x for s in sums}` — Time `O(n · target)`, Space `O(target)`.
- **Bitset trick:** `bits |= bits << x` on a Python int, check bit `target` — same complexity but very fast in practice.

## Key Takeaway

"Split into two equal-sum halves" reduces to subset-sum for `total/2`; 0/1 knapsack iterates capacity backwards, unbounded knapsack forwards.

## C++

```cpp
/*
    Given non-empty, non-negative integer array nums, find if:
    Can be partitionined into 2 subsets such that sums are equal
    Ex. nums = [1,5,11,5] -> true, [1,5,5] & [11], both add to 11

    Maintain DP set, for each num, check if num in set + curr = target
    If not, add curr to every num in set we checked & iterate

    Time: O(n x sum(nums))
    Space: O(sum(nums))
*/

class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int target = 0;
        for (int i = 0; i < nums.size(); i++) {
            target += nums[i];
        }
        if (target % 2 != 0) {
            return false;
        }
        target /= 2;
        
        unordered_set<int> dp;
        dp.insert(0);
        
        for (int i = 0; i < nums.size(); i++) {
            unordered_set<int> dpNext;
            for (auto it = dp.begin(); it != dp.end(); it++) {
                if (*it + nums[i] == target) {
                    return true;
                }
                dpNext.insert(*it + nums[i]);
                dpNext.insert(*it);
            }
            dp = dpNext;
        }
        
        return false;
    }
};
```
