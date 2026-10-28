#include "qtest.h"
#include "attempt.cpp"
#include <random>
#include <tuple>
#include <vector>

EXAMPLE("Example 1: VWAP as trades expire") {
  SlidingVwap v(100);
  CHECK(!v.vwap(0).has_value());
  v.on_trade(10, 200, 1);
  v.on_trade(20, 100, 3);
  auto a = v.vwap(20);
  CHECK(a.has_value());
  CHECK_NEAR(*a, 125.0, 1e-9);
  CHECK_NEAR(v.vwap(109).value_or(-1), 125.0, 1e-9);
  CHECK_NEAR(v.vwap(110).value_or(-1), 100.0, 1e-9);
  CHECK(!v.vwap(120).has_value());
}

EXAMPLE("Example 2: two trades at the same timestamp") {
  SlidingVwap v(1000);
  v.on_trade(0, 101, 2);
  v.on_trade(0, 102, 1);
  CHECK_NEAR(v.vwap(0).value_or(-1), 304.0 / 3.0, 1e-9);
}

CASE("single trade: visible for exactly window_ns") {
  SlidingVwap v(5);
  v.on_trade(100, 42, 7);
  CHECK_NEAR(v.vwap(100).value_or(-1), 42.0, 1e-9);
  CHECK_NEAR(v.vwap(104).value_or(-1), 42.0, 1e-9);
  CHECK(!v.vwap(105).has_value());
}

CASE("window refills after going empty") {
  SlidingVwap v(10);
  v.on_trade(0, 50, 1);
  CHECK(!v.vwap(100).has_value());
  v.on_trade(100, 60, 1);
  v.on_trade(105, 90, 2);
  CHECK_NEAR(v.vwap(105).value_or(-1), (60.0 + 180.0) / 3.0, 1e-9);
  CHECK_NEAR(v.vwap(110).value_or(-1), 90.0, 1e-9);
}

CASE("expiry also happens on on_trade-only streams") {
  SlidingVwap v(3);
  for (std::uint64_t t = 0; t < 100; ++t) v.on_trade(t, static_cast<std::int64_t>(t + 1), 1);
  // window at 99 holds trades at 97, 98, 99 with prices 98, 99, 100
  CHECK_NEAR(v.vwap(99).value_or(-1), 99.0, 1e-9);
}

CASE("weights by quantity, not by trade count") {
  SlidingVwap v(1000);
  v.on_trade(1, 100, 99);
  v.on_trade(2, 200, 1);
  CHECK_NEAR(v.vwap(2).value_or(-1), 101.0, 1e-9);
}

CASE("large timestamps, prices and quantities stay exact") {
  SlidingVwap v(1000000000000ULL);
  const std::uint64_t base = 1000000000000000000ULL;
  for (int i = 0; i < 1000; ++i) v.on_trade(base + i, 10000000 - i % 2, 100000);
  CHECK_NEAR(v.vwap(base + 1000).value_or(-1), 9999999.5, 1e-9);
  CHECK_NEAR(v.vwap(base + 1000000000000ULL).value_or(-1), (499.0 * 10000000 + 500.0 * 9999999) / 999.0, 1e-6);
  CHECK(!v.vwap(base + 2000000000000ULL).has_value());
}

CASE("random stream matches a brute-force recomputation") {
  std::mt19937_64 rng(31337);
  auto rnd = [&](long lo, long hi) { return std::uniform_int_distribution<long>(lo, hi)(rng); };
  const std::uint64_t W = 40;
  SlidingVwap v(W);
  std::vector<std::tuple<std::uint64_t, long, long>> all;
  std::uint64_t now = 0;
  for (int i = 0; i < 20000; ++i) {
    now += rnd(0, 5);
    if (rnd(0, 2)) {
      long p = rnd(1, 1000), q = rnd(1, 50);
      v.on_trade(now, p, q);
      all.emplace_back(now, p, q);
    } else {
      long num = 0, den = 0;
      for (auto it = all.rbegin(); it != all.rend() && now - std::get<0>(*it) < W; ++it) {
        num += std::get<1>(*it) * std::get<2>(*it);
        den += std::get<2>(*it);
      }
      auto got = v.vwap(now);
      CHECK_EQ(got.has_value(), den > 0);
      if (den > 0) CHECK_NEAR(*got, static_cast<double>(num) / den, 1e-9);
    }
  }
}

CASE("two million updates stay fast") {
  SlidingVwap v(1000);
  double last = 0;
  for (std::uint64_t t = 0; t < 1000000; ++t) {
    v.on_trade(t, 100 + static_cast<std::int64_t>(t % 3), 1);
    last = v.vwap(t).value_or(-1);
  }
  CHECK_NEAR(last, 100.999, 1e-9);  // window 999000..999999: 334 x 100, 333 x 101, 333 x 102
}
