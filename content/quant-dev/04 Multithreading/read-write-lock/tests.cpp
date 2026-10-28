#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

using namespace std::chrono_literals;
using Clock = std::chrono::steady_clock;

// Spin (yielding) until pred() or a 2 s deadline; returns pred().
template <class P> static bool eventually(P pred) {
  auto deadline = Clock::now() + 2s;
  while (!pred() && Clock::now() < deadline) std::this_thread::yield();
  return pred();
}

// Block until a writer is registered as waiting: try_lock_shared() then refuses new readers.
static bool wait_until_writer_waits(RWLock& rw) {
  return eventually([&] {
    if (rw.try_lock_shared()) { rw.unlock_shared(); return false; }
    return true;
  });
}

EXAMPLE("Example 1: readers share, writer is exclusive") {
  RWLock rw;
  rw.lock_shared();
  CHECK(rw.try_lock_shared());
  CHECK(!rw.try_lock());
  rw.unlock_shared();
  rw.unlock_shared();
  CHECK(rw.try_lock());
  CHECK(!rw.try_lock_shared());
  rw.unlock();
}

EXAMPLE("Example 2: a waiting writer blocks newly arriving readers") {
  RWLock rw;
  rw.lock_shared();
  std::atomic<bool> wrote{false};
  std::thread w([&] { rw.lock(); wrote = true; rw.unlock(); });
  bool waiting = wait_until_writer_waits(rw);
  bool early = wrote.load();
  rw.unlock_shared();
  w.join();
  CHECK(waiting);
  CHECK(!early);
  CHECK(wrote.load());
  CHECK(rw.try_lock_shared());
  rw.unlock_shared();
}

CASE("two readers hold the lock at the same time (blocking lock_shared)") {
  RWLock rw;
  rw.lock_shared();
  std::atomic<bool> second_in{false}, release{false};
  std::thread r([&] {
    rw.lock_shared();
    second_in = true;
    eventually([&] { return release.load(); });
    rw.unlock_shared();
  });
  bool shared = eventually([&] { return second_in.load(); });
  release = true;
  r.join();
  CHECK(shared);
  rw.unlock_shared();
  CHECK(rw.try_lock());
  rw.unlock();
}

CASE("writer waits until the reader leaves") {
  RWLock rw;
  rw.lock_shared();
  std::atomic<bool> wrote{false};
  std::thread w([&] { rw.lock(); wrote = true; rw.unlock(); });
  std::this_thread::sleep_for(50ms);
  bool early = wrote.load();
  rw.unlock_shared();
  w.join();
  CHECK(!early);
  CHECK(wrote.load());
}

CASE("reader waits until the writer leaves") {
  RWLock rw;
  rw.lock();
  std::atomic<bool> read{false};
  std::thread r([&] { rw.lock_shared(); read = true; rw.unlock_shared(); });
  std::this_thread::sleep_for(50ms);
  bool early = read.load();
  rw.unlock();
  r.join();
  CHECK(!early);
  CHECK(read.load());
}

CASE("writers exclude each other") {
  RWLock rw;
  CHECK(rw.try_lock());
  CHECK(!rw.try_lock());
  std::atomic<bool> second{false};
  std::thread w([&] { rw.lock(); second = true; rw.unlock(); });
  std::this_thread::sleep_for(50ms);
  bool early = second.load();
  rw.unlock();
  w.join();
  CHECK(!early);
  CHECK(second.load());
}

static void writer_priority_order() {
  RWLock rw;
  std::mutex em;
  std::string events;
  auto log = [&](char c) { std::lock_guard<std::mutex> g(em); events += c; };
  rw.lock_shared();                                   // reader A inside
  std::thread w([&] { rw.lock(); log('W'); rw.unlock(); });
  bool waiting = wait_until_writer_waits(rw);        // W is now registered as waiting
  std::thread b([&] { rw.lock_shared(); log('B'); rw.unlock_shared(); });
  std::this_thread::sleep_for(30ms);                  // give B a chance to (wrongly) overtake
  bool overtaken;
  { std::lock_guard<std::mutex> g(em); overtaken = !events.empty(); }
  rw.unlock_shared();                                 // A leaves
  w.join();
  b.join();
  CHECK(waiting);
  CHECK(!overtaken);
  CHECK_EQ(events, std::string("WB"));
}

CASE("waiting writer goes before a reader that arrived later") { writer_priority_order(); }

CASE("writer priority order holds, repeated 3 times") {
  for (int i = 0; i < 3; ++i) writer_priority_order();
}

CASE("when the writer leaves, all waiting readers enter together") {
  RWLock rw;
  rw.lock();
  std::atomic<int> inside{0}, all_together{0};
  std::vector<std::thread> rs;
  for (int i = 0; i < 3; ++i)
    rs.emplace_back([&] {
      rw.lock_shared();
      ++inside;
      if (eventually([&] { return inside.load() == 3; })) ++all_together;
      rw.unlock_shared();
    });
  std::this_thread::sleep_for(30ms);
  int early = inside.load();
  rw.unlock();
  for (auto& t : rs) t.join();
  CHECK_EQ(early, 0);
  CHECK_EQ(all_together.load(), 3);
}

CASE("stress: readers never see a half-written pair") {
  for (int rep = 0; rep < 3; ++rep) {
    RWLock rw;
    long a = 0, b = 0;
    std::atomic<bool> torn{false};
    std::vector<std::thread> ts;
    for (int w = 0; w < 2; ++w)
      ts.emplace_back([&] {
        for (int i = 0; i < 5000; ++i) { rw.lock(); ++a; ++b; rw.unlock(); }
      });
    for (int r = 0; r < 4; ++r)
      ts.emplace_back([&] {
        for (int i = 0; i < 5000; ++i) {
          rw.lock_shared();
          if (a != b) torn = true;
          rw.unlock_shared();
        }
      });
    for (auto& t : ts) t.join();
    CHECK(!torn.load());
    CHECK_EQ(a, 10000L);
    CHECK_EQ(b, 10000L);
  }
}
