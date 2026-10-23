---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/jump-game-ii/
neetcode: https://neetcode.io/problems/jump-game-ii
---
# Jump Game II - Solution

**Question:** Jump Game II - Question · **Difficulty:** Medium

## Intuition

Think of it as BFS over index ranges: all indices reachable with `k` jumps form a contiguous window. The next window spans from just past the current one up to the farthest `i + nums[i]` over the current window. Count how many windows it takes to cover the last index.

## Approach

1. `jumps = 0`, `cur_end = 0` (end of the current window), `farthest = 0`.
2. For `i` from 0 to `n - 2`:
   - `farthest = max(farthest, i + nums[i])`.
   - If `i == cur_end`: we must jump — `jumps += 1`, `cur_end = farthest`.
3. Return `jumps`.

## Code

```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        l, r = 0, 0
        res = 0
        while r < (len(nums) - 1):
            maxJump = 0
            for i in range(l, r + 1):
                maxJump = max(maxJump, i + nums[i])
            l = r + 1
            r = maxJump
            res += 1
        return res
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — three counters.

## Other Approaches

- **DP:** `dp[j] = min(dp[i] + 1)` for every `i` that can reach `j` — Time `O(n^2)`, Space `O(n)`.
- **Explicit BFS with a queue:** nodes are indices, edges are jumps — Time `O(n * max(nums))`, Space `O(n)`.

## Key Takeaway

Minimum jumps = number of BFS levels, and in a 1-D jump array each level is a contiguous window, so BFS reduces to a greedy window scan.
