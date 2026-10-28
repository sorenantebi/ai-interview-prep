#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <optional>
#include <string>
#include <utility>

struct Tracked {
  static inline int ctors = 0, dtors = 0, copies = 0, moves = 0;
  static void reset_counts() { ctors = dtors = copies = moves = 0; }
  static int alive() { return ctors - dtors; }
  int v;
  explicit Tracked(int v) : v(v) { ++ctors; }
  Tracked(const Tracked& o) : v(o.v) { ++ctors; ++copies; }
  Tracked(Tracked&& o) noexcept : v(o.v) { o.v = -1; ++ctors; ++moves; }
  Tracked& operator=(const Tracked& o) { v = o.v; return *this; }
  Tracked& operator=(Tracked&& o) noexcept { v = o.v; o.v = -1; return *this; }
  ~Tracked() { ++dtors; }
};

EXAMPLE("Example 1: empty, engaged, reset, value() throws") {
  Optional<int> a;
  CHECK_EQ(a.has_value(), false);
  a = Optional<int>(42);
  CHECK_EQ(a.has_value(), true);
  CHECK_EQ(*a, 42);
  a.reset();
  CHECK(!a.has_value());
  CHECK_THROWS(a.value());
}

EXAMPLE("Example 2: emplace, arrow and copy with strings") {
  Optional<std::string> s(std::string("bid"));
  CHECK_EQ(*s, std::string("bid"));
  s.emplace(3, 'x');
  CHECK_EQ(s->size(), 3u);
  Optional<std::string> t = s;
  CHECK_EQ(*t, std::string("xxx"));
  CHECK_EQ(*s, std::string("xxx"));
}

CASE("value() throws std::bad_optional_access and works when engaged") {
  Optional<int> e;
  bool threw = false;
  try { e.value(); } catch (const std::bad_optional_access&) { threw = true; }
  CHECK(threw);
  const Optional<int> c(7);
  CHECK_EQ(c.value(), 7);
  CHECK(static_cast<bool>(c));
  CHECK(!static_cast<bool>(e));
  Optional<int> m(1);
  m.value() = 5;
  CHECK_EQ(*m, 5);
}

CASE("constructors and destructor balance exactly") {
  Tracked::reset_counts();
  {
    Optional<Tracked> empty;
    CHECK_EQ(Tracked::ctors, 0);
    Optional<Tracked> a(Tracked(1));        // temp + move into storage
    CHECK_EQ(Tracked::alive(), 1);
    Optional<Tracked> b = a;                // copy
    CHECK_EQ(Tracked::copies, 1);
    Optional<Tracked> c = std::move(a);     // move; a stays engaged
    CHECK(a.has_value());
    CHECK_EQ(a->v, -1);
    CHECK_EQ(c->v, 1);
    CHECK_EQ(Tracked::alive(), 3);
    Optional<Tracked> d = empty;            // copy of empty constructs nothing
    CHECK(!d.has_value());
    CHECK_EQ(Tracked::alive(), 3);
  }
  CHECK_EQ(Tracked::alive(), 0);
}

CASE("emplace destroys the old value and constructs in place") {
  Tracked::reset_counts();
  {
    Optional<Tracked> o;
    Tracked& r = o.emplace(5);
    CHECK_EQ(r.v, 5);
    CHECK_EQ(Tracked::ctors, 1);
    CHECK_EQ(Tracked::copies + Tracked::moves, 0);
    o.emplace(6);
    CHECK_EQ(Tracked::dtors, 1);
    CHECK_EQ(Tracked::alive(), 1);
    CHECK_EQ(o->v, 6);
    CHECK_EQ(&r, &*o);                       // same storage
  }
  CHECK_EQ(Tracked::alive(), 0);
}

CASE("reset twice destroys once") {
  Tracked::reset_counts();
  Optional<Tracked> o(Tracked(1));
  o.reset();
  o.reset();
  CHECK(!o.has_value());
  CHECK_EQ(Tracked::alive(), 0);
}

CASE("copy assignment in all four engaged/empty combinations") {
  Tracked::reset_counts();
  {
    Optional<Tracked> full1(Tracked(1)), full2(Tracked(2)), empty1, empty2;
    int base = Tracked::alive();             // 2
    full1 = full2;                           // both engaged: assign
    CHECK_EQ(full1->v, 2);
    CHECK_EQ(Tracked::alive(), base);
    empty1 = full2;                          // construct
    CHECK(empty1.has_value());
    CHECK_EQ(empty1->v, 2);
    CHECK_EQ(Tracked::alive(), base + 1);
    full2 = empty2;                          // destroy
    CHECK(!full2.has_value());
    CHECK_EQ(Tracked::alive(), base);
    empty2 = full2;                          // nothing
    CHECK(!empty2.has_value());
    CHECK_EQ(Tracked::alive(), base);
  }
  CHECK_EQ(Tracked::alive(), 0);
}

CASE("move assignment and self-assignment") {
  Tracked::reset_counts();
  {
    Optional<Tracked> a(Tracked(1)), b;
    b = std::move(a);
    CHECK(b.has_value());
    CHECK_EQ(b->v, 1);
    CHECK_EQ(Tracked::alive(), 2);
    Optional<Tracked> e;
    b = std::move(e);
    CHECK(!b.has_value());
    CHECK_EQ(Tracked::alive(), 1);
    a = a;
    CHECK(a.has_value());
    Optional<Tracked>& ra = a;
    a = std::move(ra);
    CHECK(a.has_value());
    CHECK_EQ(Tracked::alive(), 1);
  }
  CHECK_EQ(Tracked::alive(), 0);
}

struct NoDefault {
  NoDefault(int a, std::string b) : a(a), b(std::move(b)) {}
  int a;
  std::string b;
};

CASE("works for types without a default constructor") {
  Optional<NoDefault> o;
  CHECK(!o.has_value());
  o.emplace(3, "ask");
  CHECK_EQ(o->a, 3);
  CHECK_EQ(o->b, std::string("ask"));
  const Optional<NoDefault>& co = o;
  CHECK_EQ((*co).b, std::string("ask"));
}

struct alignas(64) CacheLine {
  explicit CacheLine(char c) : c(c) {}
  char c;
};

CASE("storage is inline and correctly aligned") {
  Optional<CacheLine> o(CacheLine('z'));
  CHECK_EQ(reinterpret_cast<std::uintptr_t>(&*o) % 64, 0u);
  CHECK_EQ(o->c, 'z');
  CHECK(sizeof(Optional<CacheLine>) <= sizeof(CacheLine) + alignof(CacheLine));
  CHECK(sizeof(Optional<double>) <= sizeof(double) + alignof(double));
}

CASE("stress: many operations leave nothing alive") {
  Tracked::reset_counts();
  {
    Optional<Tracked> slots[8];
    unsigned seed = 12345;
    for (int i = 0; i < 20000; ++i) {
      seed = seed * 1103515245u + 12345u;
      int a = (seed >> 8) % 8, b = (seed >> 16) % 8;
      switch ((seed >> 24) % 5) {
        case 0: slots[a].emplace(i); break;
        case 1: slots[a].reset(); break;
        case 2: slots[a] = slots[b]; break;
        case 3: slots[a] = std::move(slots[b]); break;
        case 4: { Optional<Tracked> tmp(slots[b]); slots[a] = tmp; } break;
      }
    }
    int engaged = 0;
    for (auto& s : slots) engaged += s.has_value();
    CHECK_EQ(Tracked::alive(), engaged);
  }
  CHECK_EQ(Tracked::alive(), 0);
}
