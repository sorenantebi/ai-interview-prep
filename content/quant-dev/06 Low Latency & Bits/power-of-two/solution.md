---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Power of Two Helpers - Solution

## Intuition

- `x & (x - 1)` clears the lowest set bit. A power of two has exactly one set bit, so the result is zero (and `x` itself must be non-zero).
- To round up, "smear" the highest set bit of `x - 1` into every lower position, giving `0b0...0111...1`; adding one carries into the next power of two. Starting from `x - 1` makes exact powers of two map to themselves.
- For `log2_floor`, binary-search the highest set bit: if the top 32 bits are non-zero, the answer is at least 32 and you shift them down, then repeat with 16, 8, 4, 2, 1.

## Approach

1. `is_power_of_two`: `x != 0 && (x & (x - 1)) == 0`.
2. `next_power_of_two`: return 1 for `x == 0`; otherwise `--x`, then `x |= x >> 1; x |= x >> 2; ... x |= x >> 32;` and return `x + 1`.
3. `log2_floor`: six "is anything above this half?" steps, adding the shift to the answer each time.

## Code

```cpp
#include <cstdint>

bool is_power_of_two(std::uint64_t x) {
    return x != 0 && (x & (x - 1)) == 0;
}

std::uint64_t next_power_of_two(std::uint64_t x) {
    if (x == 0) return 1;
    --x;
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
    x |= x >> 32;
    return x + 1;
}

int log2_floor(std::uint64_t x) {
    int r = 0;
    for (int shift = 32; shift > 0; shift /= 2) {
        if (x >> shift) {
            x >>= shift;
            r += shift;
        }
    }
    return r;
}
```

## Complexity

- Time: O(1) for `is_power_of_two`; O(log 64) = 6 steps for the other two.
- Space: O(1).

## Interview follow-ups

- What do `std::bit_ceil`, `std::bit_width` and `std::countl_zero` (C++20) compile to on x86? (`lzcnt` / `bsr`, one instruction.) Then `log2_floor(x) == 63 - countl_zero(x)`.
- Why is `i & (cap - 1)` faster than `i % cap`? (Integer division takes tens of cycles; AND takes one.) Does the compiler do this for you? (Only if `cap` is a compile-time constant.)
- What goes wrong in `next_power_of_two` for `x > 2^63`? How would you report it?
- Isolate the lowest set bit with `x & -x`. Where is that used? (Fenwick trees, iterating set bits of a bitmap.)
