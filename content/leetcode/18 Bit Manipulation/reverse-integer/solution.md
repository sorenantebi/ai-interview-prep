---
topic: "Bit Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/reverse-integer/
neetcode: https://neetcode.io/problems/reverse-integer
---
# Reverse Integer - Solution

**Question:** Reverse Integer - Question · **Difficulty:** Medium

## Intuition

Pop digits off the end of `|x|` with `% 10` and `// 10`, and push them onto the result with `res * 10 + digit`. To stay within 32 bits, check before each push whether `res * 10 + digit` would exceed `INT_MAX`. Rearranged, the check is `res > (INT_MAX - digit) // 10`, which uses only in-range arithmetic. Work with the absolute value and apply the sign at the end. A reversed magnitude of exactly `2^31` can't occur, since it would need an input outside the valid range, so checking against `INT_MAX` is enough for negative inputs too.

## Approach

1. Record `sign`, then set `x = abs(x)` and `res = 0`.
2. While `x > 0`:
   - `digit = x % 10`, `x //= 10`;
   - if `res > (INT_MAX - digit) // 10`, return `0` because of overflow;
   - `res = res * 10 + digit`.
3. Return `sign * res`.

## Code

```python
class Solution:
    def reverse(self, x: int) -> int:
        # Integer.MAX_VALUE = 2147483647 (end with 7)
        # Integer.MIN_VALUE = -2147483648 (end with -8 )

        MIN = -2147483648  # -2^31,
        MAX = 2147483647  #  2^31 - 1

        res = 0
        while x:
            digit = int(math.fmod(x, 10))  # (python dumb) -1 %  10 = 9
            x = int(x / 10)  # (python dumb) -1 // 10 = -1

            if res > MAX // 10 or (res == MAX // 10 and digit > MAX % 10):
                return 0
            if res < MIN // 10 or (res == MIN // 10 and digit < MIN % 10):
                return 0
            res = (res * 10) + digit

        return res
```

## Complexity

- **Time:** `O(log10 |x|)`: one iteration per digit (at most 10).
- **Space:** `O(1)`.

## Other Approaches

- **String reversal:** `int(str(abs(x))[::-1])`, apply the sign, then range-check. Simple, but it relies on a value that may exceed 32 bits. Time `O(log x)`, Space `O(log x)`.

## Key Takeaway

Detect overflow before it happens: rearrange `res * 10 + d <= MAX` into `res <= (MAX - d) // 10`. In Python, take the absolute value before using `%` and `//`, because they floor toward negative infinity.

## C++

```cpp
/*
    Given a signed 32-bit integer, return it with its digits reversed
    Ex. x = 123 -> 321, x = -123 -> -321, x = 120 -> 21

    Reverse bit-by-bit starting from right, shift right off every time

    Time: O(log x)
    Space: O(1)
*/

class Solution {
public:
    int reverse(int x) {
        int rev = 0;
        while (x != 0) {
            int temp = x % 10;
            x /= 10;
            if (rev > INT_MAX / 10 || (rev == INT_MAX / 10 && temp > 7)) {
                return 0;
            }
            if (rev < INT_MIN / 10 || (rev == INT_MIN / 10 && temp < -8)) {
                return 0;
            }
            rev = rev * 10 + temp;
        }
        return rev;
    }
};
```
