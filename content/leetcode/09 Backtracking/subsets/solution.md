---
topic: "Backtracking"
difficulty: Medium
leetcode: https://leetcode.com/problems/subsets/
neetcode: https://neetcode.io/problems/subsets
---
# Subsets - Solution

**Question:** Subsets - Question · **Difficulty:** Medium

## Intuition

Each element is independently either **in** or **out** of a subset, so the subsets are the leaves of a binary decision tree of depth `n`. Backtracking walks this tree with one shared `path` list: choose to include `nums[i]`, recurse, undo the choice, then recurse without it.

## Approach

1. Define `dfs(i)` which decides about `nums[i]` given the current `path`.
2. If `i == len(nums)`, record a copy of `path` as a subset.
3. Otherwise: append `nums[i]`, call `dfs(i + 1)`, pop it (backtrack), and call `dfs(i + 1)` again to skip it.
4. Start with `dfs(0)` and return the collected subsets.

## Code

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []

        subset = []

        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            # decision to include nums[i]
            subset.append(nums[i])
            dfs(i + 1)
            # decision NOT to include nums[i]
            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res
```

## Complexity

- **Time:** `O(n * 2^n)` — `2^n` subsets, each copied in `O(n)`.
- **Space:** `O(n)` recursion stack and path (output of size `O(n * 2^n)` not counted).

## Other Approaches

- **Iterative cascading:** start with `[[]]`; for each number, append it to a copy of every existing subset — Time `O(n * 2^n)`, Space same output.
- **Bitmask enumeration:** for `mask` in `0..2^n - 1`, include `nums[j]` when bit `j` is set — Time `O(n * 2^n)`, Space `O(1)` extra.

## Key Takeaway

The include/exclude backtracking template (append, recurse, pop, recurse) is the foundation for subsets, combinations, and many "choose some items" problems.
