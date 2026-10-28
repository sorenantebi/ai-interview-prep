#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <random>
#include <string>
#include <vector>

EXAMPLE("Example 1: get refreshes recency, put evicts the least recent") {
  LRUCache<int, std::string> c(2);
  c.put(1, "one");
  c.put(2, "two");
  CHECK_EQ(c.get(1), std::optional<std::string>("one"));
  c.put(3, "three");
  CHECK(!c.get(2).has_value());
  CHECK_EQ(c.get(3), std::optional<std::string>("three"));
  CHECK_EQ(c.size(), 2u);
}

EXAMPLE("Example 2: updating a key counts as a use") {
  LRUCache<std::string, double> vol(2);
  vol.put("AAPL", 0.25);
  vol.put("MSFT", 0.22);
  vol.put("AAPL", 0.27);
  vol.put("NVDA", 0.55);
  CHECK(!vol.contains("MSFT"));
  CHECK_EQ(vol.get("AAPL"), std::optional<double>(0.27));
}

CASE("empty cache") {
  LRUCache<int, int> c(3);
  CHECK_EQ(c.size(), 0u);
  CHECK(!c.get(1).has_value());
  CHECK(!c.contains(1));
}

CASE("capacity 1 keeps only the latest key") {
  LRUCache<int, int> c(1);
  c.put(1, 10);
  c.put(2, 20);
  CHECK(!c.contains(1));
  CHECK_EQ(c.get(2), std::optional<int>(20));
  c.put(2, 21);
  CHECK_EQ(c.size(), 1u);
  CHECK_EQ(c.get(2), std::optional<int>(21));
}

CASE("update does not grow the cache or evict") {
  LRUCache<int, int> c(3);
  c.put(1, 1); c.put(2, 2); c.put(3, 3);
  for (int i = 0; i < 10; ++i) c.put(2, 100 + i);
  CHECK_EQ(c.size(), 3u);
  CHECK(c.contains(1));
  CHECK(c.contains(3));
  CHECK_EQ(c.get(2), std::optional<int>(109));
}

CASE("contains does not change the recency order") {
  LRUCache<int, int> c(2);
  c.put(1, 1);
  c.put(2, 2);
  CHECK(c.contains(1));  // must NOT refresh 1
  c.put(3, 3);           // so 1 is evicted
  CHECK(!c.contains(1));
  CHECK(c.contains(2));
  CHECK(c.contains(3));
}

CASE("a missed get does not change anything") {
  LRUCache<int, int> c(2);
  c.put(1, 1);
  c.put(2, 2);
  CHECK(!c.get(7).has_value());
  c.put(3, 3);
  CHECK(!c.contains(1));
  CHECK_EQ(c.size(), 2u);
}

CASE("eviction order follows a long access sequence") {
  LRUCache<int, int> c(3);
  c.put(1, 1); c.put(2, 2); c.put(3, 3);
  c.get(1);      // order (recent first): 1 3 2
  c.put(4, 4);   // evicts 2 -> 4 1 3
  c.get(3);      // 3 4 1
  c.put(5, 5);   // evicts 1 -> 5 3 4
  CHECK(!c.contains(2));
  CHECK(!c.contains(1));
  CHECK(c.contains(3) && c.contains(4) && c.contains(5));
  c.put(6, 6);   // evicts 4
  CHECK(!c.contains(4));
}

CASE("100000 random operations match a simple reference model") {
  const std::size_t cap = 8;
  LRUCache<int, int> c(cap);
  std::vector<std::pair<int, int>> model;  // front = most recent; O(cap) per op, fine for cap 8
  std::mt19937 rng(7);
  for (int step = 0; step < 100000; ++step) {
    int key = static_cast<int>(rng() % 20);
    auto it = std::find_if(model.begin(), model.end(), [&](auto& p) { return p.first == key; });
    if (rng() % 2) {
      int val = static_cast<int>(rng() % 1000);
      if (it != model.end()) model.erase(it);
      model.insert(model.begin(), {key, val});
      if (model.size() > cap) model.pop_back();
      c.put(key, val);
    } else {
      std::optional<int> want;
      if (it != model.end()) {
        want = it->second;
        auto p = *it;
        model.erase(it);
        model.insert(model.begin(), p);
      }
      CHECK_EQ(c.get(key), want);
    }
    CHECK_EQ(c.size(), model.size());
  }
}

CASE("a million operations on a large cache are O(1) each") {
  LRUCache<int, int> c(100000);
  std::mt19937 rng(99);
  long long hits = 0;
  for (int i = 0; i < 1000000; ++i) {
    int key = static_cast<int>(rng() % 200000);
    if (auto v = c.get(key)) {
      CHECK_EQ(*v, key * 2);
      ++hits;
    } else {
      c.put(key, key * 2);
    }
  }
  CHECK_EQ(c.size(), 100000u);
  CHECK(hits > 0);
}
