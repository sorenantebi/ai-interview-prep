#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <chrono>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

// get() on an empty future is undefined behaviour (it crashes in libc++), so check valid() first.
template <class R> static R got(std::future<R>& f) {
  if (!f.valid()) throw qtest::Failure{"submit returned an empty (invalid) future"};
  return f.get();
}
template <class R> static R got(std::future<R>&& f) { return got(f); }

EXAMPLE("Example 1: results come back through futures") {
  ThreadPool pool(4);
  auto a = pool.submit([](int x, int y) { return x + y; }, 2, 3);
  auto b = pool.submit([] { return std::string("fill"); });
  CHECK_EQ(got(a), 5);
  CHECK_EQ(got(b), std::string("fill"));
}

EXAMPLE("Example 2: exceptions propagate and the pool keeps working") {
  ThreadPool pool(2);
  auto f = pool.submit([]() -> int { throw std::runtime_error("bad price"); });
  std::string msg;
  try { got(f); } catch (const std::runtime_error& e) { msg = e.what(); }
  CHECK_EQ(msg, std::string("bad price"));
  CHECK_EQ(got(pool.submit([] { return 1; })), 1);
}

CASE("size reports the number of workers") {
  ThreadPool pool(3);
  CHECK_EQ(pool.size(), 3u);
}

CASE("many tasks give correct results") {
  ThreadPool pool(4);
  std::vector<std::future<long>> fs;
  for (long i = 0; i < 2000; ++i) fs.push_back(pool.submit([](long x) { return x * x; }, i));
  long sum = 0;
  for (auto& f : fs) sum += got(f);
  CHECK_EQ(sum, 1999L * 2000L * 3999L / 6);
}

CASE("void tasks work and their futures become ready") {
  ThreadPool pool(2);
  std::atomic<int> n{0};
  std::vector<std::future<void>> fs;
  for (int i = 0; i < 100; ++i) fs.push_back(pool.submit([&n] { ++n; }));
  for (auto& f : fs) got(f);
  CHECK_EQ(n.load(), 100);
}

CASE("tasks run on several threads at the same time") {
  // 4 tasks each wait (up to 2 s) until all 4 have started: only possible with 4 concurrent workers.
  ThreadPool pool(4);
  std::atomic<int> started{0};
  std::vector<std::future<std::thread::id>> fs;
  for (int i = 0; i < 4; ++i)
    fs.push_back(pool.submit([&started] {
      ++started;
      auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(2);
      while (started.load() < 4 && std::chrono::steady_clock::now() < deadline) std::this_thread::yield();
      return std::this_thread::get_id();
    }));
  std::set<std::thread::id> ids;
  for (auto& f : fs) ids.insert(got(f));
  CHECK_EQ(started.load(), 4);
  CHECK_EQ(ids.size(), 4u);
  CHECK(ids.count(std::this_thread::get_id()) == 0);
}

CASE("destructor finishes every queued task before joining") {
  std::atomic<int> done{0};
  std::vector<std::future<void>> fs;
  {
    ThreadPool pool(1);
    for (int i = 0; i < 200; ++i)
      fs.push_back(pool.submit([&done] {
        std::this_thread::sleep_for(std::chrono::microseconds(50));
        ++done;
      }));
  }
  CHECK_EQ(done.load(), 200);
  for (auto& f : fs) CHECK(f.valid() && f.wait_for(std::chrono::seconds(0)) == std::future_status::ready);
}

CASE("exceptions of different types propagate") {
  ThreadPool pool(3);
  auto f1 = pool.submit([] { throw std::out_of_range("no level"); });
  auto f2 = pool.submit([](int x) { if (x > 0) throw 42; return x; }, 1);
  auto f3 = pool.submit([] { return 7; });
  bool r1 = false, r2 = false;
  try { got(f1); } catch (const std::out_of_range&) { r1 = true; }
  try { got(f2); } catch (int v) { r2 = v == 42; }
  CHECK(r1);
  CHECK(r2);
  CHECK_EQ(got(f3), 7);
}

CASE("submit from several threads at once") {
  for (int rep = 0; rep < 3; ++rep) {
    ThreadPool pool(4);
    std::vector<std::thread> submitters;
    std::atomic<long> total{0};
    std::atomic<bool> invalid{false};
    for (int s = 0; s < 4; ++s)
      submitters.emplace_back([&pool, &total, &invalid] {
        std::vector<std::future<int>> fs;
        for (int i = 1; i <= 500; ++i) fs.push_back(pool.submit([i] { return i; }));
        for (auto& f : fs) {
          if (!f.valid()) { invalid = true; return; }
          total += f.get();
        }
      });
    for (auto& t : submitters) t.join();
    CHECK(!invalid.load());
    CHECK_EQ(total.load(), 4L * 500 * 501 / 2);
  }
}

CASE("move-only arguments and results") {
  ThreadPool pool(2);
  auto p = std::make_unique<int>(11);
  auto f = pool.submit([](std::unique_ptr<int> q) { return std::make_unique<int>(*q * 2); }, std::move(p));
  auto r = got(f);
  CHECK(r != nullptr);
  CHECK_EQ(*r, 22);
}
