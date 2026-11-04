---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/perfect-squares/
neetcode: https://neetcode.io/problems/perfect-squares
---
# Perfect Squares - Solution

## Intuition

This is an unbounded coin-change problem where the "coins" are the perfect squares up to `n`, and we want the minimum number of coins that make exactly `n`. The best answer for `i` is one square plus the best answer for the remainder.

## Approach

1. Let `dp[i]` be the least number of perfect squares summing to `i`, with `dp[0] = 0`.
2. For each `i` from `1` to `n`, try every square `s = j * j <= i` and set `dp[i] = min(dp[i], dp[i - s] + 1)`.
3. Since `1` is a perfect square, every `i` is reachable, so the initial value for `dp[i]` can simply be `i` (all ones).
4. Return `dp[n]`.

## Code

```python
from typing import List, Optional

class Solution:
    def numSquares(self, n: int) -> int:
        dp = list(range(n + 1))  # worst case: i copies of 1
        for i in range(2, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1
        return dp[n]
```

## Complexity

- **Time:** `O(n * sqrt(n))` — for each of the `n` values we try up to `sqrt(n)` squares.
- **Space:** `O(n)` — the `dp` array.

## Other Approaches

- **BFS over remainders:** treat each remainder as a node and subtract squares level by level; the first level reaching 0 is the answer — Time `O(n * sqrt(n))` / Space `O(n)`
- **Lagrange's four-square theorem:** the answer is always 1 to 4; check for a perfect square, then the sum of two squares, then the form `4^a(8b+7)` (answer 4), otherwise 3 — Time `O(sqrt(n))` / Space `O(1)`

## C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

/*
    problem link: https://leetcode.com/problems/perfect-squares/description/
    Given an integer n, return the least number of perfect square numbers that sum to n.

    A perfect square is an integer that is the square of an integer; in other words, it is the
    product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3
    and 11 are not.

    Example 1:

    Input: n = 12
    Output: 3
    Explanation: 12 = 4 + 4 + 4.

    Example 2:

    Input: n = 13
    Output: 2
    Explanation: 13 = 4 + 9.
*/

class Solution {
public:
    // Similar to Coin Change problem
    int numSquares(int n) {
        // Create the dp array to eliminate the cache
        vector<int> dp(n + 1);
        // Initialize the firest element of dp as 0
        dp[0] = 0;
        for (int i = 1; i <= n; i++)
        {
            // Biggest is when all square is 1^2 that is when dp[i] = i
            dp[i] = i;
            for (int j = 1; j * j <= i; j++) {
                // Update the value of dp[i]
                dp[i] = min(dp[i], dp[i - j * j] + 1);
            }
        }
        // Return the value of dp[n]
        return dp[n];
    }
};
```
