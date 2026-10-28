---
topic: "Templates & Compile Time"
difficulty: Hard
---
# Optional from Scratch - Solution

## Intuition

Reserve `sizeof(T)` bytes aligned like `T`, plus a flag. A value only exists between a **placement new** into those bytes and an **explicit destructor call** (`ptr()->~T()`). Every member function is then a small case analysis on "is there a value here (and in the other one)?". If each path either constructs or destroys exactly once, the counts come out right.

## Approach

1. Members: `alignas(T) unsigned char storage_[sizeof(T)]` and `bool engaged_`. `ptr()` returns `std::launder(reinterpret_cast<T*>(storage_))`.
2. A private `construct(args...)` does `::new (static_cast<void*>(storage_)) T(std::forward<Args>(args)...)` and **then** sets `engaged_ = true`. If `T`'s constructor throws, the flag stays false, so the destructor won't destroy something that was never built.
3. `reset()`: if engaged, call `ptr()->~T()` and clear the flag.
4. Copy / move constructors: construct from `*other` only if `other` is engaged.
5. Assignment covers four cases: both engaged → `**this = *other` (assign the `T`); only `other` → construct; only `this` → `reset()`; neither → nothing. Self-assignment lands in "both engaged" and assigns the `T` to itself, which `T` must handle (or check `this != &other` first, as below).
6. `emplace`: `reset()` first, then construct, and return the new value.
7. `value()` checks the flag and throws `std::bad_optional_access`; `operator*` and `->` don't check (that's the point of the unchecked accessors).

## Code

```cpp
#include <cstddef>
#include <new>
#include <optional>  // only for std::bad_optional_access
#include <type_traits>
#include <utility>

template <class T>
class Optional {
public:
    Optional() noexcept {}
    Optional(const T& value) { construct(value); }
    Optional(T&& value) { construct(std::move(value)); }
    Optional(const Optional& other) {
        if (other.engaged_) construct(*other);
    }
    Optional(Optional&& other) noexcept(std::is_nothrow_move_constructible_v<T>) {
        if (other.engaged_) construct(std::move(*other));
    }

    Optional& operator=(const Optional& other) {
        if (this == &other) return *this;
        if (engaged_ && other.engaged_) **this = *other;
        else if (other.engaged_) construct(*other);
        else reset();
        return *this;
    }

    Optional& operator=(Optional&& other) noexcept(std::is_nothrow_move_constructible_v<T> &&
                                                   std::is_nothrow_move_assignable_v<T>) {
        if (this == &other) return *this;
        if (engaged_ && other.engaged_) **this = std::move(*other);
        else if (other.engaged_) construct(std::move(*other));
        else reset();
        return *this;
    }

    ~Optional() { reset(); }

    bool has_value() const noexcept { return engaged_; }
    explicit operator bool() const noexcept { return engaged_; }

    T& value() {
        if (!engaged_) throw std::bad_optional_access();
        return *ptr();
    }
    const T& value() const {
        if (!engaged_) throw std::bad_optional_access();
        return *ptr();
    }
    T& operator*() { return *ptr(); }
    const T& operator*() const { return *ptr(); }
    T* operator->() { return ptr(); }
    const T* operator->() const { return ptr(); }

    template <class... Args>
    T& emplace(Args&&... args) {
        reset();
        construct(std::forward<Args>(args)...);
        return *ptr();
    }

    void reset() noexcept {
        if (engaged_) {
            ptr()->~T();
            engaged_ = false;
        }
    }

private:
    T* ptr() { return std::launder(reinterpret_cast<T*>(storage_)); }
    const T* ptr() const { return std::launder(reinterpret_cast<const T*>(storage_)); }

    template <class... Args>
    void construct(Args&&... args) {
        ::new (static_cast<void*>(storage_)) T(std::forward<Args>(args)...);
        engaged_ = true;  // only after the constructor succeeded
    }

    alignas(T) unsigned char storage_[sizeof(T)];
    bool engaged_ = false;
};
```

## Complexity

- Time: O(1) per operation plus the cost of the `T` operation it performs.
- Space: `sizeof(T)` plus one `bool` (padded up to `alignof(T)`), all inline.

## Interview follow-ups

- Why `std::launder`? (The bytes are typed `unsigned char`; launder tells the compiler a new `T` object lives there, so it can't assume stale values.)
- Make `Optional<T>` trivially copyable / trivially destructible when `T` is (conditionally defaulted special members with `requires`). Why does that matter for passing it in registers and `memcpy`-ing messages?
- Use a `union { T value_; }` instead of a byte array. What changes, and why does that make a `constexpr` optional possible?
- What happens if `T`'s copy assignment throws halfway? What exception-safety guarantee does your `operator=` give?
- Add `value_or`, `operator==` and converting constructors from `Optional<U>`.
