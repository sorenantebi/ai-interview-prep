#include <atomic>
#include <thread>

class SpinLock {
public:
    void lock() noexcept {}
    bool try_lock() noexcept { return false; }
    void unlock() noexcept {}
};
