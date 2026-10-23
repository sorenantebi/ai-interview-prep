---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/single-number/
neetcode: https://neetcode.io/problems/single-number
---
# Single Number - Solution

**Question:** Single Number - Question · **Difficulty:** Easy

## Intuition

XOR is commutative and associative, `a ^ a = 0`, and `a ^ 0 = a`. If we XOR every element, each pair cancels to 0 no matter where its two copies appear, and only the unpaired value is left.

## Approach

1. Set `res = 0`.
2. XOR every number into `res`.
3. Return `res`.

## Code

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res = n ^ res
        return res
```

## Complexity

- **Time:** `O(n)`: one pass.
- **Space:** `O(1)`: a single accumulator.

## Other Approaches

- **Hash set toggle:** add a value the first time it is seen and remove it the second time; the one remaining value is the answer. Time `O(n)`, Space `O(n)`.
- **Math:** `2 * sum(set(nums)) - sum(nums)`. Time `O(n)`, Space `O(n)`.

## Key Takeaway

XOR cancels pairs. Use it whenever values appear an even number of times except one. It also extends to "missing number" and, after splitting by a set bit, to "two single numbers".
