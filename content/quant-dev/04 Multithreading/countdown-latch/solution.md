---
topic: "Multithreading"
difficulty: Easy
---
# Countdown Latch and Barrier - Solution

## Intuition

The latch is a counter behind a mutex: `count_down` decrements it and, when it hits zero, wakes everybody; `wait` sleeps until it is zero. Because the count never goes back up, there is nothing else to track.

The barrier is the same idea made reusable, and reuse is where the bug hides. If waiters only checked "has everybody arrived?", the last arriver resets the counter for the next phase and the sleepers would see "not everybody" and sleep forever (or a fast thread re-arriving would be counted in the wrong phase). The fix is a **generation number**: each waiter remembers the generation it arrived in and sleeps until the generation changes.

## Approach

**Latch**
1. `count_down(n)`: lock, `count_ = max(0, count_ - n)`; if it is now zero, `notify_all`.
2. `wait`: `cv_.wait(lk, [&]{ return count_ == 0; })`.
3. `try_wait`: read the count under the lock.

**Barrier**
1. `arrive_and_wait`: lock, remember `gen = generation_`, `++arrived_`.
2. If this thread is the last one: reset `arrived_ = 0`, `++generation_`, `notify_all`, return.
3. Otherwise wait until `generation_ != gen`.

The mutex gives the visibility guarantee: writes made before `count_down` / `arrive` happen-before the unlock, which happens-before the waiter's re-lock.

## Code

```cpp
#include <algorithm>
#include <condition_variable>
#include <cstddef>
#include <cstdint>
#include <mutex>

class CountDownLatch {
public:
    explicit CountDownLatch(std::ptrdiff_t count) : count_(count) {}

    void count_down(std::ptrdiff_t n = 1) {
        std::lock_guard<std::mutex> lk(m_);
        if (count_ == 0) return;
        count_ = std::max<std::ptrdiff_t>(0, count_ - n);
        if (count_ == 0) cv_.notify_all();
    }

    void wait() {
        std::unique_lock<std::mutex> lk(m_);
        cv_.wait(lk, [&] { return count_ == 0; });
    }

    bool try_wait() const {
        std::lock_guard<std::mutex> lk(m_);
        return count_ == 0;
    }

private:
    mutable std::mutex m_;
    std::condition_variable cv_;
    std::ptrdiff_t count_;
};

class Barrier {
public:
    explicit Barrier(std::ptrdiff_t num_threads) : n_(num_threads) {}

    void arrive_and_wait() {
        std::unique_lock<std::mutex> lk(m_);
        const std::uint64_t gen = generation_;
        if (++arrived_ == n_) {
            arrived_ = 0;
            ++generation_;
            cv_.notify_all();
            return;
        }
        cv_.wait(lk, [&] { return generation_ != gen; });
    }

private:
    std::mutex m_;
    std::condition_variable cv_;
    const std::ptrdiff_t n_;
    std::ptrdiff_t arrived_ = 0;
    std::uint64_t generation_ = 0;
};
```

## Complexity

- Time: O(1) per call; a release wakes all waiters (O(waiters) context switches).
- Space: O(1).

## Interview follow-ups

- Why does the barrier need a generation counter? Walk through the lost wake-up without it.
- `std::latch` / `std::barrier` (C++20): what does the barrier's completion function add (e.g. merge per-thread results once per phase)?
- A spinning barrier with an atomic counter and a "sense" flag (sense-reversing barrier): when is spinning better than sleeping?
- How would a worker drop out permanently (`arrive_and_drop`)?
- Latch vs. `std::future<void>` / `std::shared_future` for "wait until ready" signalling.
