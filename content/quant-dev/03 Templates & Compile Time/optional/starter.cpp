#include <cstddef>
#include <new>
#include <optional>  // only for std::bad_optional_access
#include <stdexcept>
#include <type_traits>
#include <utility>

template <class T>
class Optional {
public:
    Optional() noexcept {}
    Optional(const T& value) {}
    Optional(T&& value) {}
    Optional(const Optional& other) {}
    Optional(Optional&& other) noexcept(std::is_nothrow_move_constructible_v<T>) {}
    Optional& operator=(const Optional& other) { return *this; }
    Optional& operator=(Optional&& other) noexcept(std::is_nothrow_move_constructible_v<T> &&
                                                   std::is_nothrow_move_assignable_v<T>) {
        return *this;
    }
    ~Optional() {}

    bool has_value() const noexcept { return false; }
    explicit operator bool() const noexcept { return false; }

    T& value() { throw std::bad_optional_access(); }
    const T& value() const { throw std::bad_optional_access(); }
    T& operator*() { throw std::logic_error("not implemented"); }
    const T& operator*() const { throw std::logic_error("not implemented"); }
    T* operator->() { return nullptr; }
    const T* operator->() const { return nullptr; }

    template <class... Args>
    T& emplace(Args&&... args) { throw std::logic_error("not implemented"); }

    void reset() noexcept {}

private:
    alignas(T) unsigned char storage_[sizeof(T)];
    bool engaged_ = false;
};
