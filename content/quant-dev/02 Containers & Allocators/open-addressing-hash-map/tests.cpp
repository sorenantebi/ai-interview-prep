#include "qtest.h"
#include "attempt.cpp"
#include <climits>
#include <random>
#include <string>
#include <unordered_map>

EXAMPLE("Example 1: insert, overwrite, find, erase") {
  HashMap<double> px;
  CHECK_EQ(px.insert(1001, 99.5), true);
  CHECK_EQ(px.insert(1002, 100.0), true);
  CHECK_EQ(px.insert(1001, 99.75), false);
  CHECK(px.find(1001) != nullptr);
  CHECK_EQ(*px.find(1001), 99.75);
  CHECK(px.find(7) == nullptr);
  CHECK_EQ(px.erase(1001), true);
  CHECK_EQ(px.erase(1001), false);
  CHECK_EQ(px.size(), 1u);
}

EXAMPLE("Example 2: grows automatically, load factor stays <= 0.7") {
  HashMap<int> m;
  for (int i = 0; i < 1000; ++i) m.insert(i, i * i);
  CHECK_EQ(m.size(), 1000u);
  CHECK(m.size() <= 0.7 * m.capacity());
  CHECK(m.find(999) != nullptr);
  CHECK_EQ(*m.find(999), 998001);
}

CASE("empty map") {
  HashMap<int> m;
  CHECK_EQ(m.size(), 0u);
  CHECK(m.capacity() > 0);
  CHECK((m.capacity() & (m.capacity() - 1)) == 0);
  CHECK(m.find(0) == nullptr);
  CHECK(!m.erase(0));
  const HashMap<int>& cm = m;
  CHECK(cm.find(0) == nullptr);
}

CASE("extreme keys: 0, negatives, INT64_MIN, INT64_MAX") {
  HashMap<int> m;
  std::int64_t keys[] = {0, -1, 1, INT64_MIN, INT64_MAX, INT64_MIN + 1, INT64_MAX - 1, -42};
  int v = 0;
  for (auto k : keys) CHECK(m.insert(k, v++));
  CHECK_EQ(m.size(), 8u);
  v = 0;
  for (auto k : keys) {
    CHECK(m.find(k) != nullptr);
    CHECK_EQ(*m.find(k), v++);
  }
  CHECK(m.erase(INT64_MIN));
  CHECK(m.find(INT64_MIN) == nullptr);
  CHECK(m.find(0) != nullptr);
}

CASE("find returns a pointer you can write through") {
  HashMap<std::string> m;
  m.insert(5, "new");
  *m.find(5) += "-filled";
  CHECK_EQ(*m.find(5), std::string("new-filled"));
}

CASE("load factor <= 0.7 after every insert") {
  HashMap<int> m;
  for (int i = 0; i < 20000; ++i) {
    m.insert(static_cast<std::int64_t>(i) * 7919, i);
    CHECK(m.size() * 10 <= m.capacity() * 7);
  }
  for (int i = 0; i < 20000; ++i) CHECK_EQ(*m.find(static_cast<std::int64_t>(i) * 7919), i);
}

CASE("keys behind an erased key are still found (tombstones)") {
  HashMap<int> m;
  for (int i = 0; i < 10; ++i) m.insert(i, i);
  for (int i = 0; i < 10; i += 2) CHECK(m.erase(i));
  for (int i = 1; i < 10; i += 2) {
    CHECK(m.find(i) != nullptr);
    CHECK_EQ(*m.find(i), i);
  }
  for (int i = 0; i < 10; i += 2) CHECK(m.find(i) == nullptr);
  CHECK(m.insert(4, 40));
  CHECK_EQ(*m.find(4), 40);
  CHECK_EQ(m.size(), 6u);
}

CASE("insert/erase churn keeps capacity bounded and lookups terminating") {
  HashMap<int> m;
  for (int i = 0; i < 10; ++i) m.insert(i, i);
  for (int i = 10; i < 200000; ++i) {
    CHECK(m.erase(i - 10));
    CHECK(m.insert(i, i));
  }
  CHECK_EQ(m.size(), 10u);
  CHECK(m.capacity() <= 1024);
  CHECK(m.find(-5) == nullptr);  // must stop: there are still empty slots
  for (int i = 199990; i < 200000; ++i) CHECK_EQ(*m.find(i), i);
}

CASE("patterned keys (multiples of 2^20) stay fast") {
  HashMap<int> m;
  const int n = 200000;
  for (int i = 0; i < n; ++i) m.insert(static_cast<std::int64_t>(i) << 20, i);
  CHECK_EQ(m.size(), static_cast<std::size_t>(n));
  long long sum = 0;
  for (int i = 0; i < n; ++i) sum += *m.find(static_cast<std::int64_t>(i) << 20);
  CHECK_EQ(sum, static_cast<long long>(n - 1) * n / 2);
  CHECK(m.find((static_cast<std::int64_t>(n) << 20) + 1) == nullptr);
}

CASE("300000 random operations match std::unordered_map") {
  HashMap<std::int64_t> m;
  std::unordered_map<std::int64_t, std::int64_t> oracle;
  std::mt19937_64 rng(20240607);
  for (int step = 0; step < 300000; ++step) {
    std::uint64_t r = rng();
    std::int64_t key = static_cast<std::int64_t>(r % 5000) - 2500;
    std::int64_t val = static_cast<std::int64_t>(r >> 20);
    switch ((r >> 13) % 4) {
      case 0:
      case 1: {
        bool fresh = oracle.find(key) == oracle.end();
        oracle[key] = val;
        CHECK_EQ(m.insert(key, val), fresh);
        break;
      }
      case 2:
        CHECK_EQ(m.erase(key), oracle.erase(key) == 1);
        break;
      default: {
        auto it = oracle.find(key);
        std::int64_t* got = m.find(key);
        CHECK_EQ(got != nullptr, it != oracle.end());
        if (got) CHECK_EQ(*got, it->second);
      }
    }
    CHECK_EQ(m.size(), oracle.size());
  }
  for (auto& [k, v] : oracle) CHECK_EQ(*m.find(k), v);
}
