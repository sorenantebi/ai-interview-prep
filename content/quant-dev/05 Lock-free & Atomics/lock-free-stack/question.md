---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# Lock-Free Treiber Stack

**Topic:** Lock-free & Atomics · **Difficulty:** Hard

## Problem

Object pools and free lists in low-latency systems (pre-allocated order objects, message buffers) are often LIFO stacks shared by several threads. A mutex-protected stack can stall every thread if the lock holder is pre-empted. The **Treiber stack** is the classic lock-free alternative: the stack is a singly linked list, and both `push` and `pop` swing the `head` pointer with a single `compare_exchange`.

Implement:

```cpp
template <class T>
class LockFreeStack {
public:
    LockFreeStack();
    ~LockFreeStack();                 // frees every node (single-threaded at that point)
    LockFreeStack(const LockFreeStack&) = delete;
    LockFreeStack& operator=(const LockFreeStack&) = delete;

    void push(T value);
    std::optional<T> pop();           // std::nullopt if empty
    bool empty() const;               // a snapshot
};
```

**Memory reclamation.** The hard part of lock-free structures is deciding when a popped node can be freed: another thread may still be reading its `next` pointer. Real systems use hazard pointers or epoch-based reclamation. Here, keep it simple and safe: **do not delete popped nodes in `pop`**. Put them on a "retired" list (itself pushed lock-free) and free them all in the destructor. Never reuse a popped node for a later push.

## Examples

**Example 1**
```cpp
LockFreeStack<int> s;
s.push(1);
s.push(2);
s.push(3);
s.pop();      // 3
s.pop();      // 2
s.empty();    // false
s.pop();      // 1
s.pop();      // std::nullopt
```

**Example 2**
```cpp
LockFreeStack<int> s;
// 4 threads, each pushing its own 10000 distinct values and popping some of them concurrently;
// afterwards, pop the rest: every pushed value came out exactly once.
```

## Constraints

- Any number of threads call `push` / `pop` concurrently. No mutex.
- Every value pushed is popped at most once; none is lost.
- Each operation is lock-free: a thread that fails its CAS retries, and some thread always makes progress.
- No memory leaks: the destructor frees every node, retired or still on the stack.
