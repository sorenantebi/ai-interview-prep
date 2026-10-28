#include "qtest.h"
#include "attempt.cpp"
#include <map>
#include <random>
#include <vector>

EXAMPLE("Example 1: two messages per 100 ns") {
  Throttler t(2, 100);
  CHECK_EQ(t.allow(7, 0), true);
  CHECK_EQ(t.allow(7, 10), true);
  CHECK_EQ(t.allow(7, 50), false);
  CHECK_EQ(t.allow(7, 99), false);
  CHECK_EQ(t.allow(7, 100), true);
  CHECK_EQ(t.allow(7, 105), false);
}

EXAMPLE("Example 2: clients are independent") {
  Throttler t(1, 1000);
  CHECK_EQ(t.allow(1, 5), true);
  CHECK_EQ(t.allow(2, 5), true);
  CHECK_EQ(t.allow(1, 6), false);
}

CASE("burst at one timestamp accepts exactly N") {
  Throttler t(5, 10);
  int ok = 0;
  for (int i = 0; i < 20; ++i) ok += t.allow(1, 1000);
  CHECK_EQ(ok, 5);
  CHECK_EQ(t.allow(1, 1009), false);
  for (int i = 0; i < 5; ++i) CHECK(t.allow(1, 1010));
  CHECK_EQ(t.allow(1, 1010), false);
}

CASE("rejected messages do not count against the future") {
  Throttler t(1, 100);
  CHECK(t.allow(1, 0));
  for (int ts = 1; ts < 100; ++ts) CHECK(!t.allow(1, ts));  // all rejected
  CHECK(t.allow(1, 100));      // only the accepted one at 0 counted
  CHECK(!t.allow(1, 199));
  CHECK(t.allow(1, 200));
}

CASE("window boundary is exclusive: a message expires exactly window_ns later") {
  Throttler t(3, 50);
  CHECK(t.allow(9, 10));
  CHECK(t.allow(9, 20));
  CHECK(t.allow(9, 30));
  CHECK(!t.allow(9, 59));
  CHECK(t.allow(9, 60));       // 10 expired
  CHECK(!t.allow(9, 69));
  CHECK(t.allow(9, 70));       // 20 expired
  CHECK(t.allow(9, 80));       // 30 expired
  CHECK(!t.allow(9, 80));
}

CASE("max_msgs = 1, window 1 lets one message per nanosecond") {
  Throttler t(1, 1);
  for (std::uint64_t ts = 0; ts < 1000; ++ts) {
    CHECK(t.allow(3, ts));
    CHECK(!t.allow(3, ts));
  }
}

CASE("large timestamps near 10^18 and a long idle gap") {
  Throttler t(2, 1000000000000ULL);
  const std::uint64_t base = 1000000000000000000ULL;
  CHECK(t.allow(1, base));
  CHECK(t.allow(1, base + 1));
  CHECK(!t.allow(1, base + 999999999999ULL));
  CHECK(t.allow(1, base + 1000000000000ULL));
  CHECK(t.allow(1, base + 5000000000000ULL));
  CHECK(t.allow(1, base + 5000000000000ULL));
  CHECK(!t.allow(1, base + 5000000000000ULL));
}

CASE("random traffic from 20 clients matches a brute-force oracle") {
  std::mt19937_64 rng(77);
  const std::size_t N = 4;
  const std::uint64_t W = 50;
  Throttler t(N, W);
  std::map<std::uint64_t, std::vector<std::uint64_t>> accepted;
  std::uint64_t ts = 0;
  for (int i = 0; i < 30000; ++i) {
    ts += std::uniform_int_distribution<int>(0, 6)(rng);
    std::uint64_t c = std::uniform_int_distribution<int>(0, 19)(rng);
    std::size_t in_window = 0;
    for (auto a : accepted[c]) in_window += ts - a < W;
    bool expect = in_window < N;
    if (expect) accepted[c].push_back(ts);
    CHECK_EQ(t.allow(c, ts), expect);
  }
}

CASE("a million calls over 100000 clients stay fast") {
  Throttler t(3, 1000);
  long ok = 0;
  for (std::uint64_t i = 0; i < 1000000; ++i) ok += t.allow(i % 100000, i);
  // each client is seen every 100000 ns > window, so everything passes
  CHECK_EQ(ok, 1000000L);
  Throttler h(100000, 1000000000ULL);
  long hot = 0;
  for (std::uint64_t i = 0; i < 1000000; ++i) hot += h.allow(1, i * 10);
  CHECK_EQ(hot, 100000L);  // all 10^6 messages fall in one window: only the first 100000 pass
}
