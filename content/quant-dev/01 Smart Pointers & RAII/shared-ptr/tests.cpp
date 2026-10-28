#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <cstdlib>
#include <new>
#include <thread>
#include <vector>

// Count live heap blocks so the tests can see whether the control block is freed.
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

struct Snapshot {
  static inline std::atomic<int> alive{0}, destroyed{0};
  int version;
  explicit Snapshot(int v) : version(v) { ++alive; }
  ~Snapshot() { --alive; ++destroyed; }
  static void clear() { alive = 0; destroyed = 0; }
};

EXAMPLE("Example 1: copies share the object and the count") {
  SharedPtr<int> a(new int(10));
  CHECK_EQ(a.use_count(), 1L);
  {
    SharedPtr<int> b = a;
    CHECK_EQ(a.use_count(), 2L);
    CHECK_EQ(b.use_count(), 2L);
    *b = 11;
  }
  CHECK_EQ(a.use_count(), 1L);
  CHECK_EQ(*a, 11);
}

EXAMPLE("Example 2: make_shared_ptr, move, reset deletes the object") {
  Snapshot::clear();
  SharedPtr<Snapshot> s = make_shared_ptr<Snapshot>(7);
  CHECK_EQ(s->version, 7);
  SharedPtr<Snapshot> t = std::move(s);
  CHECK(!s);
  CHECK_EQ(t.use_count(), 1L);
  CHECK_EQ(Snapshot::alive.load(), 1);
  t.reset();
  CHECK_EQ(Snapshot::alive.load(), 0);
  CHECK_EQ(Snapshot::destroyed.load(), 1);
}

CASE("empty pointers have use_count 0") {
  SharedPtr<int> a;
  CHECK(!a);
  CHECK(a.get() == nullptr);
  CHECK_EQ(a.use_count(), 0L);
  SharedPtr<int> b = a;
  CHECK_EQ(b.use_count(), 0L);
  SharedPtr<int> c(nullptr);
  CHECK_EQ(c.use_count(), 0L);
}

CASE("the last owner deletes the object exactly once") {
  Snapshot::clear();
  {
    SharedPtr<Snapshot> a(new Snapshot(1));
    {
      SharedPtr<Snapshot> b = a;
      SharedPtr<Snapshot> c = b;
      CHECK_EQ(a.use_count(), 3L);
    }
    CHECK_EQ(Snapshot::destroyed.load(), 0);
    CHECK_EQ(a.use_count(), 1L);
  }
  CHECK_EQ(Snapshot::destroyed.load(), 1);
  CHECK_EQ(Snapshot::alive.load(), 0);
}

CASE("copy assignment releases the old object and shares the new one") {
  Snapshot::clear();
  SharedPtr<Snapshot> a(new Snapshot(1));
  SharedPtr<Snapshot> b(new Snapshot(2));
  a = b;
  CHECK_EQ(Snapshot::destroyed.load(), 1);
  CHECK_EQ(a->version, 2);
  CHECK_EQ(a.use_count(), 2L);
  b.reset(new Snapshot(3));
  CHECK_EQ(a.use_count(), 1L);
  CHECK_EQ(b.use_count(), 1L);
  CHECK_EQ(b->version, 3);
  a.reset();
  b.reset();
  CHECK_EQ(Snapshot::alive.load(), 0);
  CHECK_EQ(Snapshot::destroyed.load(), 3);
}

CASE("self copy- and move-assignment change nothing") {
  Snapshot::clear();
  SharedPtr<Snapshot> a(new Snapshot(5));
  SharedPtr<Snapshot> keep = a;
  SharedPtr<Snapshot>& alias = a;
  a = alias;
  CHECK_EQ(a.use_count(), 2L);
  a = std::move(alias);
  CHECK(bool(a));
  CHECK_EQ(a->version, 5);
  CHECK_EQ(a.use_count(), 2L);
  CHECK_EQ(Snapshot::destroyed.load(), 0);
}

CASE("move assignment steals without touching the count") {
  SharedPtr<int> a(new int(1));
  SharedPtr<int> extra = a;
  SharedPtr<int> b;
  b = std::move(a);
  CHECK(!a);
  CHECK_EQ(a.use_count(), 0L);
  CHECK_EQ(b.use_count(), 2L);
  CHECK_EQ(*b, 1);
}

CASE("no leaks: the control block is freed with the last owner") {
  long before = g_live_allocs.load();
  {
    SharedPtr<int> a(new int(1));
    SharedPtr<int> b = a;
    SharedPtr<int> c = make_shared_ptr<int>(2);
    c = a;
    b.reset(new int(3));
    a = std::move(b);
  }
  CHECK_EQ(g_live_allocs.load(), before);
}

CASE("copies made and dropped from 4 threads keep the count exact") {
  Snapshot::clear();
  SharedPtr<Snapshot> root(new Snapshot(1));
  const int kThreads = 4, kCopies = 20000;
  std::vector<std::vector<SharedPtr<Snapshot>>> held(kThreads);
  std::vector<std::thread> ts;
  for (int t = 0; t < kThreads; ++t)
    ts.emplace_back([&, t] {
      held[t].reserve(kCopies);
      for (int i = 0; i < kCopies; ++i) {
        SharedPtr<Snapshot> tmp = root;  // extra churn: copy and drop
        held[t].push_back(tmp);
      }
    });
  for (auto& th : ts) th.join();
  CHECK_EQ(root.use_count(), 1L + kThreads * kCopies);
  ts.clear();
  for (int t = 0; t < kThreads; ++t) ts.emplace_back([&, t] { held[t].clear(); });
  for (auto& th : ts) th.join();
  CHECK_EQ(root.use_count(), 1L);
  CHECK_EQ(Snapshot::destroyed.load(), 0);
  root.reset();
  CHECK_EQ(Snapshot::destroyed.load(), 1);
}

CASE("the last of several threads deletes the object exactly once") {
  Snapshot::clear();
  for (int round = 0; round < 200; ++round) {
    SharedPtr<Snapshot> root(new Snapshot(round));
    std::vector<SharedPtr<Snapshot>> copies(4, root);
    root.reset();
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) ts.emplace_back([&, t] { copies[t].reset(); });
    for (auto& th : ts) th.join();
  }
  CHECK_EQ(Snapshot::destroyed.load(), 200);
  CHECK_EQ(Snapshot::alive.load(), 0);
}
