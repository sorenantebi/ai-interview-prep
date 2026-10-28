---
topic: "Containers & Allocators"
difficulty: Easy
---
# Fixed-Capacity Ring Buffer

**Topic:** Containers & Allocators · **Difficulty:** Easy

## Problem

Market data handlers keep the last few ticks in a ring buffer: a fixed array that never allocates after construction, where the oldest element is overwritten or rejected when full.

Implement a class template `RingBuffer<T>` with a capacity fixed at construction:

```cpp
template <class T>
class RingBuffer {
public:
    explicit RingBuffer(std::size_t capacity);
    bool push(const T& value);      // false (and no change) if full
    std::optional<T> pop();         // oldest element, or std::nullopt if empty
    const T& front() const;         // oldest element; throws std::out_of_range if empty
    std::size_t size() const;
    std::size_t capacity() const;
    bool empty() const;
    bool full() const;
};
```

No allocation may happen in `push` or `pop`.

## Examples

**Example 1**
```cpp
RingBuffer<int> rb(2);
rb.push(1);      // true
rb.push(2);      // true
rb.push(3);      // false: full
rb.pop();        // 1
rb.push(3);      // true: wraps around
rb.pop();        // 2
rb.pop();        // 3
rb.pop();        // std::nullopt
```

**Example 2**
```cpp
RingBuffer<std::string> rb(3);
rb.push("a"); rb.push("b");
rb.front();      // "a"
rb.size();       // 2
rb.full();       // false
```

## Constraints

- `1 <= capacity <= 10^6`
- Every operation is O(1).
