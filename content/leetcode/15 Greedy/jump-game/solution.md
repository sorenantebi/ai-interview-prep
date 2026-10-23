---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/jump-game/
neetcode: https://neetcode.io/problems/jump-game
---
# Jump Game - Solution

**Question:** Jump Game - Question · **Difficulty:** Medium

## Intuition

Track the farthest index reachable so far. Scanning left to right, if the current index is beyond that frontier we are stuck; otherwise extend the frontier with `i + nums[i]`. (Equivalently, walk backwards moving a "goal" index left whenever `i + nums[i] >= goal`.)

## Approach

1. `reach = 0`.
2. For each index `i`: if `i > reach`, return `False`; else `reach = max(reach, i + nums[i])`; if `reach >= n - 1`, return `True` early.
3. Return `True`.

## Code

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1

        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0
```

## Complexity

- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — one variable.

## Other Approaches

- **Backward goal shifting:** from the end, set `goal = i` whenever `i + nums[i] >= goal`; answer is `goal == 0` — Time `O(n)`, Space `O(1)`.
- **DP over reachability:** mark each reachable index and propagate up to `nums[i]` steps — Time `O(n * max(nums))`, Space `O(n)`.

## Key Takeaway

Reachability on an array with "up to k steps" jumps collapses to tracking a single max-reach frontier.
