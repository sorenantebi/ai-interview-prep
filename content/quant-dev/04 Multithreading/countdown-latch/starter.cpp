#include <condition_variable>
#include <cstddef>
#include <mutex>

class CountDownLatch {
public:
    explicit CountDownLatch(std::ptrdiff_t count) {}
    void count_down(std::ptrdiff_t n = 1) {}
    void wait() {}  // must block until the count is 0
    bool try_wait() const { return false; }
};

class Barrier {
public:
    explicit Barrier(std::ptrdiff_t num_threads) {}
    void arrive_and_wait() {}  // must block until every thread of this phase arrived
};
