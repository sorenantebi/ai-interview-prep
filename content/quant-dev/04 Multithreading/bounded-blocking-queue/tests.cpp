#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

EXAMPLE("Example 1: try_push / try_pop respect the capacity") {
  BoundedBlockingQueue<int> q(2);
  CHECK(q.try_push(1));
  CHECK(q.try_push(2));
  CHECK(!q.try_push(3));
  CHECK_EQ(q.pop(), 1);
  CHECK(q.try_push(3));
  CHECK_EQ(q.pop(), 2);
  CHECK_EQ(q.pop(), 3);
  CHECK(!q.try_pop().has_value());
}

EXAMPLE("Example 2: push blocks on a full queue until a pop") {
  BoundedBlockingQueue<int> q(1);
  q.push(10);
  std::thread producer([&] { q.push(20); });
  int first = q.pop();
  producer.join();
  CHECK_EQ(first, 10);
  CHECK_EQ(q.pop(), 20);
}

CASE("capacity, size, and empty try_pop") {
  BoundedBlockingQueue<int> q(3);
  CHECK_EQ(q.capacity(), 3u);
  CHECK_EQ(q.size(), 0u);
  q.push(1); q.push(2);
  CHECK_EQ(q.size(), 2u);
  CHECK_EQ(q.try_pop(), std::optional<int>(1));
  CHECK_EQ(q.size(), 1u);
}

CASE("push really waits while the queue is full") {
  BoundedBlockingQueue<int> q(2);
  q.push(1); q.push(2);
  std::atomic<bool> done{false};
  std::thread producer([&] { q.push(3); done = true; });
  std::this_thread::sleep_for(50ms);
  bool early = done.load();
  std::size_t sz = q.size();
  int first = q.pop();
  producer.join();
  CHECK(!early);
  CHECK_EQ(sz, 2u);
  CHECK_EQ(first, 1);
  CHECK(done.load());
  CHECK_EQ(q.pop(), 2);
  CHECK_EQ(q.pop(), 3);
}

CASE("pop really waits while the queue is empty") {
  BoundedBlockingQueue<int> q(4);
  std::atomic<bool> done{false};
  int got = 0;
  std::thread consumer([&] { got = q.pop(); done = true; });
  std::this_thread::sleep_for(50ms);
  bool early = done.load();
  q.push(99);
  consumer.join();
  CHECK(!early);
  CHECK_EQ(got, 99);
}

CASE("single fast producer, single slow consumer keeps order") {
  BoundedBlockingQueue<int> q(8);
  const int N = 20000;
  std::vector<int> seen;
  std::thread consumer([&] {
    for (int i = 0; i < N; ++i) {
      if (i % 2000 == 0) std::this_thread::sleep_for(1ms);
      seen.push_back(q.pop());
    }
  });
  for (int i = 0; i < N; ++i) q.push(i);
  consumer.join();
  bool ordered = (int)seen.size() == N;
  for (int i = 0; ordered && i < N; ++i) ordered = seen[i] == i;
  CHECK(ordered);
}

static void producers_faster_than_consumers() {
  BoundedBlockingQueue<long> q(4);
  const int P = 4, C = 2, N = 10000;
  std::atomic<long> sum{0};
  std::atomic<bool> over_capacity{false};
  std::vector<std::thread> ps, cs;
  for (int c = 0; c < C; ++c)
    cs.emplace_back([&] {
      for (int i = 0; i < P * N / C; ++i) {
        if (i % 5000 == 0) std::this_thread::sleep_for(1ms);  // consumers are slower
        sum += q.pop();
      }
    });
  for (int p = 0; p < P; ++p)
    ps.emplace_back([&] {
      for (int i = 1; i <= N; ++i) {
        q.push(i);
        if (q.size() > q.capacity()) over_capacity = true;
      }
    });
  for (auto& t : ps) t.join();
  for (auto& t : cs) t.join();
  CHECK(!over_capacity.load());
  CHECK_EQ(sum.load(), (long)P * N * (N + 1) / 2);
  CHECK_EQ(q.size(), 0u);
}

CASE("4 fast producers, 2 slow consumers: exact sum, never over capacity") { producers_faster_than_consumers(); }

CASE("producers faster than consumers, repeated 3 times") {
  for (int r = 0; r < 3; ++r) producers_faster_than_consumers();
}

CASE("try_push from many threads never exceeds capacity") {
  BoundedBlockingQueue<int> q(100);
  std::atomic<int> accepted{0};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] { for (int i = 0; i < 1000; ++i) if (q.try_push(i)) ++accepted; });
  for (auto& t : ts) t.join();
  CHECK_EQ(accepted.load(), 100);
  CHECK_EQ(q.size(), 100u);
}
