#include <condition_variable>
#include <mutex>

class RWLock {
public:
    void lock_shared() {}
    bool try_lock_shared() { return false; }
    void unlock_shared() {}

    void lock() {}
    bool try_lock() { return false; }
    void unlock() {}
};
