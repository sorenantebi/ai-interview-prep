---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/product-of-array-except-self/
neetcode: https://neetcode.io/problems/products-of-array-discluding-self
---
# Product of Array Except Self - Solution

**Question:** Product of Array Except Self - Question · **Difficulty:** Medium

## Intuition

The product of everything except `nums[i]` is (product of everything to its left) × (product of everything to its right). We can store the left prefix products in the output array in one pass, then sweep from the right with a running suffix product and multiply it in, all without division.

## Approach

1. Initialize `answer = [1] * n`.
2. Left pass: keep `prefix = 1`; for each `i`, set `answer[i] = prefix`, then `prefix *= nums[i]`.
3. Right pass: keep `suffix = 1`; for `i` from `n - 1` down to `0`, do `answer[i] *= suffix`, then `suffix *= nums[i]`.
4. Return `answer`.

## Code

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * (len(nums))

        for i in range(1, len(nums)):
            res[i] = res[i-1] * nums[i-1]
        postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        return res
```

## Complexity

- **Time:** `O(n)` — two linear passes.
- **Space:** `O(1)` extra — only `prefix`/`suffix` scalars; the output array is not counted.

## Other Approaches

- **Separate prefix and suffix arrays:** build both arrays then multiply element-wise — Time `O(n)`, Space `O(n)`.
- **Division with zero counting:** total product / `nums[i]`, special-casing one or more zeros — Time `O(n)`, Space `O(1)`, but disallowed by the problem.

## Key Takeaway

"Everything except index i" problems decompose into prefix and suffix aggregates; reuse the output array to hold one of them for `O(1)` extra space.
