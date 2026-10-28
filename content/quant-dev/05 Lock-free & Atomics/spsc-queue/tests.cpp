#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <string>
#include <thread>

using Clock = std::chrono::steady_clock;

// One producer, one consumer, n ints in order. A side that makes no progress for 500 ms gives up
// (so a broken queue fails fast instead of hanging). Returns how many values arrived in order (n on success).
static long transfer(std::size_t capacity, long n) {
  SPSCQueue<long> q(capacity);
  std::atomic<bool> abort{false};
  struct Watchdog {
    std::atomic<bool>& abort;
    long last = -1, spins = 0;
    Clock::time_point since = Clock::now();
    bool stuck(long progress) {  // called while spinning
      if ((++spins & 255) == 0) std::this_thread::yield();
      if ((spins & 1023) != 0) return abort.load(std::memory_order_relaxed);
      auto now = Clock::now();
      if (progress != last) { last = progress; since = now; }
      else if (now - since > std::chrono::milliseconds(500)) abort = true;
      return abort.load();
    }
  };
  long received = 0;
  std::thread consumer([&] {
    Watchdog w{abort};
    while (received < n) {
      if (auto v = q.try_pop()) {
        if (*v != received) { abort = true; return; }
        ++received;
      } else if (w.stuck(received)) {
        return;
      }
    }
  });
  std::thread producer([&] {
    Watchdog w{abort};
    for (long i = 0; i < n; ++i)
      while (!q.try_push(i))
        if (w.stuck(i)) return;
  });
  producer.join();
  consumer.join();
  return received;
}

EXAMPLE("Example 1: capacity rounds up, full, then wraps") {
  SPSCQueue<int> q(3);
  CHECK_EQ(q.capacity(), 4u);
  for (int i = 1; i <= 4; ++i) CHECK(q.try_push(i));
  CHECK(!q.try_push(5));
  CHECK_EQ(q.try_pop(), std::optional<int>(1));
  CHECK(q.try_push(5));
  for (int i = 2; i <= 5; ++i) CHECK_EQ(q.try_pop(), std::optional<int>(i));
  CHECK(!q.try_pop().has_value());
}

EXAMPLE("Example 2: one producer and one consumer move 1,000,000 ints in order") {
  CHECK_EQ(transfer(1024, 1000000), 1000000L);
}

CASE("capacity is rounded up to a power of two") {
  CHECK_EQ(SPSCQueue<int>(1).capacity(), 1u);
  CHECK_EQ(SPSCQueue<int>(2).capacity(), 2u);
  CHECK_EQ(SPSCQueue<int>(5).capacity(), 8u);
  CHECK_EQ(SPSCQueue<int>(1000).capacity(), 1024u);
  CHECK_EQ(SPSCQueue<int>(1024).capacity(), 1024u);
  CHECK_EQ(SPSCQueue<int>(1025).capacity(), 2048u);
}

CASE("new queue is empty; pop on empty gives nullopt") {
  SPSCQueue<std::string> q(4);
  CHECK(q.empty());
  CHECK(!q.try_pop().has_value());
  CHECK(q.try_push("px"));
  CHECK(!q.empty());
  CHECK_EQ(q.try_pop(), std::optional<std::string>("px"));
  CHECK(q.empty());
}

CASE("exactly capacity items fit, then push fails until a pop") {
  SPSCQueue<int> q(16);
  for (int i = 0; i < 16; ++i) CHECK(q.try_push(i));
  CHECK(!q.try_push(99));
  CHECK(!q.try_push(99));
  CHECK_EQ(q.try_pop(), std::optional<int>(0));
  CHECK(q.try_push(16));
  CHECK(!q.try_push(17));
  for (int i = 1; i <= 16; ++i) CHECK_EQ(q.try_pop(), std::optional<int>(i));
  CHECK(q.empty());
}

CASE("single-threaded FIFO across many wrap-arounds") {
  SPSCQueue<int> q(8);
  int in = 0, out = 0;
  bool ok = true;
  for (int round = 0; round < 20000; ++round) {
    for (int k = 0; k < round % 9; ++k) if (q.try_push(in)) ++in;
    for (int k = 0; k < round % 7; ++k) if (auto v = q.try_pop()) ok = ok && *v == out++;
  }
  while (auto v = q.try_pop()) ok = ok && *v == out++;
  CHECK(ok);
  CHECK_EQ(in, out);
}

CASE("head and tail live on separate cache lines (alignas(64))") {
  CHECK(alignof(SPSCQueue<int>) >= 64);
  CHECK(sizeof(SPSCQueue<int>) >= 128);
}

CASE("capacity 1 forces a hand-off on every item") {
  CHECK_EQ(transfer(1, 100000), 100000L);
}

CASE("1,000,000 ints through a small queue, repeated 3 times") {
  for (int r = 0; r < 3; ++r) CHECK_EQ(transfer(64, 1000000), 1000000L);
}
