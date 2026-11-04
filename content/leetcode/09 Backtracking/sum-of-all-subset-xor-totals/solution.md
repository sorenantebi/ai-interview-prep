---
topic: "Backtracking"
difficulty: Easy
leetcode: https://leetcode.com/problems/sum-of-all-subset-xor-totals/
neetcode: https://neetcode.io/problems/sum-of-all-subset-xor-totals
---
# Sum of All Subset XOR Totals - Solution

## Intuition

Consider each bit position on its own. If at least one number has that bit set, then exactly half of all subsets (2^(n-1) of them) have that bit set in their XOR total. If no number has the bit, it never appears. So the answer is the OR of all numbers, multiplied by 2^(n-1).

## Approach

1. Compute the bitwise OR of every element in `nums`.
2. Multiply it by `2^(n-1)`, where `n = len(nums)`.
3. Return the result.

## Code

```python
from typing import List, Optional

class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        bits = 0
        for x in nums:
            bits |= x
        # each set bit appears in exactly half of the 2^n subsets
        return bits << (len(nums) - 1)
```

## Complexity

- **Time:** `O(n)` — a single pass to compute the OR.
- **Space:** `O(1)` — only a few integer variables are used.

## Other Approaches

- **Backtracking (include/exclude):** recurse over each element, either taking it into the running XOR or skipping it, and sum the values at the leaves — Time `O(2^n)` / Space `O(n)`
- **Bitmask enumeration:** iterate over all masks from `0` to `2^n - 1` and XOR the selected elements — Time `O(n · 2^n)` / Space `O(1)`
