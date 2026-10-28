#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <limits>
#include <mutex>
#include <thread>
#include <vector>

EXAMPLE("Example 1: update_max keeps the larger value") {
  std::atomic<std::int64_t> worst{120};
  CHECK_EQ(update_max(worst, 95), (std::int64_t)120);
  CHECK_EQ(worst.load(), (std::int64_t)120);
  CHECK_EQ(update_max(worst, 340), (std::int64_t)120);
  CHECK_EQ(worst.load(), (std::int64_t)340);
}

EXAMPLE("Example 2: fetch_multiply returns the old value") {
  std::atomic<std::int64_t> x{3};
  CHECK_EQ(fetch_multiply(x, 5), (std::int64_t)3);
  CHECK_EQ(x.load(), (std::int64_t)15);
  CHECK_EQ(fetch_multiply(x, -2), (std::int64_t)15);
  CHECK_EQ(x.load(), (std::int64_t)-30);
}

EXAMPLE("Example 3: 4 threads x 10 doublings lose nothing") {
  std::atomic<std::int64_t> x{1};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] { for (int i = 0; i < 10; ++i) fetch_multiply(x, 2); });
  for (auto& t : ts) t.join();
  CHECK_EQ(x.load(), (std::int64_t)1 << 40);
}

CASE("update_max with equal value returns it and changes nothing") {
  std::atomic<std::int64_t> a{7};
  CHECK_EQ(update_max(a, 7), (std::int64_t)7);
  CHECK_EQ(a.load(), (std::int64_t)7);
}

CASE("update_max works with negatives and the minimum value") {
  std::atomic<std::int64_t> a{std::numeric_limits<std::int64_t>::min()};
  CHECK_EQ(update_max(a, -50), std::numeric_limits<std::int64_t>::min());
  CHECK_EQ(update_max(a, -80), (std::int64_t)-50);
  CHECK_EQ(a.load(), (std::int64_t)-50);
  update_max(a, 0);
  CHECK_EQ(a.load(), (std::int64_t)0);
}

CASE("fetch_multiply by 0 and by 1") {
  std::atomic<std::int64_t> a{42};
  CHECK_EQ(fetch_multiply(a, 1), (std::int64_t)42);
  CHECK_EQ(a.load(), (std::int64_t)42);
  CHECK_EQ(fetch_multiply(a, 0), (std::int64_t)42);
  CHECK_EQ(a.load(), (std::int64_t)0);
}

static std::int64_t mix(std::int64_t x) {  // deterministic pseudo-random values
  std::uint64_t u = (std::uint64_t)x;
  u = (u ^ (u >> 31)) * 0x7fb5d329728ea185ULL;
  return (std::int64_t)((u ^ (u >> 27)) % 1000000007ULL);
}

CASE("8 threads racing update_max end at the true maximum (3 runs)") {
  for (int rep = 0; rep < 3; ++rep) {
    std::atomic<std::int64_t> best{std::numeric_limits<std::int64_t>::min()};
    std::int64_t expected = std::numeric_limits<std::int64_t>::min();
    for (int t = 0; t < 8; ++t)
      for (int i = 0; i < 50000; ++i) expected = std::max(expected, mix(rep * 1000003LL + t * 50000LL + i));
    std::vector<std::thread> ts;
    for (int t = 0; t < 8; ++t)
      ts.emplace_back([&, t] {
        for (int i = 0; i < 50000; ++i) update_max(best, mix(rep * 1000003LL + t * 50000LL + i));
      });
    for (auto& t : ts) t.join();
    CHECK_EQ(best.load(), expected);
  }
}

CASE("update_max return values: each thread sees a non-decreasing history") {
  std::atomic<std::int64_t> best{0};
  std::atomic<bool> bad{false};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&, t] {
      std::int64_t last = 0;
      for (int i = 0; i < 50000; ++i) {
        std::int64_t prev = update_max(best, i * 4 + t);
        if (prev < last) bad = true;
        last = std::max(prev, (std::int64_t)(i * 4 + t));
      }
    });
  for (auto& t : ts) t.join();
  CHECK(!bad.load());
  CHECK_EQ(best.load(), (std::int64_t)(49999 * 4 + 3));
}

CASE("concurrent doublings return every power of two exactly once (3 runs)") {
  for (int rep = 0; rep < 3; ++rep) {
    std::atomic<std::int64_t> x{1};
    std::mutex m;
    std::vector<std::int64_t> olds;
    std::vector<std::thread> ts;
    for (int t = 0; t < 6; ++t)
      ts.emplace_back([&] {
        std::vector<std::int64_t> mine;
        for (int i = 0; i < 10; ++i) mine.push_back(fetch_multiply(x, 2));
        std::lock_guard<std::mutex> g(m);
        olds.insert(olds.end(), mine.begin(), mine.end());
      });
    for (auto& t : ts) t.join();
    std::sort(olds.begin(), olds.end());
    std::vector<std::int64_t> want;
    for (int k = 0; k < 60; ++k) want.push_back((std::int64_t)1 << k);
    CHECK_EQ(olds, want);
    CHECK_EQ(x.load(), (std::int64_t)1 << 60);
  }
}

CASE("alternating multiply by -1 from many threads") {
  std::atomic<std::int64_t> x{5};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] { for (int i = 0; i < 25001; ++i) fetch_multiply(x, -1); });
  for (auto& t : ts) t.join();
  CHECK_EQ(x.load(), (std::int64_t)5);  // 100004 flips: even
}
