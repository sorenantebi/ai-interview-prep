#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <cstring>

EXAMPLE("Example 1: byte swaps of known constants") {
  CHECK_EQ(byte_swap16(0x1234), 0x3412);
  CHECK_EQ(byte_swap32(0x12345678u), 0x78563412u);
  CHECK_EQ(byte_swap64(0x0102030405060708ull), 0x0807060504030201ull);
}

EXAMPLE("Example 2: to_big_endian32 puts the most significant byte first in memory") {
  std::uint32_t be = to_big_endian32(0x0A0B0C0Du);
  unsigned char bytes[4];
  std::memcpy(bytes, &be, 4);
  CHECK_EQ(int(bytes[0]), 0x0A);
  CHECK_EQ(int(bytes[1]), 0x0B);
  CHECK_EQ(int(bytes[2]), 0x0C);
  CHECK_EQ(int(bytes[3]), 0x0D);
}

CASE("zero, all ones and symmetric values are unchanged") {
  CHECK_EQ(byte_swap16(0), 0);
  CHECK_EQ(byte_swap16(0xFFFF), 0xFFFF);
  CHECK_EQ(byte_swap32(0u), 0u);
  CHECK_EQ(byte_swap32(0xABCDCDABu), 0xABCDCDABu);
  CHECK_EQ(byte_swap64(~0ull), ~0ull);
  CHECK_EQ(byte_swap64(0x1122334444332211ull), 0x1122334444332211ull);
}

CASE("16-bit swap keeps the result in 16 bits") {
  CHECK_EQ(byte_swap16(0x00FF), 0xFF00);
  CHECK_EQ(byte_swap16(0xFF00), 0x00FF);
  CHECK_EQ(byte_swap16(0x8001), 0x0180);
}

CASE("a single byte moves to the mirrored position") {
  for (int i = 0; i < 4; ++i) CHECK_EQ(byte_swap32(0xABu << (8 * i)), 0xABu << (8 * (3 - i)));
  for (int i = 0; i < 8; ++i) CHECK_EQ(byte_swap64(0xCDull << (8 * i)), 0xCDull << (8 * (7 - i)));
}

CASE("swapping twice gives the input back") {
  std::uint64_t s = 99;
  for (int i = 0; i < 2000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    CHECK_EQ(byte_swap64(byte_swap64(s)), s);
    std::uint32_t w = static_cast<std::uint32_t>(s >> 13);
    CHECK_EQ(byte_swap32(byte_swap32(w)), w);
    std::uint16_t h = static_cast<std::uint16_t>(s >> 40);
    CHECK_EQ(byte_swap16(byte_swap16(h)), h);
  }
}

CASE("byte_swap64 matches reversing the bytes in memory") {
  std::uint64_t s = 5;
  for (int i = 0; i < 2000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    unsigned char in[8], out[8];
    std::memcpy(in, &s, 8);
    std::uint64_t swapped = byte_swap64(s);
    std::memcpy(out, &swapped, 8);
    for (int k = 0; k < 8; ++k) CHECK_EQ(int(out[k]), int(in[7 - k]));
  }
}

CASE("to_big_endian64 lays out bytes most significant first") {
  std::uint64_t be = to_big_endian64(0x0102030405060708ull);
  unsigned char bytes[8];
  std::memcpy(bytes, &be, 8);
  for (int k = 0; k < 8; ++k) CHECK_EQ(int(bytes[k]), k + 1);
}

CASE("decode a big-endian sequence number from a packet") {
  const unsigned char packet[] = {0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x30, 0x39};  // 12345 (BE)
  std::uint64_t raw;
  std::memcpy(&raw, packet, 8);
  CHECK_EQ(to_big_endian64(raw), 0x0000000100003039ull);  // the swap is its own inverse
  std::uint32_t lo;
  std::memcpy(&lo, packet + 4, 4);
  CHECK_EQ(to_big_endian32(lo), 12345u);
}
