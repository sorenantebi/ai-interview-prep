#include <cstddef>
#include <memory>
#include <new>
#include <utility>

template <class T, std::size_t N>
class ObjectPool {
public:
    ObjectPool() {}
    ~ObjectPool() {}
    ObjectPool(const ObjectPool&) = delete;
    ObjectPool& operator=(const ObjectPool&) = delete;

    template <class... Args>
    T* acquire(Args&&... args) { return nullptr; }
    void release(T* p) {}
    std::size_t available() const noexcept { return 0; }
    static constexpr std::size_t capacity() noexcept { return N; }
};
