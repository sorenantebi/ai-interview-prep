---
topic: "Lock-free & Atomics"
difficulty: Easy
---
# Atomic Max and Fetch-Multiply - Solution

## Intuition

`compare_exchange_weak(expected, desired)` stores `desired` only if the variable still equals `expected`; if not, it fails **and writes the current value into `expected`**. So the loop is: compute the new value from what you last saw, try to swap it in, and on failure you already hold the fresh value to recompute from. Every successful CAS is one atomic step, so no other thread's update can be lost.

For max there is a shortcut: once the current value is already `>= value`, there is nothing to do, and we exit without writing.

## Approach

1. `cur = target.load(relaxed)`.
2. **update_max**: `while (cur < value && !target.compare_exchange_weak(cur, value, ...)) {}`. Exit either because the stored value is already large enough or because our CAS succeeded. Return `cur`, which is the value before (on success it still holds the expected value we replaced).
3. **fetch_multiply**: `while (!target.compare_exchange_weak(cur, cur * factor, ...)) {}`, return `cur`.

`compare_exchange_weak` may fail spuriously (on LL/SC architectures like ARM), which is harmless inside a loop and cheaper than `_strong` there.

**Memory ordering.** A statistic like a running max does not publish any other data, so `relaxed` is enough for atomicity. If other threads use the value to decide something about data written before the update, use `acq_rel` on success and `acquire` on failure.

## Code

```cpp
#include <atomic>
#include <cstdint>

std::int64_t update_max(std::atomic<std::int64_t>& target, std::int64_t value) {
    std::int64_t cur = target.load(std::memory_order_relaxed);
    while (cur < value &&
           !target.compare_exchange_weak(cur, value, std::memory_order_relaxed, std::memory_order_relaxed)) {
        // cur now holds the latest value; loop re-checks whether we still need to write
    }
    return cur;
}

std::int64_t fetch_multiply(std::atomic<std::int64_t>& target, std::int64_t factor) {
    std::int64_t cur = target.load(std::memory_order_relaxed);
    while (!target.compare_exchange_weak(cur, cur * factor, std::memory_order_relaxed,
                                         std::memory_order_relaxed)) {
    }
    return cur;
}
```

## Complexity

- Time: O(1) expected per call; under heavy contention a thread may retry, but some thread always succeeds (lock-free, not wait-free).
- Space: O(1).

## Interview follow-ups

- `compare_exchange_weak` vs `_strong`: when does spurious failure happen and when do you need `_strong`? (A single CAS outside a loop.)
- Why is a CAS loop under contention slower than `fetch_add`? (`lock xadd` always succeeds in one go; CAS loops retry and keep the line bouncing.) How would you reduce contention for a hot max? (Per-thread maxima merged on read.)
- Generalise to `template <class F> T fetch_update(std::atomic<T>&, F f)`.
- Doing the same for `double`: `std::atomic<double>` CAS compares bit patterns: what happens with `-0.0` and NaN?
- C++26 adds `fetch_max` / `fetch_min`; on which hardware can they be a single instruction (e.g. ARMv8.1 `LDSMAX`)?
