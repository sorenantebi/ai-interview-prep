---
topic: "Multithreading"
difficulty: Hard
---
# Writer-Preferring Read-Write Lock

**Topic:** Multithreading · **Difficulty:** Hard

## Problem

A reference-data table (instrument specs, tick sizes, risk limits) is read on every order by many strategy threads, but updated only a few times a day. A plain mutex makes the readers queue behind each other for nothing. A read-write lock lets any number of readers in at once and gives a writer exclusive access.

The naive version has a nasty failure mode: if readers keep arriving, the reader count never drops to zero and a limit update can wait forever (**writer starvation**). Your lock must prefer writers: once a writer is waiting, newly arriving readers queue behind it.

Implement it with a `std::mutex` and condition variables:

```cpp
class RWLock {
public:
    void lock_shared();      // blocks while a writer holds the lock OR any writer is waiting
    bool try_lock_shared();  // same condition, but returns false instead of blocking
    void unlock_shared();

    void lock();             // blocks until no reader and no writer holds the lock
    bool try_lock();         // false instead of blocking
    void unlock();
};
```

Readers that already hold the lock keep it; the waiting writer gets in as soon as the last of them calls `unlock_shared()`, before any reader that arrived after it.

## Examples

**Example 1**
```cpp
RWLock rw;
rw.lock_shared();
rw.try_lock_shared();  // true: readers share
rw.try_lock();         // false: readers inside
rw.unlock_shared();
rw.unlock_shared();
rw.try_lock();         // true
rw.try_lock_shared();  // false: writer inside
rw.unlock();
```

**Example 2**
```cpp
RWLock rw;
rw.lock_shared();                                  // reader A is inside
std::thread w([&] { rw.lock(); /*...*/ rw.unlock(); });  // writer W waits for A
// once W is waiting:
rw.try_lock_shared();   // false: a new reader B may not overtake W
rw.unlock_shared();     // A leaves -> W runs, then B may enter
w.join();
```

## Constraints

- Any number of threads; each thread calls `unlock_shared` / `unlock` only for a lock it holds.
- No recursion or upgrade (a reader never asks for the write lock while holding the read lock).
- Blocking calls must sleep on a condition variable, not spin.
- `std::shared_mutex` is not allowed (that is the thing you are building).
