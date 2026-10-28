---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Power of Two Helpers

**Topic:** Low Latency & Bits · **Difficulty:** Easy

## Problem

Ring buffers, hash tables and memory pools in low-latency systems size themselves to powers of two, so `index % capacity` becomes the much cheaper `index & (capacity - 1)`. That needs three small helpers, all branch-light bit tricks:

```cpp
bool is_power_of_two(std::uint64_t x);           // exactly one bit set; 0 is not a power of two
std::uint64_t next_power_of_two(std::uint64_t x); // smallest power of two >= x; next_power_of_two(0) == 1
int log2_floor(std::uint64_t x);                  // floor(log2(x)) = index of the highest set bit; x > 0
```

Don't use `std::has_single_bit`, `std::bit_ceil`, `std::bit_width`, `__builtin_clz` or floating-point `log2`: the point is to know the tricks behind them.

## Examples

**Example 1**
```cpp
is_power_of_two(64);    // true
is_power_of_two(96);    // false
is_power_of_two(0);     // false
```

**Example 2**
```cpp
next_power_of_two(5);   // 8
next_power_of_two(8);   // 8   (already a power of two)
next_power_of_two(0);   // 1
log2_floor(1);          // 0
log2_floor(1000);       // 9   (512 <= 1000 < 1024)
```

## Constraints

- `next_power_of_two`: `0 <= x <= 2^63` (the result must fit in 64 bits).
- `log2_floor`: `1 <= x <= 2^64 - 1`.
- O(1) / O(log 64) operations; no loop over all 64 bits.
