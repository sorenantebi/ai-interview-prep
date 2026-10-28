---
topic: "Multithreading"
difficulty: Easy
---
# RAII Lock Guard

**Topic:** Multithreading · **Difficulty:** Easy

## Problem

In a trading engine, an order book or a position table is shared between the market-data thread and the strategy thread. Forgetting to unlock a mutex on an early `return` or an exception freezes the whole engine. RAII guards make that impossible: the lock is tied to the lifetime of a stack object.

Implement two guards that work with any type that has `lock()` and `unlock()` (a `std::mutex`, or your own spinlock):

```cpp
template <class Mutex>
class LockGuard {
public:
    explicit LockGuard(Mutex& m);   // locks m
    ~LockGuard();                    // unlocks m
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
};

template <class Mutex>
class UniqueLock {
public:
    explicit UniqueLock(Mutex& m);  // locks m, owns_lock() == true
    ~UniqueLock();                   // unlocks m only if it still owns it
    UniqueLock(const UniqueLock&) = delete;
    UniqueLock& operator=(const UniqueLock&) = delete;

    void lock();                     // throws std::logic_error if it already owns the lock
    void unlock();                   // throws std::logic_error if it does not own the lock
    bool owns_lock() const;
};
```

## Examples

**Example 1**
```cpp
std::mutex m;
int counter = 0;
{
    LockGuard<std::mutex> g(m);  // m locked
    ++counter;
}                                // m unlocked here
m.try_lock();                    // true: nobody holds it
```

**Example 2**
```cpp
std::mutex m;
UniqueLock<std::mutex> ul(m);
ul.owns_lock();   // true
ul.unlock();
ul.owns_lock();   // false
ul.unlock();      // throws std::logic_error
ul.lock();
ul.owns_lock();   // true
                  // destructor unlocks
```

## Constraints

- Each guard calls `lock()` exactly once on construction and `unlock()` exactly once for every successful lock: never double-unlock, never leak a lock, also when the scope is left by an exception.
- Neither guard may be copied.
- The guards themselves are used by one thread at a time; the mutex they wrap is what protects shared data across threads.
