#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <memory>
#include <set>
#include <stdexcept>
#include <vector>

// No default constructor; counts constructions and destructions.
struct Order {
  static inline int constructed = 0, destroyed = 0;
  int id;
  double price;
  Order(int i, double p) : id(i), price(p) { ++constructed; }
  ~Order() { ++destroyed; }
  static void clear() { constructed = 0; destroyed = 0; }
};

EXAMPLE("Example 1: exhaust the pool, release, reuse the same slot") {
  Order::clear();
  ObjectPool<Order, 2> pool;
  Order* a = pool.acquire(1, 100.25);
  Order* b = pool.acquire(2, 100.50);
  CHECK(a != nullptr);
  CHECK(b != nullptr);
  CHECK_EQ(a->id, 1);
  CHECK_EQ(b->price, 100.50);
  CHECK(pool.acquire(3, 99.0) == nullptr);
  CHECK_EQ(pool.available(), 0u);
  pool.release(a);
  CHECK_EQ(Order::destroyed, 1);
  Order* c = pool.acquire(4, 101.0);
  CHECK(c == a);
  CHECK_EQ(c->id, 4);
}

CASE("a new pool constructs nothing and is fully available") {
  Order::clear();
  {
    ObjectPool<Order, 16> pool;
    CHECK_EQ(pool.available(), 16u);
    CHECK_EQ(pool.capacity(), 16u);
    CHECK_EQ(Order::constructed, 0);
  }
  CHECK_EQ(Order::destroyed, 0);
}

CASE("pool of one") {
  ObjectPool<int, 1> pool;
  int* p = pool.acquire(5);
  CHECK(p != nullptr);
  CHECK_EQ(*p, 5);
  CHECK(pool.acquire(6) == nullptr);
  pool.release(p);
  CHECK_EQ(pool.available(), 1u);
  int* q = pool.acquire(7);
  CHECK(q == p);
  CHECK_EQ(*q, 7);
}

CASE("acquired objects are distinct, aligned and inside no other object") {
  ObjectPool<long double, 64> pool;
  std::set<long double*> seen;
  for (int i = 0; i < 64; ++i) {
    long double* p = pool.acquire(i);
    CHECK(p != nullptr);
    CHECK_EQ(reinterpret_cast<std::uintptr_t>(p) % alignof(long double), 0u);
    seen.insert(p);
  }
  CHECK_EQ(seen.size(), 64u);
  long double expect = 0;
  for (long double* p : seen) expect += *p;
  CHECK_EQ(expect, 63.0L * 64.0L / 2);
}

CASE("free list is LIFO") {
  ObjectPool<int, 8> pool;
  int* p[8];
  for (int i = 0; i < 8; ++i) p[i] = pool.acquire(i);
  pool.release(p[2]);
  pool.release(p[5]);
  pool.release(p[0]);
  CHECK(pool.acquire(0) == p[0]);
  CHECK(pool.acquire(0) == p[5]);
  CHECK(pool.acquire(0) == p[2]);
  CHECK(pool.acquire(0) == nullptr);
}

CASE("one constructor per acquire, one destructor per release, rest at pool destruction") {
  Order::clear();
  {
    ObjectPool<Order, 10> pool;
    std::vector<Order*> held;
    for (int i = 0; i < 10; ++i) held.push_back(pool.acquire(i, 1.0));
    CHECK(pool.acquire(99, 1.0) == nullptr);
    CHECK_EQ(Order::constructed, 10);
    for (int i = 0; i < 6; ++i) pool.release(held[i]);
    CHECK_EQ(Order::destroyed, 6);
    CHECK_EQ(pool.available(), 6u);
  }
  CHECK_EQ(Order::destroyed, 10);  // the 4 still acquired are destroyed with the pool
}

struct Picky {
  static inline int alive = 0;
  explicit Picky(int x) {
    if (x < 0) throw std::invalid_argument("negative");
    ++alive;
  }
  ~Picky() { --alive; }
};

CASE("a throwing constructor leaves the slot free") {
  ObjectPool<Picky, 2> pool;
  CHECK_THROWS(pool.acquire(-1));
  CHECK_EQ(pool.available(), 2u);
  Picky* a = pool.acquire(1);
  Picky* b = pool.acquire(2);
  CHECK(a != nullptr);
  CHECK(b != nullptr);
  CHECK(a != b);
  CHECK_EQ(Picky::alive, 2);
  pool.release(a);
  pool.release(b);
  CHECK_EQ(Picky::alive, 0);
}

CASE("a million acquire/release pairs on a large pool") {
  auto pool = std::make_unique<ObjectPool<std::int64_t, 100000>>();
  std::vector<std::int64_t*> held;
  held.reserve(100000);
  std::uint64_t x = 12345;  // fixed-seed xorshift for a deterministic pattern
  long long sum = 0;
  for (int i = 0; i < 1000000; ++i) {
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    if (!held.empty() && (x % 3 == 0 || held.size() == 100000)) {
      std::size_t k = x % held.size();
      sum -= *held[k];
      pool->release(held[k]);
      held[k] = held.back();
      held.pop_back();
    } else {
      std::int64_t* p = pool->acquire(i);
      CHECK(p != nullptr);
      sum += i;
      held.push_back(p);
    }
    if (i % 100000 == 0) CHECK_EQ(pool->available(), 100000u - held.size());
  }
  long long check = 0;
  for (auto* p : held) check += *p;
  CHECK_EQ(check, sum);
  CHECK_EQ(pool->available(), 100000u - held.size());
}
