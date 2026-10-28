---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Population Count and Parity

**Topic:** Low Latency & Bits · **Difficulty:** Easy

## Problem

Counting set bits is everywhere in fast code: how many price levels are occupied in a bitmap order book, how many symbols in a subscription mask are active, Hamming distance between feature fingerprints. Hardware has an instruction for it, but interviewers want to see that you know how to compute it in a few arithmetic steps.

Implement, **without** `__builtin_popcount*`, `std::popcount` or `std::bitset::count`:

```cpp
int popcount(std::uint64_t x);   // number of 1 bits
bool parity(std::uint64_t x);    // true if the number of 1 bits is odd
```

Use either Kernighan's trick (`x &= x - 1` clears the lowest set bit, so loop once per set bit) or the branch-free SWAR method (add bits in parallel inside the word: pairs, then nibbles, then bytes).

## Examples

**Example 1**
```cpp
popcount(0);                       // 0
popcount(0b1011);                  // 3
popcount(0xFFFFFFFFFFFFFFFFull);   // 64
```

**Example 2**
```cpp
parity(0b1011);   // true  (3 bits set)
parity(0b1001);   // false (2 bits set)
parity(0);        // false
```

## Constraints

- O(number of set bits) or O(log 64) operations: no loop that inspects all 64 bits one by one.
- No compiler builtins or `<bit>` functions.
