---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# Lock-Free SPSC Queue

**Topic:** Lock-free & Atomics · **Difficulty:** Hard

## Problem

The workhorse of an HFT pipeline: the feed-handler thread decodes packets and passes them to the strategy thread, each pinned to its own core. With exactly **one producer and one consumer**, the hand-off needs no lock and no read-modify-write instruction at all, only one acquire load and one release store per operation. Done right, it moves an item between cores in a few tens of nanoseconds.

Implement a bounded, lock-free single-producer / single-consumer queue:

```cpp
template <class T>
class SPSCQueue {
public:
    explicit SPSCQueue(std::size_t capacity);  // rounded UP to the next power of two (>= 1)
    bool try_push(const T& value);             // producer thread only; false if full
    std::optional<T> try_pop();                // consumer thread only; std::nullopt if empty
    std::size_t capacity() const;              // the rounded capacity: that many items fit
    bool empty() const;                        // a snapshot; exact when called single-threaded
};
```

Requirements on the implementation:

- A fixed buffer allocated once in the constructor; indices wrap with `& (capacity - 1)`, not `%`.
- The producer's index (`tail`) and the consumer's index (`head`) are `std::atomic<std::size_t>`, each declared `alignas(64)` so they sit on different cache lines (no false sharing).
- Publish with release stores and observe with acquire loads; no mutex, no `compare_exchange`, no `fetch_add`.

## Examples

**Example 1**
```cpp
SPSCQueue<int> q(3);
q.capacity();   // 4
q.try_push(1); q.try_push(2); q.try_push(3); q.try_push(4);   // all true
q.try_push(5);  // false: full
q.try_pop();    // 1
q.try_push(5);  // true: wrapped around
```

**Example 2**
```cpp
SPSCQueue<int> q(1024);
// producer thread: for (int i = 0; i < 1'000'000; ++i) while (!q.try_push(i)) {}
// consumer thread: pops 1'000'000 values and sees 0, 1, 2, ... in order
```

## Constraints

- `1 <= capacity <= 2^20`; `T` is default-constructible and copyable.
- At most one thread calls `try_push` and at most one (other) thread calls `try_pop` at any time.
- `try_push` and `try_pop` are O(1), never block and never allocate.
