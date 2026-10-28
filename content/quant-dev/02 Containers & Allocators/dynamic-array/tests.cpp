#include "qtest.h"
#include "attempt.cpp"
#include <set>
#include <string>

// No default constructor; counts live objects and copies.
struct Tracked {
  static inline int alive = 0, copies = 0;
  int v;
  explicit Tracked(int x) : v(x) { ++alive; }
  Tracked(const Tracked& o) : v(o.v) { ++alive; ++copies; }
  Tracked(Tracked&& o) noexcept : v(o.v) { ++alive; o.v = -1; }
  Tracked& operator=(const Tracked& o) { v = o.v; ++copies; return *this; }
  Tracked& operator=(Tracked&& o) noexcept { v = o.v; o.v = -1; return *this; }
  ~Tracked() { --alive; }
  static void clear() { alive = 0; copies = 0; }
};

struct Px {
  explicit Px(double p) : p(p) {}
  double p;
};

EXAMPLE("Example 1: push, emplace, index, pop, at throws") {
  Vector<int> v;
  v.push_back(1);
  v.push_back(2);
  v.emplace_back(3);
  CHECK_EQ(v.size(), 3u);
  CHECK(v.capacity() >= 3);
  CHECK_EQ(v[1], 2);
  v.pop_back();
  CHECK_EQ(v.size(), 2u);
  CHECK_THROWS(v.at(5));
}

EXAMPLE("Example 2: reserve on a type without a default constructor") {
  Vector<Px> book;
  book.reserve(100);
  CHECK(book.capacity() >= 100);
  CHECK_EQ(book.size(), 0u);
  CHECK_EQ(book.emplace_back(101.5).p, 101.5);
}

CASE("empty vector") {
  Vector<int> v;
  CHECK(v.empty());
  CHECK_EQ(v.size(), 0u);
  CHECK_EQ(v.capacity(), 0u);
  CHECK_THROWS(v.at(0));
  const Vector<int>& cv = v;
  CHECK_THROWS(cv.at(0));
}

CASE("reserve constructs no objects and never shrinks") {
  Tracked::clear();
  {
    Vector<Tracked> v;
    v.reserve(50);
    CHECK_EQ(Tracked::alive, 0);
    CHECK(v.capacity() >= 50);
    v.emplace_back(1);
    v.reserve(10);
    CHECK(v.capacity() >= 50);
    CHECK_EQ(v[0].v, 1);
    CHECK_EQ(Tracked::alive, 1);
  }
  CHECK_EQ(Tracked::alive, 0);
}

CASE("live objects always equal size(): growth, pop_back, clear, destructor") {
  Tracked::clear();
  {
    Vector<Tracked> v;
    for (int i = 0; i < 1000; ++i) {
      v.emplace_back(i);
      CHECK_EQ(Tracked::alive, static_cast<int>(v.size()));
    }
    for (int i = 0; i < 300; ++i) v.pop_back();
    CHECK_EQ(Tracked::alive, 700);
    CHECK_EQ(v[699].v, 699);
    std::size_t cap = v.capacity();
    v.clear();
    CHECK_EQ(Tracked::alive, 0);
    CHECK(v.empty());
    CHECK_EQ(v.capacity(), cap);
    v.emplace_back(5);
  }
  CHECK_EQ(Tracked::alive, 0);
}

CASE("growth is geometric: few distinct capacities over 100000 pushes") {
  Vector<int> v;
  std::set<std::size_t> caps;
  for (int i = 0; i < 100000; ++i) {
    v.push_back(i);
    CHECK(v.capacity() >= v.size());
    caps.insert(v.capacity());
  }
  CHECK(caps.size() <= 40);
  long long sum = 0;
  for (std::size_t i = 0; i < v.size(); ++i) sum += v[i];
  CHECK_EQ(sum, 99999LL * 100000LL / 2);
}

CASE("push_back of its own element survives reallocation") {
  Vector<std::string> v;
  v.push_back("first-element-long-enough-to-allocate");
  for (int i = 0; i < 20; ++i) {
    v.push_back(v[0]);
    v.push_back(v.at(v.size() - 1));
  }
  CHECK_EQ(v.size(), 41u);
  for (std::size_t i = 0; i < v.size(); ++i) CHECK_EQ(v[i], std::string("first-element-long-enough-to-allocate"));
}

CASE("copy is deep, move steals without touching elements") {
  Tracked::clear();
  {
    Vector<Tracked> a;
    for (int i = 0; i < 10; ++i) a.emplace_back(i);
    Vector<Tracked> b(a);
    CHECK_EQ(Tracked::alive, 20);
    b[0].v = 100;
    CHECK_EQ(a[0].v, 0);
    int copies_before = Tracked::copies, alive_before = Tracked::alive;
    Vector<Tracked> c(std::move(a));
    CHECK_EQ(Tracked::copies, copies_before);
    CHECK_EQ(Tracked::alive, alive_before);
    CHECK_EQ(a.size(), 0u);
    CHECK_EQ(c.size(), 10u);
    CHECK_EQ(c[9].v, 9);
    Vector<Tracked> d;
    d.emplace_back(-5);
    d = c;  // copy assignment releases d's old element
    CHECK_EQ(d.size(), 10u);
    CHECK_EQ(Tracked::alive, 30);
    d = std::move(b);
    CHECK_EQ(d[0].v, 100);
    CHECK_EQ(Tracked::alive, 20);
  }
  CHECK_EQ(Tracked::alive, 0);
}

CASE("self-assignment keeps contents") {
  Vector<int> v;
  for (int i = 0; i < 5; ++i) v.push_back(i * i);
  Vector<int>& alias = v;
  v = alias;
  CHECK_EQ(v.size(), 5u);
  CHECK_EQ(v[4], 16);
  v = std::move(alias);
  CHECK_EQ(v.size(), 5u);
  CHECK_EQ(v[3], 9);
}

CASE("push_back(T&&) moves instead of copying") {
  Tracked::clear();
  {
    Vector<Tracked> v;
    v.reserve(4);
    Tracked t(7);
    v.push_back(std::move(t));
    CHECK_EQ(Tracked::copies, 0);
    CHECK_EQ(t.v, -1);
    v.push_back(t);
    CHECK_EQ(Tracked::copies, 1);
    CHECK_EQ(v[0].v, 7);
  }
  CHECK_EQ(Tracked::alive, 0);
}

CASE("at checks bounds on both sides of size()") {
  Vector<int> v;
  v.reserve(10);
  v.push_back(42);
  CHECK_EQ(v.at(0), 42);
  CHECK_THROWS(v.at(1));  // within capacity but past size
  v.at(0) = 43;
  CHECK_EQ(v[0], 43);
  bool right_type = false;
  try { v.at(100); } catch (const std::out_of_range&) { right_type = true; }
  CHECK(right_type);
}
