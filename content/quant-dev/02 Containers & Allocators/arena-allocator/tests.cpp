#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <cstring>
#include <vector>

static std::uintptr_t addr(const void* p) { return reinterpret_cast<std::uintptr_t>(p); }

EXAMPLE("Example 1: bump, align, fail without side effects, reset") {
  Arena a(256);
  void* p = a.allocate(10, 1);
  CHECK(p != nullptr);
  CHECK_EQ(a.used(), 10u);
  void* q = a.allocate(8, 8);
  CHECK_EQ(a.used(), 24u);
  CHECK_EQ(static_cast<char*>(q) - static_cast<char*>(p), 16);
  CHECK(a.allocate(1000) == nullptr);
  CHECK_EQ(a.used(), 24u);
  a.reset();
  CHECK(a.allocate(10, 1) == p);
}

EXAMPLE("Example 2: cache-line aligned block") {
  Arena a(1024);
  a.allocate(3, 1);
  void* line = a.allocate(64, 64);
  CHECK(line != nullptr);
  CHECK_EQ(addr(line) % 64, 0u);
  CHECK_EQ(a.used(), 128u);
}

CASE("fresh arena") {
  Arena a(100);
  CHECK_EQ(a.used(), 0u);
  CHECK_EQ(a.capacity(), 100u);
}

CASE("default alignment is alignof(max_align_t)") {
  Arena a(4096);
  for (int i = 0; i < 50; ++i) {
    void* p = a.allocate(1 + i % 7);
    CHECK(p != nullptr);
    CHECK_EQ(addr(p) % alignof(std::max_align_t), 0u);
  }
}

CASE("mixed alignments are all honored") {
  Arena a(1 << 16);
  std::size_t aligns[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 4096};
  for (int round = 0; round < 5; ++round)
    for (std::size_t al : aligns) {
      void* p = a.allocate(3, al);
      CHECK(p != nullptr);
      CHECK_EQ(addr(p) % al, 0u);
    }
}

CASE("exact fit succeeds, one more byte fails") {
  Arena a(64);
  CHECK(a.allocate(64, 1) != nullptr);
  CHECK_EQ(a.used(), 64u);
  CHECK(a.allocate(1, 1) == nullptr);
  a.reset();
  CHECK(a.allocate(65, 1) == nullptr);
  CHECK_EQ(a.used(), 0u);
  CHECK(a.allocate(32, 1) != nullptr);
  CHECK(a.allocate(32, 1) != nullptr);
  CHECK(a.allocate(1, 1) == nullptr);
}

CASE("padding can make an allocation fail even if size alone would fit") {
  Arena a(128);
  CHECK(a.allocate(65, 1) != nullptr);
  // 63 bytes remain, but aligning to 64 jumps to offset 128.
  CHECK(a.allocate(1, 64) == nullptr);
  CHECK_EQ(a.used(), 65u);
  CHECK(a.allocate(63, 1) != nullptr);
  CHECK_EQ(a.used(), 128u);
}

CASE("huge sizes fail cleanly (no overflow)") {
  Arena a(1024);
  a.allocate(10, 1);
  CHECK(a.allocate(SIZE_MAX, 1) == nullptr);
  CHECK(a.allocate(SIZE_MAX - 5, 8) == nullptr);
  CHECK_EQ(a.used(), 10u);
}

CASE("blocks don't overlap and stay inside the buffer") {
  Arena a(10000);
  struct Block { unsigned char* p; std::size_t n; unsigned char tag; };
  std::vector<Block> blocks;
  unsigned char tag = 1;
  std::size_t sizes[] = {1, 7, 13, 64, 3, 100, 5};
  std::size_t aligns[] = {1, 8, 16, 64, 2, 32, 4};
  unsigned char* lo = nullptr;
  for (int i = 0;; ++i) {
    std::size_t n = sizes[i % 7];
    auto* p = static_cast<unsigned char*>(a.allocate(n, aligns[i % 7]));
    if (!p) break;
    if (!lo) lo = p;
    std::memset(p, tag, n);
    blocks.push_back({p, n, tag});
    tag = static_cast<unsigned char>(tag % 250 + 1);
  }
  CHECK(blocks.size() > 50);
  CHECK(a.used() <= a.capacity());
  for (const Block& b : blocks) {
    CHECK(b.p >= lo && b.p + b.n <= lo + a.capacity());
    for (std::size_t k = 0; k < b.n; ++k) CHECK_EQ(b.p[k], b.tag);
  }
}

CASE("filling with 8-byte blocks gives exactly capacity/8 allocations, repeatedly after reset") {
  Arena a(8000);
  for (int round = 0; round < 3; ++round) {
    int count = 0;
    while (a.allocate(8, 8)) ++count;
    CHECK_EQ(count, 1000);
    CHECK_EQ(a.used(), 8000u);
    a.reset();
    CHECK_EQ(a.used(), 0u);
  }
}

CASE("zero-capacity arena never hands out memory") {
  Arena a(0);
  CHECK(a.allocate(1, 1) == nullptr);
  CHECK_EQ(a.used(), 0u);
}
