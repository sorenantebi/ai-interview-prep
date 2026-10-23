---
topic: "Math & Geometry"
difficulty: Easy
leetcode: https://leetcode.com/problems/happy-number/
neetcode: https://neetcode.io/problems/non-cyclical-number
---
# Happy Number - Solution

**Question:** Happy Number - Question · **Difficulty:** Easy

## Intuition

The "sum of squared digits" map sends any number to a much smaller value (at most `81 * digits`), so the sequence soon stays in a small range and must eventually repeat. That turns the problem into cycle detection on an implicit linked list: either we reach `1` (a fixed point) or we enter a loop. Floyd's tortoise-and-hare finds the loop in `O(1)` space.

## Approach

1. Write `nxt(x)`, which returns the sum of the squares of `x`'s digits.
2. Start with `slow = n` and `fast = nxt(n)`.
3. While `fast != 1` and `slow != fast`, move `slow` one step and `fast` two steps.
4. Return `fast == 1`.

## Code

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        slow, fast = n, self.sumSquareDigits(n)

        while slow != fast:
            fast = self.sumSquareDigits(fast)
            fast = self.sumSquareDigits(fast)
            slow = self.sumSquareDigits(slow)

        return True if fast == 1 else False

    def sumSquareDigits(self, n):
        output = 0
        while n:
            output += (n % 10) ** 2
            n = n // 10
        return output
```

## Complexity

- **Time:** `O(log n)`: the first step costs `O(log n)` digits and quickly brings the value below about 243. After that, every step and the cycle length are bounded by a constant.
- **Space:** `O(1)`: only two pointers.

## Other Approaches

- **Hash set of seen values:** keep iterating until you reach `1` or see a value again. Time `O(log n)`, Space `O(log n)` (in practice bounded by a small constant).

## Key Takeaway

When repeatedly applying a function must end in a fixed point or a cycle, treat the values as nodes of a linked list. Use Floyd's fast/slow pointers (or a seen-set) to detect the cycle.
