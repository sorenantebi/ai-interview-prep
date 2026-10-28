---
topic: "Lock-free & Atomics"
difficulty: Easy
---
# Atomic Max and Fetch-Multiply

**Topic:** Lock-free & Atomics · **Difficulty:** Easy

## Problem

Many threads record statistics into shared counters: the worst tick-to-trade latency seen today, the high-water mark of the order book depth. `std::atomic<int64_t>` gives you `fetch_add` but no `fetch_max` (that only arrives in C++26) and no `fetch_multiply`. Any such read-modify-write can be built from a **compare-and-swap loop**: read the current value, compute the new one, and `compare_exchange` it in; if another thread changed the value in between, retry with the fresh value.

Implement:

```cpp
// Atomically: target = max(target, value). Returns the value target held just before.
std::int64_t update_max(std::atomic<std::int64_t>& target, std::int64_t value);

// Atomically: target = target * factor. Returns the value target held just before.
std::int64_t fetch_multiply(std::atomic<std::int64_t>& target, std::int64_t factor);
```

## Examples

**Example 1**
```cpp
std::atomic<std::int64_t> worst{120};
update_max(worst, 95);    // returns 120, worst stays 120
update_max(worst, 340);   // returns 120, worst becomes 340
worst.load();             // 340
```

**Example 2**
```cpp
std::atomic<std::int64_t> x{3};
fetch_multiply(x, 5);     // returns 3, x becomes 15
fetch_multiply(x, -2);    // returns 15, x becomes -30
```

**Example 3**
```cpp
std::atomic<std::int64_t> x{1};
// 4 threads, each calling fetch_multiply(x, 2) ten times
x.load();                 // 1 << 40: no multiplication is lost
```

## Constraints

- Both functions are called concurrently from many threads; no update may be lost.
- Lock-free: use `compare_exchange_weak` / `compare_exchange_strong`, no mutex.
- `update_max` should not write to `target` at all when `value` is not larger (no needless cache-line invalidation).
- Products never overflow in the tests.
