#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T>
class UniquePtr {
public:
    UniquePtr() noexcept {}
    explicit UniquePtr(T* p) noexcept {}
    ~UniquePtr() {}

    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    UniquePtr(UniquePtr&& other) noexcept {}
    UniquePtr& operator=(UniquePtr&& other) noexcept { return *this; }

    T* get() const noexcept { return nullptr; }
    T* release() noexcept { return nullptr; }
    void reset(T* p = nullptr) noexcept {}

    T& operator*() const { throw std::logic_error("not implemented"); }
    T* operator->() const noexcept { return nullptr; }
    explicit operator bool() const noexcept { return false; }
};
