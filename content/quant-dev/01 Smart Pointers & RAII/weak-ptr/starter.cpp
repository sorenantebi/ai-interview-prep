#include <atomic>
#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T> class WeakPtr;

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
    T* get() const noexcept { return nullptr; }
    long use_count() const noexcept { return 0; }
    T& operator*() const { throw std::logic_error("not implemented"); }
    T* operator->() const noexcept { return nullptr; }
    explicit operator bool() const noexcept { return false; }

private:
    friend class WeakPtr<T>;
};

template <class T>
class WeakPtr {
public:
    WeakPtr() noexcept {}
    WeakPtr(const SharedPtr<T>& s) noexcept {}
    WeakPtr(const WeakPtr& other) noexcept {}
    WeakPtr(WeakPtr&& other) noexcept {}
    WeakPtr& operator=(const WeakPtr& other) noexcept { return *this; }
    WeakPtr& operator=(WeakPtr&& other) noexcept { return *this; }
    ~WeakPtr() {}

    void reset() noexcept {}
    long use_count() const noexcept { return 0; }
    bool expired() const noexcept { return true; }
    SharedPtr<T> lock() const noexcept { return SharedPtr<T>(); }
};
