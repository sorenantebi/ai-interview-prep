---
topic: "Smart Pointers & RAII"
difficulty: Medium
---
# Implement UniquePtr

**Topic:** Smart Pointers & RAII · **Difficulty:** Medium

## Problem

A trading engine owns lots of heap objects (strategy instances, order books per symbol, session handlers). Exclusive ownership expressed in the type keeps those lifetimes obvious: exactly one owner, the object is freed when the owner goes away, and handing it to someone else is an explicit move. That is `std::unique_ptr`, and writing it from scratch is a standard warm-up in C++ rounds because it tests move semantics, deleted copies and self-assignment in a few lines.

Implement a class template `UniquePtr<T>` that owns a single object allocated with `new` and frees it with `delete`:

```cpp
template <class T>
class UniquePtr {
public:
    UniquePtr() noexcept;                       // owns nothing
    explicit UniquePtr(T* p) noexcept;          // takes ownership of p (may be nullptr)
    ~UniquePtr();                               // deletes the owned object, if any

    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    UniquePtr(UniquePtr&& other) noexcept;               // other ends up empty
    UniquePtr& operator=(UniquePtr&& other) noexcept;    // frees the current object first

    T* get() const noexcept;                    // the raw pointer, ownership unchanged
    T* release() noexcept;                      // gives up ownership without deleting
    void reset(T* p = nullptr) noexcept;        // deletes the current object, then owns p

    T& operator*() const;
    T* operator->() const noexcept;
    explicit operator bool() const noexcept;    // true if it owns an object
};
```

A custom deleter is not required.

## Examples

**Example 1**
```cpp
{
    UniquePtr<Order> p(new Order{42});
    p->id;          // 42
    (*p).id = 7;
    bool(p);        // true
}                   // the Order is deleted here, exactly once
```

**Example 2**
```cpp
UniquePtr<int> a(new int(5));
UniquePtr<int> b(std::move(a));
bool(a);            // false: a is empty after the move
*b;                 // 5
a = std::move(b);   // ownership comes back
*a;                 // 5
bool(b);            // false
```

## Constraints

- Every object is deleted exactly once: no leaks and no double deletes, including after moves, `reset` and `release`.
- Moving a pointer onto itself (`p = std::move(p)`) must leave `p` owning its object.
- `UniquePtr` must not be copyable.
- All operations are O(1); `sizeof(UniquePtr<T>)` should be the size of one pointer.
