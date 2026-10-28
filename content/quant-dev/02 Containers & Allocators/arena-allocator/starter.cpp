#include <cstddef>
#include <cstdint>
#include <new>

class Arena {
public:
    explicit Arena(std::size_t bytes) {}
    ~Arena() {}
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    void* allocate(std::size_t size, std::size_t alignment = alignof(std::max_align_t)) { return nullptr; }
    void reset() noexcept {}
    std::size_t used() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
};
