---
topic: "Multithreading"
difficulty: Easy
---
# RAII Lock Guard - Solution

## Intuition

Constructors and destructors are the only code C++ guarantees to run in pairs, even during stack unwinding. Put `lock()` in the constructor and `unlock()` in the destructor and the mutex can no longer leak. `UniqueLock` adds one bit of state, "do I currently own it?", so it can be unlocked early and the destructor knows whether there is anything left to release.

## Approach

1. `LockGuard` stores a reference to the mutex, locks in the constructor, unlocks in the destructor. Copying is deleted: two guards would unlock twice.
2. `UniqueLock` stores a pointer to the mutex plus `owns_`.
3. `lock()` / `unlock()` check `owns_` first and throw `std::logic_error` on misuse, then forward and flip `owns_`.
4. The destructor unlocks only if `owns_` is true.

## Code

```cpp
#include <stdexcept>

template <class Mutex>
class LockGuard {
public:
    explicit LockGuard(Mutex& m) : m_(m) { m_.lock(); }
    ~LockGuard() { m_.unlock(); }
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;

private:
    Mutex& m_;
};

template <class Mutex>
class UniqueLock {
public:
    explicit UniqueLock(Mutex& m) : m_(&m) { m_->lock(); owns_ = true; }
    ~UniqueLock() { if (owns_) m_->unlock(); }
    UniqueLock(const UniqueLock&) = delete;
    UniqueLock& operator=(const UniqueLock&) = delete;

    void lock() {
        if (owns_) throw std::logic_error("UniqueLock already owns the mutex");
        m_->lock();
        owns_ = true;
    }
    void unlock() {
        if (!owns_) throw std::logic_error("UniqueLock does not own the mutex");
        m_->unlock();
        owns_ = false;
    }
    bool owns_lock() const { return owns_; }

private:
    Mutex* m_;
    bool owns_ = false;
};
```

`owns_` is set only after `lock()` returns: if `lock()` throws, the constructor fails and the destructor never runs, so nothing is unlocked by mistake.

## Complexity

- Time: O(1) on top of the mutex's own cost.
- Space: one reference (plus one `bool` for `UniqueLock`).

## Interview follow-ups

- Add a move constructor to `UniqueLock` (the moved-from lock must not unlock) so it can be returned from a function.
- Why does `std::condition_variable::wait` take a `std::unique_lock` and not a `std::lock_guard`?
- `std::defer_lock`, `std::try_to_lock`, `std::adopt_lock`: what does each constructor tag do?
- Locking two mutexes without deadlock: `std::scoped_lock(a, b)` and lock ordering.
- `LockGuard<std::mutex>(m);` (an unnamed temporary) compiles but protects nothing: why, and how do `[[nodiscard]]` constructors help?
