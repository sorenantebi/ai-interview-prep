---
topic: "Smart Pointers & RAII"
difficulty: Medium
---
# Implement UniquePtr - Solution

## Intuition

The whole class is one raw pointer plus a rule: whoever holds the non-null pointer is responsible for `delete`. Copying would create two owners, so copies are deleted. Moving hands the pointer over and nulls out the source, so only one destructor ever sees it.

## Approach

1. Store a single `T* ptr_`, null when empty.
2. Destructor: `delete ptr_` (deleting null is a no-op).
3. Move constructor: take `other.ptr_` and set it to null (`std::exchange` does both).
4. Move assignment: `reset(other.release())`. If `other` is `*this`, `release()` nulls our pointer and `reset` then takes the same pointer back without deleting anything, so self-move is safe with no special check.
5. `reset(p)`: swap in the new pointer first, then delete the old one. Doing it in that order means the object is never reachable through `*this` while its destructor runs.
6. `release()`: return the pointer and forget it.

## Code

```cpp
#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T>
class UniquePtr {
public:
    UniquePtr() noexcept = default;
    explicit UniquePtr(T* p) noexcept : ptr_(p) {}
    ~UniquePtr() { delete ptr_; }

    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;

    UniquePtr(UniquePtr&& other) noexcept : ptr_(std::exchange(other.ptr_, nullptr)) {}

    UniquePtr& operator=(UniquePtr&& other) noexcept {
        reset(other.release());  // also correct when &other == this
        return *this;
    }

    T* get() const noexcept { return ptr_; }
    T* release() noexcept { return std::exchange(ptr_, nullptr); }

    void reset(T* p = nullptr) noexcept {
        T* old = std::exchange(ptr_, p);
        delete old;
    }

    T& operator*() const { return *ptr_; }
    T* operator->() const noexcept { return ptr_; }
    explicit operator bool() const noexcept { return ptr_ != nullptr; }

private:
    T* ptr_ = nullptr;
};
```

## Complexity

- Time: O(1) for every operation.
- Space: one pointer per `UniquePtr`, no extra allocation.

## Interview follow-ups

- Add a custom deleter as a template parameter. How do you keep `sizeof` equal to one pointer when the deleter is an empty type (empty base optimization, or `[[no_unique_address]]`)?
- Support arrays (`UniquePtr<T[]>`) with `delete[]` and `operator[]`.
- Why is `make_unique` safer than `UniquePtr<T>(new T)` in a function call with several arguments (pre-C++17 evaluation order)?
- Why should the move operations be `noexcept`? (Hint: `std::vector` reallocation.)
- Allow converting `UniquePtr<Derived>` to `UniquePtr<Base>`. What must be true of `Base`'s destructor?
