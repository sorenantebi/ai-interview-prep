---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# Lock-Free SPSC Queue - Solution

## Intuition

Each index has exactly one writer: only the producer moves `tail_`, only the consumer moves `head_`. So neither side ever needs a read-modify-write; it just reads the other side's index to see how much room or data there is, and publishes its own with a store.

Let both indices grow forever (a 64-bit counter never wraps in practice) and map them into the buffer with `& mask_`. Then `tail_ - head_` is the number of items, `== 0` means empty and `== capacity` means full, with no wasted slot and no ambiguity.

The ordering is the classic message-passing pattern:

- Producer: write the slot, **then** `tail_.store(t + 1, release)`. A consumer that sees the new tail with an **acquire** load is guaranteed to see the slot's contents.
- Consumer: read the slot, **then** `head_.store(h + 1, release)`. The producer's acquire load of `head_` guarantees the consumer has finished reading that slot before the producer overwrites it.

## Approach

1. Constructor: round `capacity` up to a power of two, allocate the buffer once, `mask_ = cap - 1`.
2. `try_push`: `t = tail_` (relaxed, we own it); `h = head_` (acquire); if `t - h == cap` return false; write `buf_[t & mask_]`; `tail_.store(t + 1, release)`.
3. `try_pop`: `h = head_` (relaxed); `t = tail_` (acquire); if `h == t` return nullopt; read `buf_[h & mask_]`; `head_.store(h + 1, release)`.
4. Put `head_` and `tail_` on separate cache lines with `alignas(64)`. Otherwise every push invalidates the consumer's cache line and vice versa even though they write different variables (false sharing).

## Code

```cpp
#include <atomic>
#include <cstddef>
#include <memory>
#include <optional>

template <class T>
class SPSCQueue {
public:
    explicit SPSCQueue(std::size_t capacity)
        : cap_(round_up(capacity)), mask_(cap_ - 1), buf_(std::make_unique<T[]>(cap_)) {}

    bool try_push(const T& value) {
        const std::size_t t = tail_.load(std::memory_order_relaxed);
        if (t - head_.load(std::memory_order_acquire) == cap_) return false;  // full
        buf_[t & mask_] = value;
        tail_.store(t + 1, std::memory_order_release);  // publish the slot
        return true;
    }

    std::optional<T> try_pop() {
        const std::size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return std::nullopt;  // empty
        std::optional<T> out(std::move(buf_[h & mask_]));
        head_.store(h + 1, std::memory_order_release);  // hand the slot back
        return out;
    }

    std::size_t capacity() const { return cap_; }

    bool empty() const {
        return head_.load(std::memory_order_acquire) == tail_.load(std::memory_order_acquire);
    }

private:
    static std::size_t round_up(std::size_t n) {
        std::size_t p = 1;
        while (p < n) p <<= 1;
        return p;
    }

    alignas(64) std::atomic<std::size_t> head_{0};  // written by the consumer only
    alignas(64) std::atomic<std::size_t> tail_{0};  // written by the producer only
    alignas(64) const std::size_t cap_;             // read-only after construction
    const std::size_t mask_;
    std::unique_ptr<T[]> buf_;
};
```

## Complexity

- Time: O(1) per operation: one relaxed load, one acquire load, one release store. On x86 all of these are plain `mov`s; the ordering costs only compiler restrictions.
- Space: O(capacity), allocated once.

## Interview follow-ups

- **Cache the other side's index**: the producer keeps a private copy of `head_` and only re-reads the shared one when the queue looks full (and the consumer likewise for `tail_`). This removes most cross-core traffic and is the main trick in fast SPSC queues such as Rigtorp's.
- Why is `memory_order_relaxed` on the `tail_` store wrong even on x86? (The compiler may reorder the slot write after it.)
- Why `& mask_` instead of `%`, and why must the capacity be a power of two for the free-running counters to work with any capacity? (Counter overflow at 2^64 stays consistent only if the capacity divides 2^64.)
- How would you make it MPMC? (Per-slot sequence numbers plus `compare_exchange` on the indices, as in Vyukov's bounded queue.)
- Large `T`: construct in place (`emplace`) and pop by reference to avoid copies; also pad the buffer so slot 0 does not share a line with `cap_`.
- Busy-polling consumer vs. sleeping: what does the strategy thread do when the queue is empty?
