#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

EXAMPLE("Example 1: latch opens when the count reaches zero") {
  CountDownLatch ready(3);
  CHECK(!ready.try_wait());
  ready.count_down();
  CHECK(!ready.try_wait());
  ready.count_down(2);
  CHECK(ready.try_wait());
  ready.wait();
}

EXAMPLE("Example 2: wait sees every worker's result") {
  CountDownLatch done(4);
  std::vector<int> results(4);
  std::vector<std::thread> workers;
  for (int i = 0; i < 4; ++i)
    workers.emplace_back([&, i] {
      std::this_thread::sleep_for(std::chrono::milliseconds(5 * i));
      results[i] = i * i;
      done.count_down();
    });
  done.wait();
  std::vector<int> seen = results;  // read right after wait, before join
  for (auto& t : workers) t.join();
  CHECK_EQ(seen, (std::vector<int>{0, 1, 4, 9}));
}

EXAMPLE("Example 3: barrier keeps two threads in lock-step") {
  Barrier b(2);
  std::atomic<int> step0{0};
  std::atomic<bool> bad{false};
  auto worker = [&] {
    step0++;
    b.arrive_and_wait();
    if (step0.load() != 2) bad = true;  // both finished step 0
    b.arrive_and_wait();
  };
  std::thread t1(worker), t2(worker);
  t1.join(); t2.join();
  CHECK(!bad.load());
}

CASE("latch with count 0 is already open") {
  CountDownLatch l(0);
  CHECK(l.try_wait());
  l.wait();
}

CASE("extra count_down calls keep the latch open at zero") {
  CountDownLatch l(2);
  l.count_down(5);
  CHECK(l.try_wait());
  l.count_down();
  CHECK(l.try_wait());
  l.wait();
}

CASE("wait really blocks until the last count_down") {
  CountDownLatch l(2);
  std::atomic<bool> passed{false};
  std::thread waiter([&] { l.wait(); passed = true; });
  l.count_down();
  std::this_thread::sleep_for(50ms);
  bool early = passed.load();
  l.count_down();
  waiter.join();
  CHECK(!early);
  CHECK(passed.load());
}

CASE("one count_down releases many waiters") {
  for (int rep = 0; rep < 3; ++rep) {
    CountDownLatch go(1);
    std::atomic<int> released{0};
    std::vector<std::thread> ts;
    for (int i = 0; i < 6; ++i) ts.emplace_back([&] { go.wait(); ++released; });
    std::this_thread::sleep_for(20ms);
    int early = released.load();
    go.count_down();
    for (auto& t : ts) t.join();
    CHECK_EQ(early, 0);
    CHECK_EQ(released.load(), 6);
  }
}

CASE("barrier blocks until every thread arrives") {
  Barrier b(3);
  std::atomic<int> through{0};
  std::thread t1([&] { b.arrive_and_wait(); ++through; });
  std::thread t2([&] { b.arrive_and_wait(); ++through; });
  std::this_thread::sleep_for(50ms);
  int early = through.load();
  b.arrive_and_wait();
  t1.join(); t2.join();
  CHECK_EQ(early, 0);
  CHECK_EQ(through.load(), 2);
}

CASE("barrier of one never blocks and can be reused") {
  Barrier b(1);
  for (int i = 0; i < 1000; ++i) b.arrive_and_wait();
  CHECK(true);
}

CASE("barrier is reusable across 200 phases with 4 threads") {
  for (int rep = 0; rep < 3; ++rep) {
    const int T = 4, PHASES = 200;
    Barrier b(T);
    std::vector<std::atomic<int>> slot(T);
    for (auto& s : slot) s = -1;
    std::atomic<int> errors{0};
    std::vector<std::thread> ts;
    for (int i = 0; i < T; ++i)
      ts.emplace_back([&, i] {
        for (int p = 0; p < PHASES; ++p) {
          slot[i] = p;
          b.arrive_and_wait();  // everyone wrote phase p
          for (int j = 0; j < T; ++j) if (slot[j].load() != p) ++errors;
          b.arrive_and_wait();  // everyone checked before anyone writes p+1
        }
      });
    for (auto& t : ts) t.join();
    CHECK_EQ(errors.load(), 0);
  }
}
