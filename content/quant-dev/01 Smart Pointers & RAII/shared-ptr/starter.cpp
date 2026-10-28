#include <atomic>
#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T>
class SharedPtr {
public:
    SharedPtr() noexcept {}
    explicit SharedPtr(T* p) {}
    SharedPtr(const SharedPtr& other) noexcept {}
    SharedPtr(SharedPtr&& other) noexcept {}
    SharedPtr& operator=(const SharedPtr& other) noexcept { return *this; }
    SharedPtr& operator=(SharedPtr&& other) noexcept { return *this; }
    ~SharedPtr() {}

    void reset() noexcept {}
    void reset(T* p) {}

    T* get() const noexcept { return nullptr; }
    long use_count() const noexcept { return 0; }
    T& operator*() const { throw std::logic_error("not implemented"); }
    T* operator->() const noexcept { return nullptr; }
    explicit operator bool() const noexcept { return false; }
};

template <class T, class... Args>
SharedPtr<T> make_shared_ptr(Args&&... args) {
    return SharedPtr<T>();
}
