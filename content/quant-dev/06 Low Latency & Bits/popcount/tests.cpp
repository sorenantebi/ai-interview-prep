#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>

static int naive_count(std::uint64_t x) {
  int n = 0;
  for (int i = 0; i < 64; ++i) n += (x >> i) & 1;
  return n;
}

EXAMPLE("Example 1: popcount") {
  CHECK_EQ(popcount(0), 0);
  CHECK_EQ(popcount(0b1011), 3);
  CHECK_EQ(popcount(0xFFFFFFFFFFFFFFFFull), 64);
}

EXAMPLE("Example 2: parity") {
  CHECK_EQ(parity(0b1011), true);
  CHECK_EQ(parity(0b1001), false);
  CHECK_EQ(parity(0), false);
}

CASE("single bits in every position") {
  for (int i = 0; i < 64; ++i) {
    CHECK_EQ(popcount(1ull << i), 1);
    CHECK_EQ(parity(1ull << i), true);
  }
}

CASE("all-but-one bit set") {
  for (int i = 0; i < 64; ++i) {
    CHECK_EQ(popcount(~(1ull << i)), 63);
    CHECK_EQ(parity(~(1ull << i)), true);
  }
  CHECK_EQ(parity(~0ull), false);
}

CASE("masks and high bits") {
  CHECK_EQ(popcount(0x5555555555555555ull), 32);
  CHECK_EQ(popcount(0x8000000000000000ull), 1);
  CHECK_EQ(popcount(0xFF00000000000000ull), 8);
  CHECK_EQ(popcount(0x00000000FFFFFFFFull), 32);
  CHECK_EQ(popcount(0xF0F0F0F0F0F0F0F0ull), 32);
}

CASE("low n bits set for every n") {
  std::uint64_t m = 0;
  for (int n = 0; n <= 64; ++n) {
    CHECK_EQ(popcount(m), n);
    CHECK_EQ(parity(m), n % 2 == 1);
    m = (m << 1) | 1;
  }
}

CASE("matches a bit-by-bit reference on pseudo-random inputs") {
  std::uint64_t s = 2024;
  for (int i = 0; i < 20000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    std::uint64_t x = s & (s >> (s % 7));  // vary the density
    int n = naive_count(x);
    CHECK_EQ(popcount(x), n);
    CHECK_EQ(parity(x), n % 2 == 1);
  }
}

CASE("Hamming distance via popcount of XOR") {
  std::uint64_t a = 0x0123456789ABCDEFull, b = 0xFEDCBA9876543210ull;
  CHECK_EQ(popcount(a ^ b), 64);
  CHECK_EQ(popcount(a ^ a), 0);
  CHECK_EQ(popcount(0xDEADBEEFull ^ 0xDEADBEEEull), 1);
}
