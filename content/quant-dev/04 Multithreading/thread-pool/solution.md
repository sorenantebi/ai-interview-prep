---
topic: "Multithreading"
difficulty: Medium
---
# Thread Pool with Futures - Solution

## Intuition

Workers loop on a shared queue of type-erased jobs (`std::function<void()>`). The typed part lives in `submit`: wrap `f(args...)` in a `std::packaged_task<R()>`, keep its future, and push a small lambda that runs the task. `packaged_task` already stores either the return value or the thrown exception in the shared state, so exception propagation comes for free.

## Approach

1. State: `std::vector<std::thread>`, `std::queue<std::function<void()>>`, a mutex, a condition variable and a `stop_` flag.
2. Worker loop: wait until the queue is non-empty or `stop_`; if stopping **and** the queue is empty, exit; otherwise pop one job, unlock, run it.
3. `submit`: bind the callable and its arguments into a `packaged_task<R()>`. `packaged_task` is move-only and `std::function` needs a copyable target, so hold it in a `std::shared_ptr`. Take the future, push `[task]{ (*task)(); }`, `notify_one`.
4. Destructor: set `stop_` under the lock, `notify_all`, join every worker. Workers only exit once the queue is drained, so queued tasks still run.

## Code

```cpp
#include <condition_variable>
#include <cstddef>
#include <functional>
#include <future>
#include <memory>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <tuple>
#include <type_traits>
#include <utility>
#include <vector>

class ThreadPool {
public:
    explicit ThreadPool(std::size_t num_threads) {
        for (std::size_t i = 0; i < num_threads; ++i)
            workers_.emplace_back([this] { run(); });
    }

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lk(m_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& t : workers_) t.join();
    }

    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;

    template <class F, class... Args>
    auto submit(F&& f, Args&&... args) -> std::future<std::invoke_result_t<F, Args...>> {
        using R = std::invoke_result_t<F, Args...>;
        auto task = std::make_shared<std::packaged_task<R()>>(
            [f = std::forward<F>(f), tup = std::make_tuple(std::forward<Args>(args)...)]() mutable {
                return std::apply(std::move(f), std::move(tup));
            });
        std::future<R> fut = task->get_future();
        {
            std::lock_guard<std::mutex> lk(m_);
            if (stop_) throw std::runtime_error("submit on a stopped ThreadPool");
            jobs_.emplace([task] { (*task)(); });
        }
        cv_.notify_one();
        return fut;
    }

    std::size_t size() const { return workers_.size(); }

private:
    void run() {
        for (;;) {
            std::function<void()> job;
            {
                std::unique_lock<std::mutex> lk(m_);
                cv_.wait(lk, [&] { return stop_ || !jobs_.empty(); });
                if (jobs_.empty()) return;  // stop_ and nothing left to do
                job = std::move(jobs_.front());
                jobs_.pop();
            }
            job();  // packaged_task catches exceptions into the future
        }
    }

    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> jobs_;
    std::mutex m_;
    std::condition_variable cv_;
    bool stop_ = false;
};
```

## Complexity

- Time: O(1) queue work per `submit`, plus one heap allocation for the shared `packaged_task` (and possibly one inside `std::function`).
- Space: O(queued tasks + threads).

## Interview follow-ups

- The single shared queue is a contention point: per-worker queues with **work stealing** (how TBB / Folly do it).
- Remove the per-task allocations: a move-only `std::move_only_function` (C++23) or a small-buffer job type.
- What happens if a task submits another task and waits on its future while every worker is busy doing the same? (Deadlock; how do you avoid it?)
- `shutdown_now()` that drops queued tasks: what should their futures report? (`broken_promise`.)
- In a low-latency system, why might you pin workers to cores and busy-poll instead of sleeping on a condition variable?
