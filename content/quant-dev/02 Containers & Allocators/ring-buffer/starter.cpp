#include <cstddef>
#include <optional>
#include <stdexcept>
#include <vector>

template <class T>
class RingBuffer {
public:
    explicit RingBuffer(std::size_t capacity) {}

    bool push(const T& value) { return false; }

    std::optional<T> pop() { return std::nullopt; }

    const T& front() const { throw std::out_of_range("empty"); }

    std::size_t size() const { return 0; }
    std::size_t capacity() const { return 0; }
    bool empty() const { return true; }
    bool full() const { return false; }
};
