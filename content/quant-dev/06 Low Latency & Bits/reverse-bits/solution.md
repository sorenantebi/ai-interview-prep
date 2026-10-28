---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Reverse Bits - Solution

## Intuition

Reversing a word is the same as swapping its two halves, then swapping the two halves inside each half, and so on down to single bits. Each level is one "mask, shift, OR" over the whole word at once, so a 32-bit reverse takes 5 steps and a 64-bit one 6.

## Approach

For 32 bits:
1. Swap 16-bit halves: `x = (x >> 16) | (x << 16)`.
2. Swap bytes within each half: `((x & 0xFF00FF00) >> 8) | ((x & 0x00FF00FF) << 8)`.
3. Swap nibbles: masks `0xF0F0F0F0` / `0x0F0F0F0F`, shift 4.
4. Swap bit pairs: masks `0xCCCCCCCC` / `0x33333333`, shift 2.
5. Swap single bits: masks `0xAAAAAAAA` / `0x55555555`, shift 1.

The 64-bit version adds a first step swapping the 32-bit halves and uses 64-bit masks.

## Code

```cpp
#include <cstdint>

std::uint32_t reverse_bits(std::uint32_t x) {
    x = (x >> 16) | (x << 16);
    x = ((x & 0xFF00FF00u) >> 8) | ((x & 0x00FF00FFu) << 8);
    x = ((x & 0xF0F0F0F0u) >> 4) | ((x & 0x0F0F0F0Fu) << 4);
    x = ((x & 0xCCCCCCCCu) >> 2) | ((x & 0x33333333u) << 2);
    x = ((x & 0xAAAAAAAAu) >> 1) | ((x & 0x55555555u) << 1);
    return x;
}

std::uint64_t reverse_bits64(std::uint64_t x) {
    x = (x >> 32) | (x << 32);
    x = ((x & 0xFFFF0000FFFF0000ull) >> 16) | ((x & 0x0000FFFF0000FFFFull) << 16);
    x = ((x & 0xFF00FF00FF00FF00ull) >> 8) | ((x & 0x00FF00FF00FF00FFull) << 8);
    x = ((x & 0xF0F0F0F0F0F0F0F0ull) >> 4) | ((x & 0x0F0F0F0F0F0F0F0Full) << 4);
    x = ((x & 0xCCCCCCCCCCCCCCCCull) >> 2) | ((x & 0x3333333333333333ull) << 2);
    x = ((x & 0xAAAAAAAAAAAAAAAAull) >> 1) | ((x & 0x5555555555555555ull) << 1);
    return x;
}
```

## Complexity

- Time: O(log w): 5 (or 6) mask-shift-or steps, no branches.
- Space: O(1).

## Interview follow-ups

- Build the 64-bit version from two 32-bit calls: `(uint64_t(reverse_bits(lo)) << 32) | reverse_bits(hi)`.
- Use a 256-entry byte lookup table. When is that faster or slower than the mask version? (Table lookups can miss the cache; the mask version is pure ALU.)
- The first step for 32 bits is a byte swap followed by bit work: which single instruction does it map to on x86? (`bswap`; ARM even has `rbit` for the whole reverse.)
- Why must you use unsigned types here? (Right-shifting a negative signed value is implementation-defined before C++20 and sign-extends.)
