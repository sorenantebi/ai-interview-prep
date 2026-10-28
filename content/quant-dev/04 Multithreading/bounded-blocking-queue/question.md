---
topic: "Multithreading"
difficulty: Medium
---
# Bounded Blocking Queue

**Topic:** Multithreading · **Difficulty:** Medium

## Problem

An unbounded queue between a fast feed handler and a slow consumer (say, a logger or a database writer) just grows until the process runs out of memory. A bounded queue applies **back-pressure**: when it is full, the producer has to wait, or it gets an immediate "no" it can act on (drop, conflate, raise an alert).

Implement `BoundedBlockingQueue<T>` with a capacity fixed at construction, using a mutex and condition variables:

```cpp
template <class T>
class BoundedBlockingQueue {
public:
    explicit BoundedBlockingQueue(std::size_t capacity);
    void push(T value);              // blocks while the queue is full
    T pop();                         // blocks while the queue is empty
    bool try_push(T value);          // false immediately if full
    std::optional<T> try_pop();      // std::nullopt immediately if empty
    std::size_t size() const;
    std::size_t capacity() const;
};
```

## Examples

**Example 1**
```cpp
BoundedBlockingQueue<int> q(2);
q.try_push(1);   // true
q.try_push(2);   // true
q.try_push(3);   // false: full
q.pop();         // 1
q.try_push(3);   // true
q.pop();         // 2
q.pop();         // 3
q.try_pop();     // std::nullopt
```

**Example 2**
```cpp
BoundedBlockingQueue<int> q(1);
q.push(10);
std::thread producer([&] { q.push(20); });  // blocks: queue is full
q.pop();                                     // 10, frees a slot, producer continues
producer.join();
q.pop();                                     // 20
```

## Constraints

- `1 <= capacity <= 10^6`
- Any number of producer and consumer threads may run concurrently.
- `size()` never exceeds `capacity()`.
- Blocking calls must wait on a condition variable, not spin.
- No item is lost or delivered twice; a single producer's items come out in order.
