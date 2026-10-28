#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>

static std::uint64_t naive_reverse(std::uint64_t x, int bits) {
  std::uint64_t r = 0;
  for (int i = 0; i < bits; ++i) r |= ((x >> i) & 1ull) << (bits - 1 - i);
  return r;
}

EXAMPLE("Example 1: 32-bit reverse") {
  CHECK_EQ(reverse_bits(1u), 0x80000000u);
  CHECK_EQ(reverse_bits(0x0000000Fu), 0xF0000000u);
  CHECK_EQ(reverse_bits(43261596u), 964176192u);
}

EXAMPLE("Example 2: 64-bit reverse") {
  CHECK_EQ(reverse_bits64(1ull), 0x8000000000000000ull);
  CHECK_EQ(reverse_bits64(0x00000000000000FFull), 0xFF00000000000000ull);
}

CASE("zero and all ones are fixed points") {
  CHECK_EQ(reverse_bits(0u), 0u);
  CHECK_EQ(reverse_bits(0xFFFFFFFFu), 0xFFFFFFFFu);
  CHECK_EQ(reverse_bits64(0ull), 0ull);
  CHECK_EQ(reverse_bits64(~0ull), ~0ull);
}

CASE("palindromic and alternating patterns") {
  CHECK_EQ(reverse_bits(0x80000001u), 0x80000001u);
  CHECK_EQ(reverse_bits(0xAAAAAAAAu), 0x55555555u);
  CHECK_EQ(reverse_bits64(0x5555555555555555ull), 0xAAAAAAAAAAAAAAAAull);
  CHECK_EQ(reverse_bits(4294967293u), 3221225471u);
}

CASE("every single-bit input maps to the mirrored bit") {
  for (int i = 0; i < 32; ++i) CHECK_EQ(reverse_bits(1u << i), 1u << (31 - i));
  for (int i = 0; i < 64; ++i) CHECK_EQ(reverse_bits64(1ull << i), 1ull << (63 - i));
}

CASE("reversing twice gives the input back") {
  std::uint64_t s = 0x9E3779B97F4A7C15ull;
  for (int i = 0; i < 1000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    CHECK_EQ(reverse_bits64(reverse_bits64(s)), s);
    std::uint32_t w = static_cast<std::uint32_t>(s >> 17);
    CHECK_EQ(reverse_bits(reverse_bits(w)), w);
  }
}

CASE("matches a bit-by-bit reference on pseudo-random inputs") {
  std::uint64_t s = 42;
  for (int i = 0; i < 5000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    CHECK_EQ(reverse_bits64(s), naive_reverse(s, 64));
    std::uint32_t w = static_cast<std::uint32_t>(s >> 32);
    CHECK_EQ(static_cast<std::uint64_t>(reverse_bits(w)), naive_reverse(w, 32));
  }
}

CASE("64-bit reverse equals two swapped 32-bit reverses") {
  std::uint64_t x = 0x0123456789ABCDEFull;
  std::uint64_t expect = (static_cast<std::uint64_t>(reverse_bits(static_cast<std::uint32_t>(x))) << 32) |
                         reverse_bits(static_cast<std::uint32_t>(x >> 32));
  CHECK_EQ(reverse_bits64(x), expect);
  CHECK_EQ(reverse_bits64(x), 0xF7B3D591E6A2C480ull);
}
