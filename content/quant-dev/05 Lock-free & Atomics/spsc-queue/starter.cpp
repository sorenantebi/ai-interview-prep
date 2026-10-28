#include <atomic>
#include <cstddef>
#include <memory>
#include <optional>

template <class T>
class SPSCQueue {
public:
    explicit SPSCQueue(std::size_t capacity) {}

    bool try_push(const T& value) { return false; }

    std::optional<T> try_pop() { return std::nullopt; }

    std::size_t capacity() const { return 0; }

    bool empty() const { return true; }

private:
    // alignas(64) std::atomic<std::size_t> head_{0};  // consumer's index
    // alignas(64) std::atomic<std::size_t> tail_{0};  // producer's index
};
