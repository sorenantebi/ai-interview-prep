---
topic: "Lock-free & Atomics"
difficulty: Easy
---
# Test-and-Test-and-Set Spinlock

**Topic:** Lock-free & Atomics · **Difficulty:** Easy

## Problem

On an isolated core that must react within a microsecond, putting a thread to sleep on a contended `std::mutex` (a syscall plus a reschedule) is too slow. For very short critical sections, such as updating a position or swapping a pointer, HFT code often uses a **spinlock**: a waiting thread keeps the CPU and retries until the lock is free.

Implement a spinlock on top of `std::atomic<bool>` (or `std::atomic_flag`) using the **test-and-test-and-set** pattern: while the lock is taken, spin on a plain load and attempt the atomic exchange only once it looks free.

```cpp
class SpinLock {
public:
    void lock() noexcept;
    bool try_lock() noexcept;   // one attempt, never spins
    void unlock() noexcept;
};
```

It must meet the *Lockable* requirements, so `std::lock_guard<SpinLock>`, `std::unique_lock<SpinLock>` and `std::scoped_lock` work with it.

## Examples

**Example 1**
```cpp
SpinLock s;
s.try_lock();   // true
s.try_lock();   // false: already held
s.unlock();
s.try_lock();   // true
s.unlock();
```

**Example 2**
```cpp
SpinLock s;
long counter = 0;   // plain long, protected only by s
// 4 threads, each doing 100000 times: { std::lock_guard<SpinLock> g(s); ++counter; }
counter;            // exactly 400000
```

## Constraints

- Use acquire ordering when taking the lock and release ordering when giving it up (no stronger than needed).
- The spinning part must not hammer the cache line with read-modify-write operations: spin on a load.
- Not recursive: locking twice from the same thread deadlocks (that is fine, do not test it).
