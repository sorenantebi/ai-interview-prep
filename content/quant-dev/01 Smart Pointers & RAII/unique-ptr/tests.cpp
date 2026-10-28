#include "qtest.h"
#include "attempt.cpp"
#include <type_traits>
#include <vector>

// Counts live instances so the tests can prove there are no leaks and no double deletes.
struct Order {
  static inline int alive = 0, destroyed = 0;
  int id;
  explicit Order(int i) : id(i) { ++alive; }
  ~Order() { --alive; ++destroyed; }
  static void clear() { alive = 0; destroyed = 0; }
};

EXAMPLE("Example 1: owns the object and deletes it once at scope exit") {
  Order::clear();
  {
    UniquePtr<Order> p(new Order{42});
    CHECK_EQ(p->id, 42);
    (*p).id = 7;
    CHECK_EQ(p->id, 7);
    CHECK(bool(p));
    CHECK_EQ(Order::alive, 1);
  }
  CHECK_EQ(Order::alive, 0);
  CHECK_EQ(Order::destroyed, 1);
}

EXAMPLE("Example 2: move construction and move assignment transfer ownership") {
  UniquePtr<int> a(new int(5));
  UniquePtr<int> b(std::move(a));
  CHECK(!a);
  CHECK_EQ(*b, 5);
  a = std::move(b);
  CHECK_EQ(*a, 5);
  CHECK(!b);
}

CASE("default-constructed pointer is empty") {
  UniquePtr<Order> p;
  CHECK(!p);
  CHECK(p.get() == nullptr);
  UniquePtr<Order> q(nullptr);
  CHECK(!q);
}

CASE("release gives up ownership without deleting") {
  Order::clear();
  Order* raw = nullptr;
  {
    UniquePtr<Order> p(new Order{1});
    raw = p.release();
    CHECK(!p);
    CHECK(p.get() == nullptr);
  }
  CHECK_EQ(Order::alive, 1);
  CHECK_EQ(raw->id, 1);
  delete raw;
  CHECK_EQ(Order::alive, 0);
}

CASE("reset deletes the old object and owns the new one") {
  Order::clear();
  UniquePtr<Order> p(new Order{1});
  p.reset(new Order{2});
  CHECK_EQ(Order::destroyed, 1);
  CHECK_EQ(p->id, 2);
  p.reset();
  CHECK_EQ(Order::destroyed, 2);
  CHECK_EQ(Order::alive, 0);
  CHECK(!p);
  p.reset();  // resetting an empty pointer is a no-op
  CHECK_EQ(Order::destroyed, 2);
}

CASE("move assignment frees the previously owned object") {
  Order::clear();
  {
    UniquePtr<Order> a(new Order{1});
    UniquePtr<Order> b(new Order{2});
    a = std::move(b);
    CHECK_EQ(Order::destroyed, 1);
    CHECK_EQ(a->id, 2);
    CHECK(!b);
    CHECK_EQ(Order::alive, 1);
  }
  CHECK_EQ(Order::alive, 0);
  CHECK_EQ(Order::destroyed, 2);
}

CASE("self move-assignment keeps the object alive") {
  Order::clear();
  {
    UniquePtr<Order> p(new Order{9});
    UniquePtr<Order>& alias = p;
    p = std::move(alias);
    CHECK(bool(p));
    CHECK_EQ(p->id, 9);
    CHECK_EQ(Order::alive, 1);
    CHECK_EQ(Order::destroyed, 0);
  }
  CHECK_EQ(Order::destroyed, 1);
}

CASE("move-only and nothrow-movable") {
  CHECK(!std::is_copy_constructible_v<UniquePtr<Order>>);
  CHECK(!std::is_copy_assignable_v<UniquePtr<Order>>);
  CHECK(std::is_nothrow_move_constructible_v<UniquePtr<Order>>);
  CHECK(std::is_nothrow_move_assignable_v<UniquePtr<Order>>);
}

CASE("moving from an empty pointer leaves both empty") {
  UniquePtr<int> a;
  UniquePtr<int> b(std::move(a));
  CHECK(!a);
  CHECK(!b);
  UniquePtr<int> c(new int(3));
  c = std::move(a);
  CHECK(!c);
}

CASE("a vector of 1000 pointers reallocates and still deletes each object once") {
  Order::clear();
  {
    std::vector<UniquePtr<Order>> v;
    for (int i = 0; i < 1000; ++i) v.push_back(UniquePtr<Order>(new Order{i}));
    CHECK_EQ(Order::alive, 1000);
    CHECK_EQ(Order::destroyed, 0);
    long sum = 0;
    for (auto& p : v) sum += p->id;
    CHECK_EQ(sum, 999L * 1000L / 2);
    v.erase(v.begin(), v.begin() + 500);
    CHECK_EQ(Order::alive, 500);
    CHECK_EQ(v.front()->id, 500);
  }
  CHECK_EQ(Order::alive, 0);
  CHECK_EQ(Order::destroyed, 1000);
}
