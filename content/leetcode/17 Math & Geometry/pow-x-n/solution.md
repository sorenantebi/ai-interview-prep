---
topic: "Math & Geometry"
difficulty: Medium
leetcode: https://leetcode.com/problems/powx-n/
neetcode: https://neetcode.io/problems/pow-x-n
---
# Pow(x, n) - Solution

**Question:** Pow(x, n) - Question · **Difficulty:** Medium

## Intuition

Multiplying `x` by itself `n` times is too slow when `|n|` is around 2^31. Binary exponentiation uses `x^n = (x^2)^(n/2)`. Read the bits of `n`: keep squaring the base, and multiply it into the result whenever the current bit is 1. That takes `O(log n)` multiplications. For a negative exponent, use `1/x` as the base and `-n` as the exponent.

## Approach

1. If `n < 0`, set `x = 1 / x` and `n = -n`. Python integers don't overflow, so `-(-2^31)` is safe.
2. Set `res = 1.0`.
3. While `n > 0`: if `n & 1`, multiply `res *= x`; then square `x *= x` and shift `n >>= 1`.
4. Return `res`.

## Code

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            if x == 0:
                return 0
            if n == 0:
                return 1

            res = helper(x * x, n // 2)
            return x * res if n % 2 else res

        res = helper(x, abs(n))
        return res if n >= 0 else 1 / res
```

## Complexity

- **Time:** `O(log |n|)`: one loop iteration per bit of `n`.
- **Space:** `O(1)`: iterative, no recursion stack.

## Other Approaches

- **Recursive fast power:** `half = myPow(x, n // 2)`, then return `half * half`, times `x` if `n` is odd. Time `O(log n)`, Space `O(log n)` for the recursion stack.
- **Naive repeated multiplication:** Time `O(|n|)`, Space `O(1)`. Too slow when `|n|` is around 2^31.

## Key Takeaway

Exponentiation by squaring turns `O(n)` repeated work into `O(log n)`. The same idea gives modular power, matrix power (fast Fibonacci), and binary lifting. In languages with fixed-size integers, remember that negating `INT_MIN` overflows.
