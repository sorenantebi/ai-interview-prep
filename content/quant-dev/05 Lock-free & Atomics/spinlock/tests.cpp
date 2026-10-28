#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <mutex>
#include <thread>
#include <vector>

static long hammer(SpinLock& s, int threads, int iters) {
  long counter = 0;
  std::vector<std::thread> ts;
  for (int t = 0; t < threads; ++t)
    ts.emplace_back([&] {
      for (int i = 0; i < iters; ++i) {
        std::lock_guard<SpinLock> g(s);
        ++counter;
      }
    });
  for (auto& t : ts) t.join();
  return counter;
}

EXAMPLE("Example 1: try_lock succeeds only when free") {
  SpinLock s;
  CHECK(s.try_lock());
  CHECK(!s.try_lock());
  s.unlock();
  CHECK(s.try_lock());
  s.unlock();
}

EXAMPLE("Example 2: 4 threads x 100000 increments are exact") {
  SpinLock s;
  CHECK_EQ(hammer(s, 4, 100000), 400000L);
}

CASE("lock then try_lock fails, unlock then try_lock succeeds") {
  SpinLock s;
  s.lock();
  CHECK(!s.try_lock());
  s.unlock();
  CHECK(s.try_lock());
  s.unlock();
}

CASE("works with std::unique_lock and std::scoped_lock") {
  SpinLock a, b;
  {
    std::unique_lock<SpinLock> ul(a);
    CHECK(ul.owns_lock());
    CHECK(!a.try_lock());
  }
  CHECK(a.try_lock());
  a.unlock();
  {
    std::scoped_lock both(a, b);
    CHECK(!a.try_lock());
    CHECK(!b.try_lock());
  }
  CHECK(a.try_lock());
  CHECK(b.try_lock());
  a.unlock();
  b.unlock();
}

CASE("another thread cannot take a held lock") {
  SpinLock s;
  s.lock();
  bool other = true;
  std::thread t([&] { other = s.try_lock(); });
  t.join();
  s.unlock();
  CHECK(!other);
}

CASE("lock waits for the owner to release") {
  SpinLock s;
  std::atomic<int> stage{0};
  s.lock();
  std::thread t([&] { stage = 1; s.lock(); stage = 2; s.unlock(); });
  while (stage.load() == 0) std::this_thread::yield();
  for (int i = 0; i < 1000; ++i) std::this_thread::yield();
  int early = stage.load();
  s.unlock();
  t.join();
  CHECK_EQ(early, 1);
  CHECK_EQ(stage.load(), 2);
}

CASE("4 threads x 100000, repeated 3 times") {
  for (int r = 0; r < 3; ++r) {
    SpinLock s;
    CHECK_EQ(hammer(s, 4, 100000), 400000L);
  }
}

CASE("no two threads are ever inside the critical section together") {
  SpinLock s;
  std::atomic<int> inside{0};
  std::atomic<bool> overlap{false};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] {
      for (int i = 0; i < 50000; ++i) {
        std::lock_guard<SpinLock> g(s);
        if (inside.fetch_add(1) != 0) overlap = true;
        inside.fetch_sub(1);
      }
    });
  for (auto& t : ts) t.join();
  CHECK(!overlap.load());
}

CASE("8 threads with try_lock retries stay exact") {
  SpinLock s;
  long counter = 0;
  std::atomic<bool> gave_up{false};
  auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(3);
  std::vector<std::thread> ts;
  for (int t = 0; t < 8; ++t)
    ts.emplace_back([&] {
      for (int i = 0; i < 20000; ++i) {
        while (!s.try_lock()) {
          if (gave_up.load() || std::chrono::steady_clock::now() > deadline) { gave_up = true; return; }
          std::this_thread::yield();
        }
        ++counter;
        s.unlock();
      }
    });
  for (auto& t : ts) t.join();
  CHECK(!gave_up.load());
  CHECK_EQ(counter, 160000L);
}
