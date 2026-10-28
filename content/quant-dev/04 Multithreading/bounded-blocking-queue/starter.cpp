#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>

template <class T>
class BoundedBlockingQueue {
public:
    explicit BoundedBlockingQueue(std::size_t capacity) {}

    // Must block while full.
    void push(T value) {}

    // Must block while empty.
    T pop() { return T{}; }

    bool try_push(T value) { return false; }

    std::optional<T> try_pop() { return std::nullopt; }

    std::size_t size() const { return 0; }
    std::size_t capacity() const { return 0; }
};
