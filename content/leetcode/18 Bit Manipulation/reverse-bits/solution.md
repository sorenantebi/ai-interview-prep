---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/reverse-bits/
neetcode: https://neetcode.io/problems/reverse-bits
---
# Reverse Bits - Solution

**Question:** Reverse Bits - Question · **Difficulty:** Easy

## Intuition

Build the result one bit at a time. Read the lowest bit of `n` and append it to the right of `res` by shifting `res` left. After exactly 32 iterations, the first bit read (bit 0 of `n`) has moved to bit 31 of `res`, so the bits are reversed. The loop must run 32 times even after `n` becomes 0, so that zeros fill in.

## Approach

1. Set `res = 0`.
2. Repeat 32 times: `res = (res << 1) | (n & 1)`, then `n >>= 1`.
3. Return `res`.

## Code

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for i in range(32):
            bit = (n >> i) & 1
            res += (bit << (31 - i))
        return res
```

## Complexity

- **Time:** `O(1)`: always exactly 32 iterations.
- **Space:** `O(1)`.

## Other Approaches

- **Divide-and-conquer masks:** swap 16-bit halves, then 8-bit groups, then 4, 2 and 1 bits using masks such as `0xff00ff00`. Five steps instead of 32. Time `O(1)`, Space `O(1)`.
- **Byte lookup table (the follow-up):** precompute the reversals of all 256 bytes and combine four lookups. This is fast when the function is called many times. Time `O(1)`, Space `O(256)`.
- **String:** `int(format(n, '032b')[::-1], 2)`. Time `O(1)`, Space `O(1)`.

## Key Takeaway

`res = (res << 1) | (n & 1); n >>= 1` moves bits from one integer to another in reverse order. Fix the iteration count at the word size so that leading zeros are reversed too.

## C++

```cpp
/*
    Reverse bits of a given integer
    Ex. n = 10011100 -> 00111001 = 57

    Shift into result & shift out of n

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t result = 0;
        
        for (int i = 0; i < 32; i++) {
            result <<= 1;
            result |= n & 1;
            n >>= 1;
        }
        
        return result;
    }
};
```
