---
topic: "Multithreading"
difficulty: Medium
---
# Thread Pool with Futures

**Topic:** Multithreading · **Difficulty:** Medium

## Problem

Spawning a thread costs tens of microseconds; a pricing service that revalues a book of options on every tick cannot afford that per task. A thread pool starts its workers once and feeds them work through a queue. Callers get a `std::future` back so they can collect the result, or the exception, later.

Implement:

```cpp
class ThreadPool {
public:
    explicit ThreadPool(std::size_t num_threads);   // starts num_threads workers
    ~ThreadPool();                                   // runs every task already submitted, then joins

    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;

    template <class F, class... Args>
    auto submit(F&& f, Args&&... args) -> std::future<std::invoke_result_t<F, Args...>>;

    std::size_t size() const;                        // number of worker threads
};
```

`submit` queues `f(args...)` and returns a future for its result. If the task throws, the exception must come out of `future::get()`, and the worker must keep running.

## Examples

**Example 1**
```cpp
ThreadPool pool(4);
auto a = pool.submit([](int x, int y) { return x + y; }, 2, 3);
auto b = pool.submit([] { return std::string("fill"); });
a.get();   // 5
b.get();   // "fill"
```

**Example 2**
```cpp
ThreadPool pool(2);
auto f = pool.submit([]() -> int { throw std::runtime_error("bad price"); });
f.get();   // throws std::runtime_error("bad price")
pool.submit([] { return 1; }).get();   // 1: the pool still works
```

## Constraints

- `1 <= num_threads <= 64`
- `submit` may be called from several threads at once.
- Tasks run concurrently on up to `num_threads` threads (not one after another on a single thread).
- The destructor must not drop queued tasks: every future obtained from `submit` becomes ready.
- `void`-returning tasks give a `std::future<void>`.
