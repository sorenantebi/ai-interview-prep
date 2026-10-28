#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <cstdint>
#include <thread>
#include <vector>

struct Quote { double bid, ask; };
struct Wide { std::int64_t v[8]; };   // 64 bytes: easy to tear
struct Odd { std::int32_t a; char tag; std::int16_t b; std::int32_t c; };  // size not a multiple of 8

EXAMPLE("Example 1: read returns the latest write; sequence counts writes") {
  SeqLock<Quote> q(Quote{100.25, 100.50});
  CHECK_EQ(q.sequence(), 0u);
  Quote r = q.read();
  CHECK_EQ(r.bid, 100.25);
  CHECK_EQ(r.ask, 100.50);
  q.write({100.50, 100.75});
  r = q.read();
  CHECK_EQ(r.bid, 100.50);
  CHECK_EQ(r.ask, 100.75);
  CHECK_EQ(q.sequence(), 2u);
}

// One writer writes {x, x} for x = 1..writes; readers check every value is untorn and never goes back.
template <class Make, class Check>
static long torn_reads(int readers, int writes, Make make, Check check) {
  SeqLock<decltype(make(0))> lock(make(0));
  std::atomic<bool> done{false};
  std::atomic<long> bad{0};
  std::vector<std::thread> rs;
  for (int r = 0; r < readers; ++r)
    rs.emplace_back([&] {
      std::int64_t last = 0;
      while (!done.load(std::memory_order_acquire)) {
        std::int64_t x;
        if (!check(lock.read(), x) || x < last) ++bad;
        last = x;
      }
    });
  std::thread w([&] {
    for (int x = 1; x <= writes; ++x) lock.write(make(x));
    done.store(true, std::memory_order_release);
  });
  w.join();
  for (auto& t : rs) t.join();
  std::int64_t final_x;
  if (!check(lock.read(), final_x) || final_x != writes) ++bad;
  if (lock.sequence() != 2u * writes) ++bad;
  return bad.load();
}

static Quote make_quote(int x) { return Quote{(double)x, (double)x}; }
static bool check_quote(const Quote& q, std::int64_t& x) { x = (std::int64_t)q.bid; return q.bid == q.ask; }

static Wide make_wide(int x) { Wide w; for (auto& v : w.v) v = x; return w; }
static bool check_wide(const Wide& w, std::int64_t& x) {
  x = w.v[0];
  for (auto v : w.v) if (v != x) return false;
  return true;
}

EXAMPLE("Example 2: readers never observe a torn quote") {
  CHECK_EQ(torn_reads(2, 200000, make_quote, check_quote), 0L);
}

CASE("default constructed holds T{}") {
  SeqLock<Quote> q;
  Quote r = q.read();
  CHECK_EQ(r.bid, 0.0);
  CHECK_EQ(r.ask, 0.0);
  q.write({1.5, 2.5});
  CHECK_EQ(q.read().ask, 2.5);
}

CASE("sequence goes up by 2 per write and stays even") {
  SeqLock<int> s(5);
  for (int i = 1; i <= 100; ++i) {
    s.write(i);
    CHECK_EQ(s.sequence(), (std::uint64_t)(2 * i));
    CHECK_EQ(s.read(), i);
  }
}

CASE("works for a type whose size is not a multiple of 8") {
  SeqLock<Odd> s(Odd{1, 'x', 2, 3});
  Odd r = s.read();
  CHECK_EQ(r.a, 1);
  CHECK_EQ(r.tag, 'x');
  CHECK_EQ(r.b, (std::int16_t)2);
  CHECK_EQ(r.c, 3);
  s.write(Odd{-7, 'q', -8, 9});
  r = s.read();
  CHECK_EQ(r.a, -7);
  CHECK_EQ(r.tag, 'q');
  CHECK_EQ(r.c, 9);
}

CASE("64-byte payload is copied whole") {
  SeqLock<Wide> s(make_wide(3));
  std::int64_t x;
  CHECK(check_wide(s.read(), x));
  CHECK_EQ(x, (std::int64_t)3);
  s.write(make_wide(-11));
  CHECK(check_wide(s.read(), x));
  CHECK_EQ(x, (std::int64_t)-11);
}

CASE("4 readers, 64-byte payload: no torn reads (3 runs)") {
  for (int r = 0; r < 3; ++r) CHECK_EQ(torn_reads(4, 200000, make_wide, check_wide), 0L);
}

CASE("3 readers on a Quote: no torn reads (3 runs)") {
  for (int r = 0; r < 3; ++r) CHECK_EQ(torn_reads(3, 300000, make_quote, check_quote), 0L);
}

CASE("read never writes: a const SeqLock is readable") {
  const SeqLock<Quote> q(Quote{9.0, 9.5});
  CHECK_EQ(q.read().bid, 9.0);
  CHECK_EQ(q.sequence(), 0u);
}
