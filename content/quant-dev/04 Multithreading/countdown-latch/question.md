---
topic: "Multithreading"
difficulty: Easy
---
# Countdown Latch and Barrier

**Topic:** Multithreading · **Difficulty:** Easy

## Problem

Two coordination primitives show up all over trading-system start-up and batch code:

- A **countdown latch** is a one-shot gate. The engine must not accept orders until the market-data, risk and gateway threads have each reported "ready": every component calls `count_down()`, and the main thread `wait()`s until the count reaches zero. Once open, it stays open.
- A **barrier** is reusable. In an end-of-day simulation, N worker threads each price a slice of the book for step *t*, and nobody may start step *t+1* until all N have finished step *t*. Each worker calls `arrive_and_wait()` at the end of every step.

Implement both with a mutex and a condition variable (not `std::latch` / `std::barrier`):

```cpp
class CountDownLatch {
public:
    explicit CountDownLatch(std::ptrdiff_t count);
    void count_down(std::ptrdiff_t n = 1);  // subtract n (the count never goes below 0)
    void wait();                             // block until the count is 0
    bool try_wait() const;                   // true if the count is already 0
};

class Barrier {
public:
    explicit Barrier(std::ptrdiff_t num_threads);
    void arrive_and_wait();  // block until num_threads threads have arrived in this phase,
                             // then all of them continue and the barrier resets for the next phase
};
```

## Examples

**Example 1**
```cpp
CountDownLatch ready(3);
ready.try_wait();     // false
ready.count_down();
ready.count_down(2);
ready.try_wait();     // true
ready.wait();         // returns immediately
```

**Example 2**
```cpp
CountDownLatch done(4);
std::vector<int> results(4);
std::vector<std::thread> workers;
for (int i = 0; i < 4; ++i)
    workers.emplace_back([&, i] { results[i] = i * i; done.count_down(); });
done.wait();          // after this, results == {0, 1, 4, 9} is visible to this thread
```

**Example 3**
```cpp
Barrier b(2);
// thread 1: step(0); b.arrive_and_wait(); step(1); b.arrive_and_wait();
// thread 2: step(0); b.arrive_and_wait(); step(1); b.arrive_and_wait();
// neither thread starts step(1) until both finished step(0)
```

## Constraints

- `0 <= count`, `1 <= num_threads`; any number of threads may call any member.
- `wait` / `arrive_and_wait` must sleep on a condition variable, not spin.
- Everything a thread wrote before `count_down()` / `arrive_and_wait()` must be visible to the threads released by it.
- The barrier is reused for many phases; a fast thread that re-arrives for the next phase must not slip through the current one.
