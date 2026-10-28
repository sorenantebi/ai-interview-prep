---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Reverse Bits

**Topic:** Low Latency & Bits · **Difficulty:** Easy

## Problem

Bit tricks show up in low-latency code wherever a branchy loop can be replaced by a few shifts and masks: packed order flags, bitmap order books, hash mixing, CRCs. A classic warm-up is reversing the bit order of a word: bit 0 becomes bit 31, bit 1 becomes bit 30, and so on.

Implement:

```cpp
std::uint32_t reverse_bits(std::uint32_t x);
std::uint64_t reverse_bits64(std::uint64_t x);
```

Aim for the branch-free divide-and-conquer version (swap halves, then quarters, ... then neighbouring bits) rather than a 32-step loop.

## Examples

**Example 1**
```cpp
reverse_bits(1u);            // 0x80000000
reverse_bits(0x0000000Fu);   // 0xF0000000
reverse_bits(43261596u);     // 964176192  (0b00000010100101000001111010011100 -> 0b00111001011110000010100101000000)
```

**Example 2**
```cpp
reverse_bits64(1ull);                    // 0x8000000000000000
reverse_bits64(0x00000000000000FFull);   // 0xFF00000000000000
```

## Constraints

- O(log w) operations for a w-bit word (5 steps for 32 bits, 6 for 64), no loops over individual bits.
- No compiler builtins (`__builtin_bitreverse32` and friends).
