#include <stdexcept>

template <class Mutex>
class LockGuard {
public:
    explicit LockGuard(Mutex& m) {}
    ~LockGuard() {}
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
};

template <class Mutex>
class UniqueLock {
public:
    explicit UniqueLock(Mutex& m) {}
    ~UniqueLock() {}
    UniqueLock(const UniqueLock&) = delete;
    UniqueLock& operator=(const UniqueLock&) = delete;

    void lock() {}
    void unlock() {}
    bool owns_lock() const { return false; }
};
