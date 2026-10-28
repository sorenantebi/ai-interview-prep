#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <map>
#include <random>

using OI = std::optional<int>;

EXAMPLE("Example 1: median, mode and percentiles") {
  BoundedStats s(0, 10);
  for (int x : {3, 1, 4, 1, 5, 9, 2, 6}) s.add(x);
  CHECK_EQ(s.count(), 8u);
  CHECK_NEAR(s.median().value_or(-1), 3.5, 1e-12);
  CHECK_EQ(s.mode(), OI(1));
  CHECK_EQ(s.percentile(25), OI(1));
  CHECK_EQ(s.percentile(90), OI(9));
  CHECK_EQ(s.percentile(0), OI(1));
}

EXAMPLE("Example 2: empty mode, tie breaking, out of range") {
  BoundedStats s(-5, 5);
  CHECK(!s.mode().has_value());
  s.add(-5); s.add(5); s.add(5); s.add(-5);
  CHECK_EQ(s.mode(), OI(-5));
  CHECK_THROWS(s.add(6));
}

CASE("empty stream returns nullopt everywhere") {
  BoundedStats s(1, 1);
  CHECK_EQ(s.count(), 0u);
  CHECK(!s.median().has_value());
  CHECK(!s.mode().has_value());
  CHECK(!s.percentile(50).has_value());
}

CASE("out-of-range values throw out_of_range and are not counted") {
  BoundedStats s(10, 20);
  bool threw = false;
  try { s.add(9); } catch (const std::out_of_range&) { threw = true; }
  CHECK(threw);
  CHECK_THROWS(s.add(21));
  CHECK_THROWS(s.add(-2147483647 - 1));
  CHECK_THROWS(s.add(2147483647));
  s.add(10); s.add(20);
  CHECK_EQ(s.count(), 2u);
  CHECK_NEAR(s.median().value_or(-1), 15.0, 1e-12);
}

CASE("odd count median, p100 is the max, single value range") {
  BoundedStats s(0, 1000);
  for (int x : {1000, 0, 500}) s.add(x);
  CHECK_NEAR(s.median().value_or(-1), 500.0, 1e-12);
  CHECK_EQ(s.percentile(100), OI(1000));
  CHECK_EQ(s.percentile(66.7), OI(1000));  // ceil(2.001) = 3
  CHECK_EQ(s.percentile(66.6), OI(500));   // ceil(1.998) = 2
  BoundedStats one(7, 7);
  for (int i = 0; i < 5; ++i) one.add(7);
  CHECK_EQ(one.mode(), OI(7));
  CHECK_EQ(one.percentile(37), OI(7));
}

CASE("mode updates as counts change and prefers the smaller value on ties") {
  BoundedStats s(0, 9);
  s.add(8);
  CHECK_EQ(s.mode(), OI(8));
  s.add(3);
  CHECK_EQ(s.mode(), OI(3));
  s.add(8);
  CHECK_EQ(s.mode(), OI(8));
  s.add(3);
  CHECK_EQ(s.mode(), OI(3));
  s.add(9); s.add(9); s.add(9);
  CHECK_EQ(s.mode(), OI(9));
}

CASE("negative ranges and exact percentile boundaries") {
  BoundedStats s(-1000, 0);
  for (int x = -100; x < 0; ++x) s.add(x);  // 100 values: -100..-1
  CHECK_EQ(s.percentile(1), OI(-100));
  CHECK_EQ(s.percentile(10), OI(-91));  // k = 10 exactly
  CHECK_EQ(s.percentile(10.5), OI(-90));
  CHECK_EQ(s.percentile(99), OI(-2));
  CHECK_NEAR(s.median().value_or(1), -50.5, 1e-12);
}

CASE("random streams match sorting") {
  std::mt19937 rng(4242);
  for (int trial = 0; trial < 50; ++trial) {
    int lo = std::uniform_int_distribution<int>(-500, 500)(rng);
    int hi = lo + std::uniform_int_distribution<int>(0, 1000)(rng);
    BoundedStats s(lo, hi);
    std::vector<int> v;
    std::map<int, int> freq;
    int n = std::uniform_int_distribution<int>(1, 2000)(rng);
    for (int i = 0; i < n; ++i) {
      int x = std::uniform_int_distribution<int>(lo, std::min(hi, lo + 30))(rng);
      s.add(x);
      v.push_back(x);
      ++freq[x];
    }
    std::sort(v.begin(), v.end());
    CHECK_NEAR(s.median().value_or(1e9), (v[(n - 1) / 2] + static_cast<double>(v[n / 2])) / 2, 1e-9);
    int best = v[0];
    for (auto [x, c] : freq) if (c > freq[best]) best = x;
    CHECK_EQ(s.mode(), OI(best));
    for (int p = 0; p <= 100; p += 5) {
      long k = std::max(1L, (static_cast<long>(p) * n + 99) / 100);
      CHECK_EQ(s.percentile(p), OI(v[k - 1]));
    }
  }
}

CASE("ten million adds and ten thousand percentile queries stay fast") {
  BoundedStats s(0, 1000);
  for (int i = 0; i < 10000000; ++i) s.add(i % 1001);
  CHECK_EQ(s.count(), 10000000u);
  CHECK_EQ(s.mode(), OI(0));
  CHECK_EQ(s.percentile(100), OI(1000));
  for (int q = 0; q < 10000; ++q) CHECK(s.percentile(q % 101).has_value());
}
