---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Endian Swap - Solution

## Intuition

A byte swap moves byte `i` to position `n - 1 - i`. Like bit reversal, it's easiest as divide and conquer: swap the two halves, then the halves of each half, down to single bytes. For 16 bits that's one step, for 32 two, for 64 three. Endianness is a compile-time fact (`std::endian::native` in C++20), so `to_big_endian` picks swap or no-op with `if constexpr` and costs nothing extra.

## Approach

1. `byte_swap16`: `(x >> 8) | (x << 8)`, cast back to 16 bits (the shift promotes to `int`).
2. `byte_swap32`: swap 16-bit halves, then swap bytes inside each half with masks `0xFF00FF00` / `0x00FF00FF`.
3. `byte_swap64`: swap 32-bit halves, then 16-bit pairs, then bytes.
4. `to_big_endian*`: `if constexpr (std::endian::native == std::endian::little) return byte_swap(x); else return x;`.

## Code

```cpp
#include <bit>
#include <cstdint>

std::uint16_t byte_swap16(std::uint16_t x) {
    return static_cast<std::uint16_t>((x >> 8) | (x << 8));
}

std::uint32_t byte_swap32(std::uint32_t x) {
    x = (x >> 16) | (x << 16);
    return ((x & 0xFF00FF00u) >> 8) | ((x & 0x00FF00FFu) << 8);
}

std::uint64_t byte_swap64(std::uint64_t x) {
    x = (x >> 32) | (x << 32);
    x = ((x & 0xFFFF0000FFFF0000ull) >> 16) | ((x & 0x0000FFFF0000FFFFull) << 16);
    return ((x & 0xFF00FF00FF00FF00ull) >> 8) | ((x & 0x00FF00FF00FF00FFull) << 8);
}

std::uint32_t to_big_endian32(std::uint32_t x) {
    if constexpr (std::endian::native == std::endian::little) return byte_swap32(x);
    else return x;
}

std::uint64_t to_big_endian64(std::uint64_t x) {
    if constexpr (std::endian::native == std::endian::little) return byte_swap64(x);
    else return x;
}
```

## Complexity

- Time: O(1): 1, 2 or 3 mask-shift-or steps. Modern compilers recognise this pattern and emit a single `bswap` / `rev` instruction.
- Space: O(1).

## Interview follow-ups

- Decode a big-endian `uint32` price field from a `const char*` packet without undefined behaviour. (`std::memcpy` into a local, then swap; never `*reinterpret_cast<const uint32_t*>(p)`, which breaks aliasing and alignment rules.)
- Why is a swap its own inverse, and why does that mean `from_big_endian == to_big_endian`?
- Some binary protocols (e.g. many exchange native feeds) are little-endian on purpose. Why would an exchange choose that?
- How do you swap a `double`? (`std::bit_cast` to `uint64_t`, swap, `bit_cast` back.)
