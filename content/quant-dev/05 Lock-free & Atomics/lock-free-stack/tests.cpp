#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <atomic>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

// 4 threads each push their own n distinct values, popping after every second push.
// Afterwards the rest is drained. Returns true if the popped values are exactly the pushed ones.
static bool concurrent_push_pop(int threads, int n) {
  LockFreeStack<int> s;
  std::mutex m;
  std::vector<int> popped;
  std::vector<std::thread> ts;
  for (int t = 0; t < threads; ++t)
    ts.emplace_back([&, t] {
      std::vector<int> mine;
      for (int i = 0; i < n; ++i) {
        s.push(t * n + i);
        if (i % 2 == 1)
          if (auto v = s.pop()) mine.push_back(*v);
      }
      std::lock_guard<std::mutex> g(m);
      popped.insert(popped.end(), mine.begin(), mine.end());
    });
  for (auto& t : ts) t.join();
  while (auto v = s.pop()) popped.push_back(*v);
  std::sort(popped.begin(), popped.end());
  bool ok = (int)popped.size() == threads * n;
  for (int i = 0; ok && i < threads * n; ++i) ok = popped[i] == i;
  return ok && s.empty();
}

EXAMPLE("Example 1: LIFO order and empty pop") {
  LockFreeStack<int> s;
  s.push(1);
  s.push(2);
  s.push(3);
  CHECK_EQ(s.pop(), std::optional<int>(3));
  CHECK_EQ(s.pop(), std::optional<int>(2));
  CHECK(!s.empty());
  CHECK_EQ(s.pop(), std::optional<int>(1));
  CHECK(!s.pop().has_value());
  CHECK(s.empty());
}

EXAMPLE("Example 2: 4 threads push and pop concurrently, nothing lost or duplicated") {
  CHECK(concurrent_push_pop(4, 10000));
}

CASE("new stack is empty") {
  LockFreeStack<std::string> s;
  CHECK(s.empty());
  CHECK(!s.pop().has_value());
}

CASE("interleaved push and pop single-threaded") {
  LockFreeStack<std::string> s;
  s.push("a");
  s.push("b");
  CHECK_EQ(s.pop(), std::optional<std::string>("b"));
  s.push("c");
  CHECK_EQ(s.pop(), std::optional<std::string>("c"));
  CHECK_EQ(s.pop(), std::optional<std::string>("a"));
  CHECK(s.empty());
}

CASE("move-only values") {
  LockFreeStack<std::unique_ptr<int>> s;
  s.push(std::make_unique<int>(5));
  s.push(std::make_unique<int>(6));
  auto a = s.pop();
  auto b = s.pop();
  CHECK(a.has_value() && b.has_value());
  CHECK_EQ(**a, 6);
  CHECK_EQ(**b, 5);
}

struct Counted {
  static inline std::atomic<int> live{0};
  int v;
  explicit Counted(int v) : v(v) { ++live; }
  Counted(const Counted& o) : v(o.v) { ++live; }
  Counted(Counted&& o) noexcept : v(o.v) { ++live; }
  ~Counted() { --live; }
};

CASE("destructor frees retired and remaining nodes") {
  Counted::live = 0;
  {
    LockFreeStack<Counted> s;
    for (int i = 0; i < 1000; ++i) s.push(Counted(i));
    for (int i = 0; i < 600; ++i) CHECK(s.pop().has_value());
    CHECK(Counted::live.load() >= 400);  // 400 still on the stack
  }
  CHECK_EQ(Counted::live.load(), 0);
}

CASE("concurrent pushes then concurrent pops (3 runs)") {
  for (int rep = 0; rep < 3; ++rep) {
    LockFreeStack<int> s;
    const int T = 4, N = 20000;
    std::vector<std::thread> ts;
    for (int t = 0; t < T; ++t)
      ts.emplace_back([&, t] { for (int i = 0; i < N; ++i) s.push(t * N + i); });
    for (auto& t : ts) t.join();
    ts.clear();
    std::mutex m;
    std::vector<int> popped;
    for (int t = 0; t < T; ++t)
      ts.emplace_back([&] {
        std::vector<int> mine;
        while (auto v = s.pop()) mine.push_back(*v);
        std::lock_guard<std::mutex> g(m);
        popped.insert(popped.end(), mine.begin(), mine.end());
      });
    for (auto& t : ts) t.join();
    std::sort(popped.begin(), popped.end());
    bool ok = (int)popped.size() == T * N;
    for (int i = 0; ok && i < T * N; ++i) ok = popped[i] == i;
    CHECK(ok);
    CHECK(s.empty());
  }
}

CASE("mixed push/pop from 4 threads, repeated 3 times") {
  for (int rep = 0; rep < 3; ++rep) CHECK(concurrent_push_pop(4, 20000));
}

CASE("8 threads hammering the same stack") {
  CHECK(concurrent_push_pop(8, 10000));
}
