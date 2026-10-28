#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <cstdlib>
#include <new>
#include <thread>
#include <vector>

// Count live heap blocks so the tests can see when the control block is freed.
static std::atomic<long> g_live_allocs{0};
void* operator new(std::size_t n) {
  void* p = std::malloc(n ? n : 1);
  if (!p) throw std::bad_alloc();
  g_live_allocs.fetch_add(1, std::memory_order_relaxed);
  return p;
}
void operator delete(void* p) noexcept {
  if (!p) return;
  g_live_allocs.fetch_sub(1, std::memory_order_relaxed);
  std::free(p);
}
void operator delete(void* p, std::size_t) noexcept { operator delete(p); }

struct Session {
  static inline std::atomic<int> alive{0}, destroyed{0};
  int id;
  explicit Session(int i) : id(i) { ++alive; }
  ~Session() { --alive; ++destroyed; }
  static void clear() { alive = 0; destroyed = 0; }
};

EXAMPLE("Example 1: lock while alive, expired after the last owner is gone") {
  Session::clear();
  WeakPtr<Session> w;
  {
    SharedPtr<Session> s(new Session{1});
    w = WeakPtr<Session>(s);
    CHECK(!w.expired());
    CHECK_EQ(w.use_count(), 1L);
    SharedPtr<Session> t = w.lock();
    CHECK_EQ(t->id, 1);
    CHECK_EQ(s.use_count(), 2L);
  }
  CHECK_EQ(Session::destroyed.load(), 1);
  CHECK(w.expired());
  CHECK(!w.lock());
}

EXAMPLE("Example 2: the object dies with the last SharedPtr, the control block with the last WeakPtr") {
  Session::clear();
  long before = g_live_allocs.load();
  SharedPtr<Session> s(new Session{2});
  WeakPtr<Session> w(s);
  s.reset();
  CHECK_EQ(Session::alive.load(), 0);
  CHECK(w.expired());
  CHECK(g_live_allocs.load() > before);  // control block still held by w
  w.reset();
  CHECK_EQ(g_live_allocs.load(), before);
}

CASE("empty pointers") {
  WeakPtr<Session> w;
  CHECK(w.expired());
  CHECK_EQ(w.use_count(), 0L);
  CHECK(!w.lock());
  SharedPtr<Session> s;
  WeakPtr<Session> w2(s);
  CHECK(w2.expired());
  CHECK(!w2.lock());
}

CASE("weak pointers never keep the object alive") {
  Session::clear();
  SharedPtr<Session> s(new Session{3});
  std::vector<WeakPtr<Session>> ws(50, WeakPtr<Session>(s));
  CHECK_EQ(s.use_count(), 1L);
  s.reset();
  CHECK_EQ(Session::destroyed.load(), 1);
  for (auto& w : ws) CHECK(w.expired());
}

CASE("lock adds a strong owner that keeps the object alive") {
  Session::clear();
  SharedPtr<Session> s(new Session{4});
  WeakPtr<Session> w(s);
  SharedPtr<Session> locked = w.lock();
  CHECK_EQ(s.use_count(), 2L);
  s.reset();
  CHECK_EQ(Session::alive.load(), 1);
  CHECK(!w.expired());
  CHECK_EQ(locked->id, 4);
  locked.reset();
  CHECK_EQ(Session::alive.load(), 0);
  CHECK_EQ(Session::destroyed.load(), 1);
  CHECK(w.expired());
}

CASE("control block outlives the object when the weak pointer is last, and vice versa") {
  Session::clear();
  long before = g_live_allocs.load();
  {
    // Weak pointers die first: block freed together with the object.
    SharedPtr<Session> s(new Session{5});
    { WeakPtr<Session> w1(s); WeakPtr<Session> w2 = w1; }
    CHECK_EQ(Session::alive.load(), 1);
  }
  CHECK_EQ(Session::alive.load(), 0);
  CHECK_EQ(g_live_allocs.load(), before);
  {
    // Weak pointer dies last: block freed only then.
    WeakPtr<Session> w;
    {
      SharedPtr<Session> s(new Session{6});
      w = WeakPtr<Session>(s);
    }
    CHECK_EQ(Session::alive.load(), 0);
    CHECK(g_live_allocs.load() > before);
  }
  CHECK_EQ(g_live_allocs.load(), before);
}

CASE("copy, move and self-assignment of WeakPtr") {
  Session::clear();
  SharedPtr<Session> s(new Session{7});
  WeakPtr<Session> a(s);
  WeakPtr<Session> b;
  b = a;
  CHECK_EQ(b.lock()->id, 7);
  WeakPtr<Session>& alias = b;
  b = alias;
  CHECK(!b.expired());
  b = std::move(alias);
  CHECK(!b.expired());
  WeakPtr<Session> c(std::move(a));
  CHECK(a.expired());
  CHECK(!c.expired());
  SharedPtr<Session>& salias = s;
  s = salias;
  s = std::move(salias);
  CHECK_EQ(s.use_count(), 1L);
  CHECK_EQ(Session::destroyed.load(), 0);
}

CASE("no leaks after a mix of operations") {
  Session::clear();
  long before = g_live_allocs.load();
  {
    std::vector<SharedPtr<Session>> owners;
    std::vector<WeakPtr<Session>> observers;
    for (int i = 0; i < 100; ++i) {
      owners.emplace_back(new Session{i});
      observers.emplace_back(owners.back());
      if (i % 3 == 0) observers.emplace_back(observers.back());
    }
    for (int i = 0; i < 100; i += 2) owners[i].reset();
    CHECK_EQ(Session::alive.load(), 50);
    int alive = 0;
    for (auto& w : observers) alive += w.lock() ? 1 : 0;
    CHECK_EQ(alive, 50 + 17);  // odd ids, plus the duplicates for odd multiples of 3
  }
  CHECK_EQ(Session::alive.load(), 0);
  CHECK_EQ(Session::destroyed.load(), 100);
  CHECK_EQ(g_live_allocs.load(), before);
}

CASE("4 threads lock and drop concurrently while the owner keeps it alive") {
  Session::clear();
  SharedPtr<Session> s(new Session{8});
  WeakPtr<Session> w(s);
  std::atomic<int> ok{0};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] {
      WeakPtr<Session> mine = w;
      for (int i = 0; i < 20000; ++i)
        if (SharedPtr<Session> p = mine.lock(); p && p->id == 8) ok.fetch_add(1);
    });
  for (auto& th : ts) th.join();
  CHECK_EQ(ok.load(), 80000);
  CHECK_EQ(s.use_count(), 1L);
  s.reset();
  CHECK_EQ(Session::destroyed.load(), 1);
  CHECK(w.expired());
}

CASE("lock racing with the last reset never resurrects the object") {
  Session::clear();
  std::atomic<int> wrong{0};
  for (int round = 0; round < 300; ++round) {
    SharedPtr<Session> s(new Session{round});
    WeakPtr<Session> w(s);
    std::atomic<bool> go{false};
    std::thread locker([&] {
      while (!go.load()) {}
      for (int i = 0; i < 50; ++i)
        if (SharedPtr<Session> p = w.lock(); p && p->id != round) wrong.fetch_add(1);
    });
    go.store(true);
    s.reset();
    locker.join();
    CHECK(w.expired());
  }
  CHECK_EQ(wrong.load(), 0);
  CHECK_EQ(Session::destroyed.load(), 300);
  CHECK_EQ(Session::alive.load(), 0);
}
