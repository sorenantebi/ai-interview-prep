---
topic: "Containers & Allocators"
difficulty: Easy
---
# Fixed-Capacity Ring Buffer - Solution

## Intuition

Keep a fixed array plus the index of the oldest element (`head_`) and a count. The next free slot is `(head_ + count_) % capacity`. Both ends move forward and wrap with the modulo, so nothing is ever shifted or reallocated.

## Approach

1. Allocate all `capacity` slots once in the constructor (`std::vector<std::optional<T>>`, so `T` needs no default constructor).
2. `push`: if full, return `false`; else write at `(head_ + count_) % cap` and grow `count_`.
3. `pop`: if empty, return `nullopt`; else move the value out of `head_`, advance `head_`, shrink `count_`.

## Code

```cpp
#include <cstddef>
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>

template <class T>
class RingBuffer {
public:
    explicit RingBuffer(std::size_t capacity) : slots_(capacity) {}

    bool push(const T& value) {
        if (full()) return false;
        slots_[(head_ + count_) % slots_.size()] = value;
        ++count_;
        return true;
    }

    std::optional<T> pop() {
        if (empty()) return std::nullopt;
        std::optional<T> out = std::move(slots_[head_]);
        slots_[head_].reset();
        head_ = (head_ + 1) % slots_.size();
        --count_;
        return out;
    }

    const T& front() const {
        if (empty()) throw std::out_of_range("RingBuffer is empty");
        return *slots_[head_];
    }

    std::size_t size() const { return count_; }
    std::size_t capacity() const { return slots_.size(); }
    bool empty() const { return count_ == 0; }
    bool full() const { return count_ == slots_.size(); }

private:
    std::vector<std::optional<T>> slots_;
    std::size_t head_ = 0, count_ = 0;
};
```

## Complexity

- Time: O(1) for every operation.
- Space: O(capacity), allocated once.

## Interview follow-ups

- Make the capacity a power of two and replace `%` with `& (cap - 1)`: why is that faster?
- Overwrite the oldest element when full instead of rejecting (a "last N ticks" window).
- Make it a lock-free single-producer / single-consumer queue (see Lock-free & Atomics).
