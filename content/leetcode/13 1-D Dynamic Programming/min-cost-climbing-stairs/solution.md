---
topic: "1-D Dynamic Programming"
difficulty: Easy
leetcode: https://leetcode.com/problems/min-cost-climbing-stairs/
neetcode: https://neetcode.io/problems/min-cost-climbing-stairs
---
# Min Cost Climbing Stairs - Solution

**Question:** Min Cost Climbing Stairs - Question · **Difficulty:** Easy

## Intuition

Let `dp[i]` be the minimum cost to stand on position `i` (before paying for it). You can arrive from `i - 1` (paying `cost[i - 1]`) or from `i - 2` (paying `cost[i - 2]`). Starting on 0 or 1 is free, so `dp[0] = dp[1] = 0`, and the answer is `dp[n]`.

## Approach

1. Keep two rolling values `a = dp[i - 2]`, `b = dp[i - 1]`, both 0 initially.
2. For `i` from 2 to `n`: `dp[i] = min(b + cost[i - 1], a + cost[i - 2])`; shift.
3. Return the last value.

## Code

```python
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        for i in range(len(cost) - 3, -1, -1):
            cost[i] += min(cost[i + 1], cost[i + 2])

        return min(cost[0], cost[1])
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — two rolling variables.

## Other Approaches

- **Backward in-place DP:** `cost[i] += min(cost[i+1], cost[i+2])` from the end, answer `min(cost[0], cost[1])` — Time `O(n)`, Space `O(1)` (mutates input).
- **Memoised recursion:** top-down version of the same recurrence — Time `O(n)`, Space `O(n)`.

## Key Takeaway

Define the DP state precisely (cost to *stand on* `i` vs cost *including* `i`) — off-by-one choices like where "the top" is follow directly from that definition.
