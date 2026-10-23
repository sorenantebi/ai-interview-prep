---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/container-with-most-water/
neetcode: https://neetcode.io/problems/max-water-container
---
# Container With Most Water - Solution

**Question:** Container With Most Water - Question · **Difficulty:** Medium

## Intuition

Start with the widest container (both ends). The area is limited by the shorter line, so moving the taller pointer inward can never help: width shrinks and the height is still capped by the same shorter line. Therefore always move the pointer at the shorter line, which is the only move that might find a taller boundary.

## Approach

1. Set `l = 0`, `r = n - 1`, `best = 0`.
2. While `l < r`:
   - Update `best` with `min(height[l], height[r]) * (r - l)`.
   - Move the pointer with the smaller height inward (either one on ties).
3. Return `best`.

## Code

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        res = 0

        while l < r:
            res = max(res, min(height[l], height[r]) * (r - l))
            if height[l] < height[r]:
                l += 1
            elif height[r] <= height[l]:
                r -= 1
            
        return res
```

## Complexity

- **Time:** `O(n)` — pointers converge in at most `n - 1` steps.
- **Space:** `O(1)` — constant variables.

## Other Approaches

- **Brute force:** evaluate every pair `(i, j)` — Time `O(n^2)`, Space `O(1)`.

## Key Takeaway

Greedy two pointers work when you can prove that one side is "dominated" and can be discarded: here, the shorter line can never form a larger container with any closer partner.
