#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>

EXAMPLE("Example 1: is_power_of_two") {
  CHECK_EQ(is_power_of_two(64), true);
  CHECK_EQ(is_power_of_two(96), false);
  CHECK_EQ(is_power_of_two(0), false);
}

EXAMPLE("Example 2: next_power_of_two and log2_floor") {
  CHECK_EQ(next_power_of_two(5), 8ull);
  CHECK_EQ(next_power_of_two(8), 8ull);
  CHECK_EQ(next_power_of_two(0), 1ull);
  CHECK_EQ(log2_floor(1), 0);
  CHECK_EQ(log2_floor(1000), 9);
}

CASE("is_power_of_two on every power and its neighbours") {
  for (int i = 0; i < 64; ++i) {
    std::uint64_t p = 1ull << i;
    CHECK(is_power_of_two(p));
    if (i >= 2) CHECK(!is_power_of_two(p - 1));
    if (i >= 1) CHECK(!is_power_of_two(p + 1));
  }
  CHECK(!is_power_of_two(~0ull));
  CHECK(!is_power_of_two(0x8000000000000001ull));
}

CASE("next_power_of_two of 1, 2, 3 and the top of the range") {
  CHECK_EQ(next_power_of_two(1), 1ull);
  CHECK_EQ(next_power_of_two(2), 2ull);
  CHECK_EQ(next_power_of_two(3), 4ull);
  CHECK_EQ(next_power_of_two(0x8000000000000000ull), 0x8000000000000000ull);
  CHECK_EQ(next_power_of_two(0x4000000000000001ull), 0x8000000000000000ull);
}

CASE("next_power_of_two around every power") {
  for (int i = 1; i < 63; ++i) {
    std::uint64_t p = 1ull << i;
    CHECK_EQ(next_power_of_two(p), p);
    CHECK_EQ(next_power_of_two(p + 1), p << 1);
    CHECK_EQ(next_power_of_two(p - 1), i == 1 ? 1ull : p);
  }
}

CASE("log2_floor on powers, neighbours and the maximum") {
  for (int i = 0; i < 64; ++i) {
    std::uint64_t p = 1ull << i;
    CHECK_EQ(log2_floor(p), i);
    if (i >= 1) CHECK_EQ(log2_floor(p - 1), i == 1 ? 0 : i - 1);
    if (i >= 1 && i < 63) CHECK_EQ(log2_floor(p + 1), i);
  }
  CHECK_EQ(log2_floor(~0ull), 63);
}

CASE("results agree with each other on pseudo-random inputs") {
  std::uint64_t s = 7;
  for (int k = 0; k < 5000; ++k) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    std::uint64_t x = s >> (1 + s % 63);  // stays below 2^63
    if (x == 0) continue;
    int l = log2_floor(x);
    CHECK((x >> l) == 1ull);
    std::uint64_t n = next_power_of_two(x);
    CHECK(is_power_of_two(n));
    CHECK(n >= x);
    CHECK(n / 2 < x);
    CHECK_EQ(is_power_of_two(x), n == x);
  }
}

CASE("power-of-two capacity turns modulo into a mask") {
  std::uint64_t cap = next_power_of_two(1000);
  CHECK_EQ(cap, 1024ull);
  for (std::uint64_t i = 0; i < 5000; i += 7) CHECK_EQ(i & (cap - 1), i % cap);
}
