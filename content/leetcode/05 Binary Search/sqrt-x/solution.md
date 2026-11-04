---
topic: "Binary Search"
difficulty: Easy
leetcode: https://leetcode.com/problems/sqrtx/
neetcode: https://neetcode.io/problems/sqrtx
---
# Sqrt(x) - Solution

## Intuition

The answer is the largest integer `m` with `m * m <= x`. Since `m * m` increases monotonically with `m`, the candidates split into a block where `m * m <= x` followed by a block where `m * m > x`. That makes it a binary search for the boundary.

## Approach

1. Search the range `[0, x]` (for `x >= 1`, `x // 2 + 1` also works as an upper bound, but `[0, x]` is simpler and safe).
2. Compute `mid = (lo + hi) // 2`.
3. If `mid * mid <= x`, `mid` is a valid answer, so record it and search higher (`lo = mid + 1`).
4. Otherwise `mid` is too large, so search lower (`hi = mid - 1`).
5. When `lo > hi`, return the last recorded valid `mid`.

## Code

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        while l <= r:
            mid = (l + r) // 2
            if mid * mid == x:
                return mid
            if mid * mid < x:
                l = mid + 1
            else:
                r = mid - 1
        return r
```

## Complexity

- **Time:** `O(log x)` — the search range halves each iteration.
- **Space:** `O(1)` — only a few integer variables are used.

## Other Approaches

- **Newton's method:** iterate `r = (r + x // r) // 2` starting from `r = x` until `r * r <= x` — Time `O(log x)` (converges quadratically) / Space `O(1)`
- **Linear scan:** increment `m` until `(m + 1) * (m + 1) > x` — Time `O(sqrt(x))` / Space `O(1)`

## C++

```cpp
/*
  Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.
  You must not use any built-in exponent function or operator.

  For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

  Ex. Input: x = 4
      Output: 2
      Explanation: The square root of 4 is 2, so we return 2.

  Time  : O(log N)
  Space : O(1)
*/

class Solution {
public:
    int mySqrt(int x) {
        if(x == 0 || x == 1)
            return x;
            
        long long beg = 0, mid = 0, end = x/2;
        while(beg <= end) {
            mid = (beg + end)/2;
            if(mid * mid < x) {
                if((mid + 1) * (mid + 1) > x)
                    return mid;
                beg = mid+1;
            } else if(mid * mid > x) {
                if( (mid - 1) * (mid - 1) < x)
                    return mid-1;
                end = mid - 1;
            } else 
                return mid;
        }
        return mid;
    }
};
```
