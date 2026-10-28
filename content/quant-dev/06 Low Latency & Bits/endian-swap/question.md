---
topic: "Low Latency & Bits"
difficulty: Easy
---
# Endian Swap

**Topic:** Low Latency & Bits · **Difficulty:** Easy

## Problem

x86 and ARM servers store integers little-endian (least significant byte first), but many exchange protocols and the network itself use **big-endian** ("network byte order"). Feed handlers decode prices, quantities and sequence numbers straight out of packets, so they swap byte order millions of times a second, and you should be able to write the swap yourself.

Implement, **without** `__builtin_bswap*`, `std::byteswap`, `htonl` or similar:

```cpp
std::uint16_t byte_swap16(std::uint16_t x);
std::uint32_t byte_swap32(std::uint32_t x);
std::uint64_t byte_swap64(std::uint64_t x);

// Value whose in-memory bytes are x in big-endian order (most significant byte at the lowest address).
// A no-op on big-endian machines, a byte swap on little-endian ones. Use std::endian to decide.
std::uint32_t to_big_endian32(std::uint32_t x);
std::uint64_t to_big_endian64(std::uint64_t x);
```

## Examples

**Example 1**
```cpp
byte_swap16(0x1234);               // 0x3412
byte_swap32(0x12345678);           // 0x78563412
byte_swap64(0x0102030405060708);   // 0x0807060504030201
```

**Example 2**
```cpp
std::uint32_t be = to_big_endian32(0x0A0B0C0D);
unsigned char bytes[4];
std::memcpy(bytes, &be, 4);
// bytes == {0x0A, 0x0B, 0x0C, 0x0D} on any machine
```

## Constraints

- Shifts and masks only; no loops are needed.
- `to_big_endian*` must be correct on both little- and big-endian targets.
