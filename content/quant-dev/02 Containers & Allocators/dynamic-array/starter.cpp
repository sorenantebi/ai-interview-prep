#include <cstddef>
#include <memory>
#include <new>
#include <stdexcept>
#include <utility>

template <class T>
class Vector {
public:
    Vector() noexcept {}
    Vector(const Vector& other) {}
    Vector(Vector&& other) noexcept {}
    Vector& operator=(const Vector& other) { return *this; }
    Vector& operator=(Vector&& other) noexcept { return *this; }
    ~Vector() {}

    void push_back(const T& value) {}
    void push_back(T&& value) {}
    template <class... Args>
    T& emplace_back(Args&&... args) { throw std::logic_error("not implemented"); }
    void pop_back() {}
    void reserve(std::size_t n) {}
    void clear() noexcept {}

    std::size_t size() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
    bool empty() const noexcept { return true; }
    T& operator[](std::size_t i) { throw std::logic_error("not implemented"); }
    const T& operator[](std::size_t i) const { throw std::logic_error("not implemented"); }
    T& at(std::size_t i) { throw std::out_of_range("not implemented"); }
    const T& at(std::size_t i) const { throw std::out_of_range("not implemented"); }
};
