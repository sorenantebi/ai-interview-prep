---
topic: "Lock-free & Atomics"
difficulty: Easy
---
# Test-and-Test-and-Set Spinlock - Solution

## Intuition

The lock is one `std::atomic<bool>`. Taking it is `exchange(true)`: if the old value was `false`, we own it. The naive version calls `exchange` in a tight loop, but every `exchange` is a write, so each spinning core keeps pulling the cache line into exclusive state and the line bounces between cores, slowing down the owner too. Test-and-test-and-set spins on a **load** instead: all waiters share the line in read-only state and only retry the `exchange` when they see `false`.

## Approach

1. `lock`: loop: `if (!locked_.exchange(true, acquire)) return;` otherwise `while (locked_.load(relaxed)) cpu_relax();` and try again.
2. `try_lock`: cheap load first (do not write a line we would fail on anyway), then one `exchange`.
3. `unlock`: `locked_.store(false, release)`.

**Memory ordering.** The acquire on a successful `exchange` pairs with the release `store` in `unlock`: everything the previous owner wrote inside the critical section is visible to the next owner. The spinning load can be relaxed because it only decides when to retry; the `exchange` does the synchronising.

`cpu_relax()` emits the CPU's spin-wait hint (`pause` on x86, `yield` on ARM): it saves power, frees resources for the sibling hyper-thread, and avoids a memory-order mis-speculation penalty when the lock is released.

## Code

```cpp
#include <atomic>
#include <thread>
#if defined(__x86_64__) || defined(__i386__)
#include <immintrin.h>
#endif

inline void cpu_relax() noexcept {
#if defined(__x86_64__) || defined(__i386__)
    _mm_pause();
#elif defined(__aarch64__)
    asm volatile("yield");
#else
    std::this_thread::yield();
#endif
}

class SpinLock {
public:
    void lock() noexcept {
        for (;;) {
            if (!locked_.exchange(true, std::memory_order_acquire)) return;
            while (locked_.load(std::memory_order_relaxed)) cpu_relax();
        }
    }

    bool try_lock() noexcept {
        return !locked_.load(std::memory_order_relaxed) &&
               !locked_.exchange(true, std::memory_order_acquire);
    }

    void unlock() noexcept { locked_.store(false, std::memory_order_release); }

private:
    std::atomic<bool> locked_{false};
};
```

## Complexity

- Time: O(1) uncontended (one atomic exchange); under contention, unbounded spinning.
- Space: one byte (in practice, give it its own cache line: `alignas(64)`).

## Interview follow-ups

- Why is TTAS faster than TAS under contention? Explain in terms of the MESI cache-coherence protocol.
- A spinlock is not fair: one core can win repeatedly. Build a **ticket lock** (two counters) for FIFO fairness, or an MCS lock so each waiter spins on its own cache line.
- When is a spinlock *worse* than a mutex? (Oversubscribed cores, owner pre-empted while holding it, long critical sections.) Spin-then-park hybrids.
- Add exponential back-off to the spin loop.
- Why must the spinlock sit on its own cache line, apart from the data it protects and from other locks (false sharing)?
- `std::atomic_flag` is the only type guaranteed lock-free; in C++20 it also has `test()` for the TTAS read.
