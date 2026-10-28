---
topic: "Containers & Allocators"
difficulty: Medium
---
# Implement a Dynamic Array (Vector) - Solution

## Intuition

Separate memory from objects. The buffer is raw storage for `capacity_` elements, obtained from `std::allocator<T>::allocate`, which constructs nothing. Slots `[0, size_)` hold live objects created with placement new (`std::construct_at`); slots `[size_, capacity_)` are just bytes. Every operation keeps that invariant: grow `size_` only after constructing, destroy before shrinking it.

Doubling the capacity when full makes `push_back` amortized O(1): after `n` pushes the total number of element moves is at most `1 + 2 + 4 + ... + n < 2n`.

## Approach

1. Members: `T* data_`, `size_`, `cap_`.
2. `emplace_back(args...)`:
   - if `size_ < cap_`, construct in place at `data_ + size_`;
   - otherwise allocate a buffer of `max(1, 2 * cap_)`, **construct the new element in it first** (the arguments may refer to an element of the old buffer, as in `v.push_back(v[0])`), then move the old elements across with `std::move_if_noexcept`, destroy them, and free the old buffer.
3. `push_back` forwards to `emplace_back`.
4. `pop_back`: decrement `size_`, then `std::destroy_at(data_ + size_)`.
5. `reserve(n)`: if `n > cap_`, move everything into a buffer of exactly `n`.
6. Copy constructor: allocate `other.size_` and copy-construct each element. Copy assignment: copy-and-swap. Moves: swap the three members.
7. Destructor: `clear()` (destroy all), then deallocate.

## Code

```cpp
#include <cstddef>
#include <memory>
#include <new>
#include <stdexcept>
#include <utility>

template <class T>
class Vector {
public:
    Vector() noexcept = default;

    Vector(const Vector& other) {
        reserve(other.size_);
        for (std::size_t i = 0; i < other.size_; ++i) emplace_back(other.data_[i]);
    }

    Vector(Vector&& other) noexcept { swap(other); }

    Vector& operator=(const Vector& other) {
        if (this != &other) Vector(other).swap(*this);
        return *this;
    }

    Vector& operator=(Vector&& other) noexcept {
        Vector(std::move(other)).swap(*this);
        return *this;
    }

    ~Vector() {
        clear();
        if (data_) std::allocator<T>().deallocate(data_, cap_);
    }

    void push_back(const T& value) { emplace_back(value); }
    void push_back(T&& value) { emplace_back(std::move(value)); }

    template <class... Args>
    T& emplace_back(Args&&... args) {
        if (size_ < cap_) {
            std::construct_at(data_ + size_, std::forward<Args>(args)...);
        } else {
            std::size_t new_cap = cap_ ? cap_ * 2 : 1;
            T* buf = std::allocator<T>().allocate(new_cap);
            // Build the new element first: args may point into the old buffer.
            std::construct_at(buf + size_, std::forward<Args>(args)...);
            relocate_into(buf, new_cap);
        }
        return data_[size_++];
    }

    void pop_back() {
        --size_;
        std::destroy_at(data_ + size_);
    }

    void reserve(std::size_t n) {
        if (n <= cap_) return;
        relocate_into(std::allocator<T>().allocate(n), n);
    }

    void clear() noexcept {
        while (size_) pop_back();
    }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return cap_; }
    bool empty() const noexcept { return size_ == 0; }

    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

    T& at(std::size_t i) {
        if (i >= size_) throw std::out_of_range("Vector::at");
        return data_[i];
    }
    const T& at(std::size_t i) const {
        if (i >= size_) throw std::out_of_range("Vector::at");
        return data_[i];
    }

    void swap(Vector& other) noexcept {
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
        std::swap(cap_, other.cap_);
    }

private:
    // Moves the size_ live elements into buf (capacity new_cap), then frees the old buffer.
    void relocate_into(T* buf, std::size_t new_cap) {
        for (std::size_t i = 0; i < size_; ++i) {
            std::construct_at(buf + i, std::move_if_noexcept(data_[i]));
            std::destroy_at(data_ + i);
        }
        if (data_) std::allocator<T>().deallocate(data_, cap_);
        data_ = buf;
        cap_ = new_cap;
    }

    T* data_ = nullptr;
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
};
```

## Complexity

- Time: `push_back` / `emplace_back` amortized O(1), worst case O(n) on a reallocation; `pop_back`, `operator[]`, `at` O(1); copy O(n); move O(1).
- Space: O(capacity), at most 2 × size after growth by pushes.

## Interview follow-ups

- Why `std::move_if_noexcept`? What guarantee does `std::vector::push_back` give if a move constructor can throw?
- Make reallocation exception safe: if constructing the new element or copying an old one throws, the vector must be unchanged.
- Growth factor 2 vs 1.5: why can 1.5 let the allocator reuse previously freed blocks?
- For trivially copyable `T`, replace the element-by-element move with `memcpy` / `realloc`. What C++ rules make that legal?
- On a hot path, how do you guarantee a vector never reallocates (reserve up front, fixed capacity, or a `static_vector`)?
