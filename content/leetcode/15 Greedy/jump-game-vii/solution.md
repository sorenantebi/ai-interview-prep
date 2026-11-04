---
topic: "Greedy"
difficulty: Medium
leetcode: https://leetcode.com/problems/jump-game-vii/
neetcode: https://neetcode.io/problems/jump-game-vii
---
# Jump Game VII - Solution

## Intuition

An index `j` is reachable if `s[j] == '0'` and at least one reachable index lies in the window `[j - maxJump, j - minJump]`. Instead of rescanning that window for every `j`, keep a running count of reachable indices inside it and slide it as `j` advances.

## Approach

1. Create a boolean array `reach` with `reach[0] = True`, and a counter `window` of reachable indices in the current window.
2. For each `j` from `1` to `n - 1`:
   - If `j - minJump >= 0` and `reach[j - minJump]`, add one to `window` (that index just entered the window).
   - If `j - maxJump - 1 >= 0` and `reach[j - maxJump - 1]`, subtract one (that index just left the window).
   - Set `reach[j] = window > 0 and s[j] == '0'`.
3. Return `reach[n - 1]`.

## Code

```python
from typing import List, Optional

class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        reach = [False] * n
        reach[0] = True
        window = 0
        for j in range(1, n):
            if j - minJump >= 0 and reach[j - minJump]:
                window += 1
            if j - maxJump - 1 >= 0 and reach[j - maxJump - 1]:
                window -= 1
            reach[j] = window > 0 and s[j] == '0'
        return reach[n - 1]
```

## Complexity

- **Time:** `O(n)` — each index is visited once and the window update is constant time.
- **Space:** `O(n)` — the `reach` array.

## Other Approaches

- **BFS with a furthest-visited pointer:** each index is enqueued at most once by only scanning unvisited positions beyond the previous frontier — Time `O(n)` / Space `O(n)`
- **Prefix sums over reachable indices:** the window count is read from a prefix-sum array instead of a sliding counter — Time `O(n)` / Space `O(n)`
- **Brute-force DP:** for each `j`, scan the whole window for a reachable index — Time `O(n * maxJump)` / Space `O(n)`
