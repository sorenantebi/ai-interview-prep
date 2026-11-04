---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/integer-break/
neetcode: https://neetcode.io/problems/integer-break
---
# Integer Break - Solution

## Intuition

The best split of `n` is built from the best splits of smaller numbers. For the first piece `j`, the remainder `n - j` is either kept whole or broken further, so we take the larger of the two options. This gives a 1-D DP over `n`.

## Approach

1. Let `dp[i]` be the maximum product obtainable by breaking `i` into at least two positive integers.
2. Base case: `dp[1] = 1` (used only as a convenience; it never beats keeping a piece whole).
3. For each `i` from 2 to `n`, try every first piece `j` from 1 to `i - 1`.
4. For each `j`, the candidate product is `j * max(i - j, dp[i - j])`: the remainder is either left whole or split further.
5. Set `dp[i]` to the best candidate; the answer is `dp[n]`.

## Code

```python
from typing import List, Optional

class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            for j in range(1, i):
                # remainder i - j is either kept whole or split further
                dp[i] = max(dp[i], j * max(i - j, dp[i - j]))
        return dp[n]
```

## Complexity

- **Time:** `O(n^2)` — for each `i` we try up to `i - 1` first pieces.
- **Space:** `O(n)` — the `dp` array of size `n + 1`.

## Other Approaches

- **Greedy / math (use 3s):** for `n <= 3` return `n - 1`; otherwise split into as many 3s as possible, using a 4 (or 2×2) if the remainder is 1, and a 2 if the remainder is 2 — Time `O(log n)` (or `O(1)` with closed-form power) / Space `O(1)`
- **Top-down memoization:** the same recurrence written recursively with a cache — Time `O(n^2)` / Space `O(n)`

## C++

```cpp
/*
Given an integer n, break it into the sum of k positive integers, where k >= 2, and maximize the product of those integers.
Return the maximum product that we can get.

Example. For n = 10, we can break it as 10 = 3 + 3 + 4. Product of these integers is 3 x 3 x 4 = 36, which is the maximum product that
	 we can get in this case. So we return 36 as the answer. 


Time: O(n^2)
Space: O(n)

*/

class Solution {
public:
    int integerBreak(int n) {
        vector<int> dp(n+1, INT_MIN);
        dp[0] = 1, dp[1] = 1;
        for(int ind=2; ind<=n; ind++) {
            for(int i=ind-1; i>=1; i--) {
                dp[ind] = max(dp[ind], i * dp[ind - i]);
            }
            if(ind < n) dp[ind] = max(dp[ind], ind);
        }
        return dp[n];
    }
};
```
