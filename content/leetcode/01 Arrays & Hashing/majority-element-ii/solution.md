---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/majority-element-ii/
neetcode: https://neetcode.io/problems/majority-element-ii
---
# Majority Element II - Solution

## Intuition

At most two distinct values can appear more than `n / 3` times, since three such values would need more than `n` elements in total. This generalizes the Boyer-Moore majority vote: keep two candidates with counters. When a third distinct value shows up, it cancels one occurrence of each candidate. Any true answer survives the cancellations, so a second pass is enough to verify the candidates.

## Approach

1. Keep two candidates `c1`, `c2` and counters `n1`, `n2`, all starting at zero.
2. For each number: if it equals a candidate, increment that counter; else if a counter is zero, take the number as that candidate with count 1; else decrement both counters.
3. Count the actual occurrences of both candidates in a second pass.
4. Return the candidates whose count exceeds `len(nums) // 3`.

## Code

```python
from typing import List, Optional

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        c1, c2 = 0, 1
        n1, n2 = 0, 0
        for x in nums:
            if x == c1:
                n1 += 1
            elif x == c2:
                n2 += 1
            elif n1 == 0:
                c1, n1 = x, 1
            elif n2 == 0:
                c2, n2 = x, 1
            else:
                n1 -= 1
                n2 -= 1

        # candidates are only possible answers; verify them
        threshold = len(nums) // 3
        res = []
        if nums.count(c1) > threshold:
            res.append(c1)
        if nums.count(c2) > threshold:
            res.append(c2)
        return res
```

## Complexity

- **Time:** `O(n)` — two linear passes over the array.
- **Space:** `O(1)` — only two candidates and two counters are stored.

## Other Approaches

- **Hash map counting:** count every value and keep those above `n // 3` — Time `O(n)` / Space `O(n)`
- **Sorting:** sort and scan runs of equal values — Time `O(n log n)` / Space `O(1)` or `O(n)` depending on the sort
