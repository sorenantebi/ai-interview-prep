---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/decode-ways/
neetcode: https://neetcode.io/problems/decode-ways
---
# Decode Ways - Solution

**Question:** Decode Ways - Question · **Difficulty:** Medium

## Intuition

Let `dp[i]` be the number of ways to decode the prefix `s[:i]`. The last piece is either one digit (valid if it isn't `'0'`) or two digits (valid if between `10` and `26`), so `dp[i] = dp[i-1]·[one-digit ok] + dp[i-2]·[two-digit ok]`. Only two previous values are needed.

## Approach

1. `prev2 = dp[i-2]`, `prev1 = dp[i-1]`; start with `dp[0] = 1` (empty prefix) so `prev1 = 1`, `prev2 = 0`.
2. For each position `i` (1-based), `cur = 0`; if `s[i-1] != '0'` add `prev1`; if `i >= 2` and `10 <= int(s[i-2:i]) <= 26` add `prev2`.
3. Shift and continue; return `prev1`.

## Code

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        # Memoization
        dp = {len(s): 1}

        def dfs(i):
            if i in dp:
                return dp[i]
            if s[i] == "0":
                return 0

            res = dfs(i + 1)
            if i + 1 < len(s) and (
                s[i] == "1" or s[i] == "2" and s[i + 1] in "0123456"
            ):
                res += dfs(i + 2)
            dp[i] = res
            return res

        return dfs(0)

        # Dynamic Programming
        dp = {len(s): 1}
        for i in range(len(s) - 1, -1, -1):
            if s[i] == "0":
                dp[i] = 0
            else:
                dp[i] = dp[i + 1]

            if i + 1 < len(s) and (
                s[i] == "1" or s[i] == "2" and s[i + 1] in "0123456"
            ):
                dp[i] += dp[i + 2]
        return dp[0]
```

## Complexity

- **Time:** `O(n)` — one pass with constant work per character.
- **Space:** `O(1)` — two rolling values.

## Other Approaches

- **Memoised recursion:** `f(i)` = ways to decode `s[i:]`, branching on one or two digits — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Decode Ways is Climbing Stairs with validity checks on each step; zeros are the trap — a `'0'` can only be the second digit of `10` or `20`.
