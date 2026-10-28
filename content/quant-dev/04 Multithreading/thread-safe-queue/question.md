---
topic: "Multithreading"
difficulty: Medium
---
# Thread-Safe Queue with Close

**Topic:** Multithreading · **Difficulty:** Medium

## Problem

A gateway thread decodes exchange messages and hands them to worker threads that update books and risk. The hand-off is a queue shared by many producers and many consumers. Consumers must sleep (not spin) while there is no work, and at shutdown every consumer has to wake up, drain what is left and exit cleanly.

Implement an unbounded `ThreadSafeQueue<T>` using a `std::mutex` and a `std::condition_variable`:

```cpp
template <class T>
class ThreadSafeQueue {
public:
    bool push(T value);          // false (value dropped) if the queue is closed
    std::optional<T> pop();      // blocks until an item is available;
                                 // std::nullopt once the queue is closed AND empty
    std::optional<T> try_pop();  // never blocks; std::nullopt if empty right now
    void close();                // wakes every waiting pop(); later pushes are rejected
    bool closed() const;
    std::size_t size() const;
};
```

Items pushed before `close()` are still delivered: `pop()` returns `std::nullopt` only when the queue is both closed and drained.

## Examples

**Example 1**
```cpp
ThreadSafeQueue<int> q;
q.push(1);
q.push(2);
q.pop();       // 1
q.try_pop();   // 2
q.try_pop();   // std::nullopt (empty, does not block)
```

**Example 2**
```cpp
ThreadSafeQueue<int> q;
q.push(7);
q.close();
q.push(8);     // false: closed
q.pop();       // 7: still drained after close
q.pop();       // std::nullopt: closed and empty, returns immediately
```

**Example 3**
```cpp
ThreadSafeQueue<int> q;
std::thread consumer([&] { auto v = q.pop(); /* blocks, then v == 42 */ });
q.push(42);
consumer.join();
```

## Constraints

- Any number of threads may call any member concurrently.
- `pop()` must not busy-wait: it waits on the condition variable.
- No item is lost or delivered twice. FIFO order is kept for a single producer.
- `close()` may be called more than once.
