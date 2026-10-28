---
topic: "2-D Dynamic Programming"
difficulty: Hard
leetcode: https://leetcode.com/problems/burst-balloons/
neetcode: https://neetcode.io/problems/burst-balloons
---
# Burst Balloons - Solution

**Question:** Burst Balloons - Question · **Difficulty:** Hard

## Intuition

Choosing which balloon to burst *first* splits nothing cleanly, because neighbours change. Instead think about which balloon in an interval is burst **last**: if `k` is the last one in the open interval `(l, r)`, its neighbours at that moment are exactly `l` and `r`, and the left part `(l, k)` and right part `(k, r)` are independent subproblems. Pad the array with `1`s on both ends.

## Approach

1. `vals = [1] + nums + [1]`, `N = len(vals)`.
2. `dp[l][r]` = max coins from bursting every balloon strictly between `l` and `r`.
3. For gap sizes from 2 to `N - 1`, for each `l` with `r = l + gap`:
   `dp[l][r] = max(dp[l][k] + vals[l] * vals[k] * vals[r] + dp[k][r])` over `l < k < r`.
4. Return `dp[0][N-1]`.

## Code

```python
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        cache = {}
        nums = [1] + nums + [1]

        for offset in range(2, len(nums)):
            for left in range(len(nums) - offset):
                right = left + offset
                for pivot in range(left + 1, right):
                    coins = nums[left] * nums[pivot] * nums[right]
                    coins += cache.get((left, pivot), 0) + cache.get((pivot, right), 0)
                    cache[(left, right)] = max(coins, cache.get((left, right), 0))
        return cache.get((0, len(nums) - 1), 0)
```

## Complexity

- **Time:** `O(n^3)` — `O(n^2)` intervals, each trying `O(n)` split points.
- **Space:** `O(n^2)` — the interval DP table.

## Other Approaches

- **Memoized recursion on `(l, r)`:** same "last balloon" recurrence top-down — Time `O(n^3)`, Space `O(n^2)`.
- **Brute force over burst orders:** try all `n!` permutations — Time `O(n! * n)`, Space `O(n)`.

## Key Takeaway

For interval DPs where removing an element changes adjacency, reason about the element processed **last** in the interval — its boundaries are then fixed and the subproblems become independent.

## C++

```cpp
/*
    Given array of balloons w/ coins, if burst ith, get (i-1) + i + (i+1) coins
    Return max coins can collect by bursting the balloons wisely

    DP to return max coins obtainable in each interval [left, right]
    Divide & conquer left & right depends on previous bursts, so think backwards
    Instead of which one to burst first, need to think which one to burst last

    Time: O(n^3) -> O(n^2) states, for each states, determining max coins is O(n)
    Space: O(n^2) -> O(n^2) to store all states
*/

class Solution {
public:
    int maxCoins(vector<int>& nums) {
        // add 1 before & after nums
        nums.insert(nums.begin(), 1);
        nums.insert(nums.end(), 1);
        int n = nums.size();
        
        // cache results of dp
        vector<vector<int>> memo(n, vector<int>(n, 0));
        
        // 1 & n - 2 since we can't burst our fake balloons
        return dp(nums, memo, 1, n - 2);
    }
private:
    int dp(vector<int>& nums, vector<vector<int>>& memo, int left, int right) {
        // base case interval is empty, yields 0 coins
        if (right - left < 0) {
            return 0;
        }
        
        // we've already seen this, return from cache
        if (memo[left][right] > 0) {
            return memo[left][right];
        }
        
        // find the last burst in nums[left]...nums[right]
        int result = 0;
        for (int i = left; i <= right; i++) {
            // nums[i] is the last burst
            int curr = nums[left - 1] * nums[i] * nums[right + 1];
            // nums[i] is fixed, recursively call left & right sides
            int remaining = dp(nums, memo, left, i - 1) + dp(nums, memo, i + 1, right);
            result = max(result, curr + remaining);
        }
        // add to cache
        memo[left][right] = result;
        return result;
    }
};
```
