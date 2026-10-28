---
topic: "1-D Dynamic Programming"
difficulty: Easy
leetcode: https://leetcode.com/problems/climbing-stairs/
neetcode: https://neetcode.io/problems/climbing-stairs
---
# Climbing Stairs - Solution

**Question:** Climbing Stairs - Question · **Difficulty:** Easy

## Intuition

The last move to step `n` is either a 1-step from `n - 1` or a 2-step from `n - 2`, so `ways(n) = ways(n - 1) + ways(n - 2)` — the Fibonacci recurrence. Only the previous two values are needed, so two variables suffice.

## Approach

1. Start with `prev = ways(0) = 1` and `cur = ways(1) = 1`.
2. For each step from 2 to `n`, set `prev, cur = cur, prev + cur` to slide the window forward.
3. Return `cur`.

## Code

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3:
            return n
        n1, n2 = 2, 3

        for i in range(4, n + 1):
            temp = n1 + n2
            n1 = n2
            n2 = temp
        return n2
```

## Complexity

- **Time:** `O(n)` — one pass.
- **Space:** `O(1)` — two variables.

## Other Approaches

- **Memoised recursion:** `f(n) = f(n-1) + f(n-2)` with a cache — Time `O(n)`, Space `O(n)`.
- **Matrix exponentiation / Binet's formula:** Fibonacci in `O(log n)` time, `O(1)` space.

## Key Takeaway

"Count the ways to reach a state from a few previous states" is a 1-D DP; when it only looks back a fixed number of steps, roll it into constant space.

## C++

```cpp
/*
    Climbing stairs, either 1 or 2 steps, distinct ways to reach top
    Ex. n = 2 -> 2 (1 + 1, 2), n = 3 -> 3 (1 + 1 + 1, 1 + 2, 2 + 1)

    Recursion w/ memoization -> DP, why DP? Optimal substructure
    Recurrence relation: dp[i] = dp[i - 1] + dp[i - 2]
    Reach ith step in 2 ways: 1) 1 step from i-1, 2) 2 steps from i-2

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int climbStairs(int n) {
        if (n == 1) {
            return 1;
        }
        if (n == 2) {
            return 2;
        }
        
        int first = 1;
        int second = 2;
        
        int result = 0;
        
        for (int i = 2; i < n; i++) {
            result = first + second;
            first = second;
            second = result;
        }
        
        return result;
    }
};
```
