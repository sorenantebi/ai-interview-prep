---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Population Count and Parity - Solution

## Intuition

**SWAR** (SIMD within a register) treats the 64-bit word as many small counters and adds neighbours in parallel:

1. Each 2-bit field gets the count of its two bits: `x - ((x >> 1) & 0x5555...)`.
2. Add pairs of 2-bit fields into 4-bit fields: `(x & 0x3333...) + ((x >> 2) & 0x3333...)`.
3. Add nibbles into bytes: `(x + (x >> 4)) & 0x0F0F...` (a byte holds at most 8, so no overflow).
4. Multiplying by `0x0101...01` adds all eight bytes into the top byte; shift it down by 56.

**Parity** only needs the count's lowest bit. XOR-folding the word in half repeatedly (`x ^= x >> 32`, `>> 16`, ... `>> 1`) leaves the XOR of all bits in bit 0.

## Approach

1. `popcount`: the four SWAR steps above, no branches.
2. `parity`: six XOR-folds, then `x & 1`.

Kernighan's loop `while (x) { x &= x - 1; ++n; }` is also fine and is faster on very sparse words; mention both.

## Code

```cpp
#include <cstdint>

int popcount(std::uint64_t x) {
    x = x - ((x >> 1) & 0x5555555555555555ull);
    x = (x & 0x3333333333333333ull) + ((x >> 2) & 0x3333333333333333ull);
    x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0Full;
    return static_cast<int>((x * 0x0101010101010101ull) >> 56);
}

bool parity(std::uint64_t x) {
    x ^= x >> 32;
    x ^= x >> 16;
    x ^= x >> 8;
    x ^= x >> 4;
    x ^= x >> 2;
    x ^= x >> 1;
    return x & 1;
}
```

## Complexity

- Time: O(1): about 12 ALU operations for `popcount`, 12 for `parity`, no branches.
- Space: O(1).

## Interview follow-ups

- Why does step 1 work? (For a 2-bit field `ab` worth `2a + b`, subtracting `a` leaves `a + b`, the count.)
- When is Kernighan faster than SWAR? (Few set bits; but its loop branch is data-dependent and can mispredict.)
- What does `std::popcount` compile to with `-mpopcnt` / `-march=native`? (A single `popcnt` instruction; without the flag, roughly this SWAR code.)
- Hamming distance between two 64-bit fingerprints: `popcount(a ^ b)`.
- Find the index of the k-th set bit in a bitmap order book.
