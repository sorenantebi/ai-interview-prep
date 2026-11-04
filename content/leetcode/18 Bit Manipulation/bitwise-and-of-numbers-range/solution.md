---
topic: "Bit Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/bitwise-and-of-numbers-range/
neetcode: https://neetcode.io/problems/bitwise-and-of-numbers-range
---
# Bitwise AND of Numbers Range - Solution

## Intuition

Within a range of consecutive numbers, any bit position that changes between `left` and `right` will take both values 0 and 1 somewhere in the range, so it ANDs to 0. The only bits that survive are the leading bits that `left` and `right` share, i.e. their common binary prefix. Everything after the prefix becomes 0.

## Approach

1. Start with a shift counter at 0.
2. While `left != right`, shift both right by one bit and increment the counter. This strips the differing low bits.
3. When they become equal, the value is the common prefix.
4. Shift the prefix left by the counter to restore its position; the low bits are zeros.

## Code

```python
# check difference at each bit (cannot be more than left - right)
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        res = 0

        for i in range(32):
            bit = (left >> i) & 1
            if not bit:
                continue
            
            remain = left % (1 << (i + 1))
            diff = (1 << (i + 1)) - remain
            if right - left < diff:
                res = res | (1 << i)
        return res

# find the longest matching prefix of set bits between left and right
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        i = 0
        while left != right:
            left = left >> 1
            right = right >> 1
            i += 1
        return left << i
```

## Complexity

- **Time:** `O(log n)` — at most 31 shifts, since each iteration removes one bit.
- **Space:** `O(1)` — only a few integer variables.

## Other Approaches

- **Brian Kernighan's trick:** repeatedly clear the lowest set bit of `right` (`right &= right - 1`) while `right > left`, then return `right` — Time `O(log n)` / Space `O(1)`
- **Brute force AND:** AND every number from `left` to `right`, with early exit when the result hits 0 — Time `O(right - left)` / Space `O(1)`
