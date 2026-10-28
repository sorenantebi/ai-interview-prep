---
topic: "2-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/coin-change-ii/
neetcode: https://neetcode.io/problems/coin-change-ii
---
# Coin Change II - Solution

**Question:** Coin Change II - Question · **Difficulty:** Medium

## Intuition

This is the unbounded knapsack counting problem. To count combinations (not permutations), process coins one at a time in the **outer** loop: `dp[a]` = number of ways to make `a` using only the coins seen so far. Adding coin `c` lets every amount `a` also be formed as `(a - c) + c`.

## Approach

1. `dp = [0] * (amount + 1)`, `dp[0] = 1`.
2. For each coin `c`, for `a` from `c` up to `amount` (ascending, so the coin can be reused): `dp[a] += dp[a - c]`.
3. Return `dp[amount]`.

## Code

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        # MEMOIZATION
        # Time: O(n*m)
        # Memory: O(n*m)
        cache = {}

        def dfs(i, a):
            if a == amount:
                return 1
            if a > amount:
                return 0
            if i == len(coins):
                return 0
            if (i, a) in cache:
                return cache[(i, a)]

            cache[(i, a)] = dfs(i, a + coins[i]) + dfs(i + 1, a)
            return cache[(i, a)]

        return dfs(0, 0)

        # DYNAMIC PROGRAMMING
        # Time: O(n*m)
        # Memory: O(n*m)
        dp = [[0] * (len(coins) + 1) for i in range(amount + 1)]
        dp[0] = [1] * (len(coins) + 1)
        for a in range(1, amount + 1):
            for i in range(len(coins) - 1, -1, -1):
                dp[a][i] = dp[a][i + 1]
                if a - coins[i] >= 0:
                    dp[a][i] += dp[a - coins[i]][i]
        return dp[amount][0]

        # DYNAMIC PROGRAMMING
        # Time: O(n*m)
        # Memory: O(n) where n = amount
        dp = [0] * (amount + 1)
        dp[0] = 1
        for i in range(len(coins) - 1, -1, -1):
            nextDP = [0] * (amount + 1)
            nextDP[0] = 1

            for a in range(1, amount + 1):
                nextDP[a] = dp[a]
                if a - coins[i] >= 0:
                    nextDP[a] += nextDP[a - coins[i]]
            dp = nextDP
        return dp[amount]
```

## Complexity

- **Time:** `O(n * amount)` — each coin sweeps all amounts once.
- **Space:** `O(amount)` — a single 1-D table.

## Other Approaches

- **2-D DP `dp[i][a]`:** ways to make `a` with the first `i` coins — Time `O(n * amount)`, Space `O(n * amount)`.
- **Memoized DFS on `(i, remaining)`:** take coin `i` again or move to `i + 1` — Time `O(n * amount)`, Space `O(n * amount)`.

## Key Takeaway

Loop order matters in counting knapsacks: coins outer counts combinations, amounts outer counts permutations; ascending inner loop = unbounded, descending = 0/1.

## C++

```cpp
/*
    Given array of coins & an amount, return # of combos that make up this amount
    Ex. amount = 5, coins = [1,2,5] -> 4 (5, 2+2+1, 2+1+1+1, 1+1+1+1+1)

    DFS + memo, 2 choices: either try coin & stay at idx, or don't try & proceed

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int change(int amount, vector<int>& coins) {
        return dfs(amount, coins, 0, 0);
    }
private:
    // {(index, sum) -> # of combos that make up this amount}
    map<pair<int, int>, int> dp;
    
    int dfs(int amount, vector<int>& coins, int i, int sum) {
        if (sum == amount) {
            return 1;
        }
        if (sum > amount) {
            return 0;
        }
        if (i == coins.size()) {
            return 0;
        }
        if (dp.find({i, sum}) != dp.end()) {
            return dp[{i, sum}];
        }
        
        dp[{i, sum}] = dfs(amount, coins, i, sum + coins[i])
                     + dfs(amount, coins, i + 1, sum);
        
        return dp[{i, sum}];
    }
};
```
