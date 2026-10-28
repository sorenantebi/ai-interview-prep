#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>

template <class T>
class ThreadSafeQueue {
public:
    bool push(T value) { return false; }

    // Must block until an item arrives or the queue is closed and empty.
    std::optional<T> pop() { return std::nullopt; }

    std::optional<T> try_pop() { return std::nullopt; }

    void close() {}

    bool closed() const { return false; }

    std::size_t size() const { return 0; }
};
