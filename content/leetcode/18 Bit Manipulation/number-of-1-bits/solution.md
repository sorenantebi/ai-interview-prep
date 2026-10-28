---
topic: "Bit Manipulation"
difficulty: Easy
leetcode: https://leetcode.com/problems/number-of-1-bits/
neetcode: https://neetcode.io/problems/number-of-one-bits
---
# Number of 1 Bits - Solution

**Question:** Number of 1 Bits - Question · **Difficulty:** Easy

## Intuition

`n & (n - 1)` clears the lowest set bit of `n`. Subtracting 1 flips that bit to 0 and turns every 0 below it into a 1, and the AND then wipes all of those positions. Repeating this until `n` is 0 takes exactly as many steps as there are set bits.

## Approach

1. Set `count = 0`.
2. While `n` is non-zero: `n &= n - 1` and `count += 1`.
3. Return `count`.

## Code

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            n &= n - 1
            res += 1
        return res
```

## Complexity

- **Time:** `O(k)`: `k` is the number of set bits, at most 32.
- **Space:** `O(1)`.

## Other Approaches

- **Check each bit:** `count += n & 1; n >>= 1` until `n` is 0. Time `O(32)`, Space `O(1)`.
- **Built-in:** `bin(n).count("1")` or `n.bit_count()` (Python 3.10+). Time `O(log n)`, Space `O(log n)` for the `bin` string.

## Key Takeaway

`n & (n - 1)` removes the lowest set bit. It is used for popcount, for checking powers of two (`n & (n - 1) == 0`), and for walking the subsets of a bitmask.

## C++

```cpp
/*
    Return number of '1' bits in an int
    Ex. n = 00001011 -> 3

    Simply count bit-by-bit & shift it off

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    int hammingWeight(uint32_t n) {
        int bit = 0;
        int result = 0;
        
        while (n != 0) {
            bit = n & 1;
            if (bit == 1) {
                result++;
            }
            n = n >> 1;
        }
        
        return result;
    }
};


/* use kernighan's algorithm to only iterate num(set bits) times */
class Solution {
public:
    int hammingWeight(uint32_t n) {
        unsigned int count = 0;

        while(n) {
            ++count;
            // unset rightmost set bit
            n = (n & (n - 1));
        }
        
        return count;
    }
};
```
