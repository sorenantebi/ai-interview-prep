#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <string>
#include <thread>
#include <vector>

EXAMPLE("Example 1: FIFO pop and non-blocking try_pop") {
  ThreadSafeQueue<int> q;
  CHECK(q.push(1));
  CHECK(q.push(2));
  CHECK_EQ(q.pop(), std::optional<int>(1));
  CHECK_EQ(q.try_pop(), std::optional<int>(2));
  CHECK(!q.try_pop().has_value());
}

EXAMPLE("Example 2: close rejects pushes but still drains") {
  ThreadSafeQueue<int> q;
  q.push(7);
  q.close();
  CHECK(!q.push(8));
  CHECK_EQ(q.pop(), std::optional<int>(7));
  CHECK(!q.pop().has_value());
}

EXAMPLE("Example 3: pop blocks until a producer pushes") {
  ThreadSafeQueue<int> q;
  std::optional<int> got;
  std::thread consumer([&] { got = q.pop(); });
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  q.push(42);
  consumer.join();
  CHECK_EQ(got, std::optional<int>(42));
}

CASE("size and closed report state") {
  ThreadSafeQueue<std::string> q;
  CHECK_EQ(q.size(), 0u);
  CHECK(!q.closed());
  q.push("a"); q.push("b"); q.push("c");
  CHECK_EQ(q.size(), 3u);
  q.close();
  q.close();  // idempotent
  CHECK(q.closed());
  CHECK_EQ(q.pop(), std::optional<std::string>("a"));
  CHECK_EQ(q.size(), 2u);
}

CASE("close wakes every blocked consumer with nullopt") {
  ThreadSafeQueue<int> q;
  std::atomic<int> woke{0}, got_value{0};
  std::vector<std::thread> ts;
  for (int i = 0; i < 4; ++i)
    ts.emplace_back([&] { if (q.pop().has_value()) ++got_value; ++woke; });
  std::this_thread::sleep_for(std::chrono::milliseconds(30));
  q.close();
  for (auto& t : ts) t.join();
  CHECK_EQ(woke.load(), 4);
  CHECK_EQ(got_value.load(), 0);
}

CASE("blocked pop is not woken by nothing: it waits for the push") {
  ThreadSafeQueue<int> q;
  std::atomic<bool> done{false};
  std::optional<int> got;
  std::thread consumer([&] { got = q.pop(); done = true; });
  std::this_thread::sleep_for(std::chrono::milliseconds(50));
  bool early = done.load();
  q.push(5);
  consumer.join();
  CHECK(!early);
  CHECK_EQ(got, std::optional<int>(5));
}

CASE("single producer keeps FIFO order for a consumer thread") {
  ThreadSafeQueue<int> q;
  std::vector<int> seen;
  std::thread consumer([&] { while (auto v = q.pop()) seen.push_back(*v); });
  for (int i = 0; i < 20000; ++i) q.push(i);
  q.close();
  consumer.join();
  CHECK_EQ(seen.size(), 20000u);
  bool ordered = true;
  for (int i = 0; i < (int)seen.size(); ++i) ordered = ordered && seen[i] == i;
  CHECK(ordered);
}

static void many_to_many() {
  ThreadSafeQueue<long> q;
  const int P = 4, C = 4, N = 20000;
  std::atomic<long> sum{0}, count{0};
  std::vector<std::thread> consumers, producers;
  for (int c = 0; c < C; ++c)
    consumers.emplace_back([&] { while (auto v = q.pop()) { sum += *v; ++count; } });
  for (int p = 0; p < P; ++p)
    producers.emplace_back([&, p] { for (int i = 1; i <= N; ++i) q.push((long)p * N + i); });
  for (auto& t : producers) t.join();
  q.close();
  for (auto& t : consumers) t.join();
  long n = (long)P * N;
  CHECK_EQ(count.load(), n);
  CHECK_EQ(sum.load(), n * (n + 1) / 2);
  CHECK(!q.try_pop().has_value());
}

CASE("4 producers x 4 consumers: every value delivered exactly once") { many_to_many(); }

CASE("many-to-many repeated 3 times") { for (int r = 0; r < 3; ++r) many_to_many(); }

CASE("try_pop from many threads never duplicates") {
  ThreadSafeQueue<int> q;
  for (int i = 0; i < 40000; ++i) q.push(1);
  std::atomic<int> taken{0};
  std::vector<std::thread> ts;
  for (int t = 0; t < 4; ++t)
    ts.emplace_back([&] { while (q.try_pop()) ++taken; });
  for (auto& t : ts) t.join();
  CHECK_EQ(taken.load(), 40000);
  CHECK_EQ(q.size(), 0u);
}
