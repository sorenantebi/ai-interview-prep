#include "qtest.h"
#include "attempt.cpp"
#include <mutex>
#include <stdexcept>
#include <thread>
#include <type_traits>
#include <vector>

// Instrumented mutex: counts calls and remembers whether it is held.
struct FakeMutex {
  int locks = 0, unlocks = 0;
  bool held = false;
  void lock() { ++locks; held = true; }
  void unlock() { ++unlocks; held = false; }
};

EXAMPLE("Example 1: LockGuard releases the mutex at end of scope") {
  std::mutex m;
  int counter = 0;
  {
    LockGuard<std::mutex> g(m);
    ++counter;
    CHECK(!m.try_lock());
  }
  CHECK(m.try_lock());
  m.unlock();
  CHECK_EQ(counter, 1);
}

EXAMPLE("Example 2: UniqueLock unlock / relock / misuse") {
  std::mutex m;
  {
    UniqueLock<std::mutex> ul(m);
    CHECK(ul.owns_lock());
    ul.unlock();
    CHECK(!ul.owns_lock());
    CHECK_THROWS(ul.unlock());
    ul.lock();
    CHECK(ul.owns_lock());
  }
  CHECK(m.try_lock());
  m.unlock();
}

CASE("LockGuard locks once and unlocks once") {
  FakeMutex m;
  {
    LockGuard<FakeMutex> g(m);
    CHECK_EQ(m.locks, 1);
    CHECK_EQ(m.unlocks, 0);
    CHECK(m.held);
  }
  CHECK_EQ(m.locks, 1);
  CHECK_EQ(m.unlocks, 1);
  CHECK(!m.held);
}

CASE("LockGuard unlocks when the scope exits by exception") {
  FakeMutex m;
  try {
    LockGuard<FakeMutex> g(m);
    throw std::runtime_error("reject order");
  } catch (const std::runtime_error&) {}
  CHECK_EQ(m.locks, 1);
  CHECK_EQ(m.unlocks, 1);
}

CASE("guards are not copyable") {
  CHECK(!std::is_copy_constructible_v<LockGuard<FakeMutex>>);
  CHECK(!std::is_copy_assignable_v<LockGuard<FakeMutex>>);
  CHECK(!std::is_copy_constructible_v<UniqueLock<FakeMutex>>);
  CHECK(!std::is_copy_assignable_v<UniqueLock<FakeMutex>>);
}

CASE("UniqueLock destructor does not unlock after a manual unlock") {
  FakeMutex m;
  {
    UniqueLock<FakeMutex> ul(m);
    CHECK(ul.owns_lock());
    ul.unlock();
  }
  CHECK_EQ(m.locks, 1);
  CHECK_EQ(m.unlocks, 1);
}

CASE("UniqueLock lock while owning throws and does not lock again") {
  FakeMutex m;
  {
    UniqueLock<FakeMutex> ul(m);
    bool threw = false;
    try { ul.lock(); } catch (const std::logic_error&) { threw = true; }
    CHECK(threw);
    CHECK_EQ(m.locks, 1);
  }
  CHECK_EQ(m.unlocks, 1);
}

CASE("UniqueLock relocked many times stays balanced") {
  FakeMutex m;
  {
    UniqueLock<FakeMutex> ul(m);
    for (int i = 0; i < 10; ++i) { ul.unlock(); ul.lock(); }
  }
  CHECK_EQ(m.locks, 11);
  CHECK_EQ(m.unlocks, 11);
  CHECK(!m.held);
}

CASE("LockGuard with std::mutex protects a counter across 4 threads") {
  std::mutex m;
  long counter = 0;
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] { for (int i = 0; i < 50000; ++i) { LockGuard<std::mutex> g(m); ++counter; } });
  for (auto& t : ts) t.join();
  CHECK_EQ(counter, 200000L);
  CHECK(m.try_lock());
  m.unlock();
}

CASE("UniqueLock with std::mutex across threads, unlocking early") {
  std::mutex m;
  long counter = 0, outside = 0;
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] {
      long mine = 0;
      for (int i = 0; i < 50000; ++i) {
        UniqueLock<std::mutex> ul(m);
        ++counter;
        ul.unlock();
        ++mine;  // work outside the lock
      }
      UniqueLock<std::mutex> ul(m);
      outside += mine;
    });
  for (auto& t : ts) t.join();
  CHECK_EQ(counter, 200000L);
  CHECK_EQ(outside, 200000L);
  CHECK(m.try_lock());
  m.unlock();
}
