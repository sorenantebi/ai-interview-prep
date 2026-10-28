---
topic: "Smart Pointers & RAII"
difficulty: Hard
---
# Implement SharedPtr with a Thread-Safe Reference Count

**Topic:** Smart Pointers & RAII · **Difficulty:** Hard

## Problem

Some objects in a trading system have no single obvious owner: a reference-data snapshot (instrument definitions, tick sizes) is read by several strategy threads while a loader thread publishes a new one. Shared ownership with a reference count lets the old snapshot live exactly as long as the last reader still holds it. Interviewers like this problem because the count must be updated atomically, and the "who deletes" decision has to be made by exactly one thread.

Implement `SharedPtr<T>`, a reference-counted owner of an object allocated with `new`, plus a `make_shared_ptr` helper:

```cpp
template <class T>
class SharedPtr {
public:
    SharedPtr() noexcept;                         // empty, use_count() == 0
    explicit SharedPtr(T* p);                     // takes ownership, use_count() == 1 (0 if p is null)
    SharedPtr(const SharedPtr& other) noexcept;   // shares ownership, count + 1
    SharedPtr(SharedPtr&& other) noexcept;        // steals ownership, count unchanged, other empty
    SharedPtr& operator=(const SharedPtr& other) noexcept;
    SharedPtr& operator=(SharedPtr&& other) noexcept;
    ~SharedPtr();                                 // count - 1; the last owner deletes the object

    void reset() noexcept;                        // drop ownership, become empty
    void reset(T* p);                             // drop ownership, then own p alone

    T* get() const noexcept;
    long use_count() const noexcept;              // number of SharedPtrs owning the object, 0 if empty
    T& operator*() const;
    T* operator->() const noexcept;
    explicit operator bool() const noexcept;
};

template <class T, class... Args>
SharedPtr<T> make_shared_ptr(Args&&... args);     // SharedPtr<T>(new T(args...))
```

## Examples

**Example 1**
```cpp
SharedPtr<int> a(new int(10));
a.use_count();            // 1
{
    SharedPtr<int> b = a; // copy
    a.use_count();        // 2
    *b = 11;
}
a.use_count();            // 1
*a;                       // 11
```

**Example 2**
```cpp
SharedPtr<Snapshot> s = make_shared_ptr<Snapshot>(7);
SharedPtr<Snapshot> t = std::move(s);
bool(s);                  // false
t.use_count();            // 1
t.reset();                // the Snapshot is deleted here
```

## Constraints

- The object is deleted exactly once, by whichever `SharedPtr` drops the count to 0. The count's own storage must be freed too (no leaks).
- Copying and destroying `SharedPtr`s that share one object from several threads at the same time must be safe (each individual `SharedPtr` instance is used by one thread at a time, like `std::shared_ptr`).
- Self-assignment (copy or move) must not change the count or delete the object.
- All operations are O(1).
