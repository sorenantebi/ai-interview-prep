---
topic: "1-D Dynamic Programming"
difficulty: Medium
leetcode: https://leetcode.com/problems/longest-increasing-subsequence/
neetcode: https://neetcode.io/problems/longest-increasing-subsequence
---
# Longest Increasing Subsequence - Solution

**Question:** Longest Increasing Subsequence - Question · **Difficulty:** Medium

## Intuition

Maintain `tails`, where `tails[L - 1]` is the smallest possible last value of an increasing subsequence of length `L` seen so far. `tails` is always sorted, so for each new number we binary-search the first tail `>= x` and replace it (a smaller tail is never worse), or append `x` if it extends the longest one. The final length of `tails` is the answer.

## Approach

1. `tails = []`.
2. For each `x`: `i = bisect_left(tails, x)`. If `i == len(tails)`, append `x`; else set `tails[i] = x`.
3. Return `len(tails)`.

## Code

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        LIS = [1] * len(nums)

        for i in range(len(nums) - 1, -1, -1):
            for j in range(i + 1, len(nums)):
                if nums[i] < nums[j]:
                    LIS[i] = max(LIS[i], 1 + LIS[j])
        return max(LIS)
```

## Complexity

- **Time:** `O(n log n)` — one binary search per element.
- **Space:** `O(n)` — the `tails` array.

## Other Approaches

- **Quadratic DP:** `dp[i] = 1 + max(dp[j])` over `j < i` with `nums[j] < nums[i]` — Time `O(n^2)`, Space `O(n)`.

## Key Takeaway

Patience sorting: keep the smallest tail for each length and binary search into it; `bisect_left` for strictly increasing, `bisect_right` for non-decreasing. Note `tails` itself is not necessarily a valid subsequence.
