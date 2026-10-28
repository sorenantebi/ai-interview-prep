---
topic: "Smart Pointers & RAII"
difficulty: Easy
---
# RAII Handle for an OS Resource

**Topic:** Smart Pointers & RAII · **Difficulty:** Easy

## Problem

A feed handler opens sockets, multicast groups, shared-memory segments and timer descriptors. Each is an integer id that must be passed to the right close function exactly once. Leaking one exhausts descriptors after a few reconnects; closing one twice may close a descriptor that has since been reused by another connection. Wrapping the id in a move-only RAII type makes both mistakes impossible.

Implement a class template `Handle<Closer>` that owns an integer resource id and calls `closer(id)` when it is done with it. `Closer` can be a function pointer type or a lambda type. The value `-1` means "no resource".

```cpp
template <class Closer>
class Handle {
public:
    Handle(int id, Closer closer);                 // owns id (may be -1)
    ~Handle();                                     // closer(id) if it owns a resource

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept;               // other is left owning -1
    Handle& operator=(Handle&& other) noexcept;    // closes the current resource first

    int get() const noexcept;                      // the id, or -1
    bool valid() const noexcept;                   // get() != -1
    int release() noexcept;                        // give up ownership without closing; returns the id
    void reset(int id = -1);                       // close the current resource (if any), then own id
};
```

This is the rule of five: destructor, two deleted copy operations, two move operations.

## Examples

**Example 1**
```cpp
std::vector<int> closed;  // what the fake close function recorded
void fake_close(int fd) { closed.push_back(fd); }

{
    Handle<void (*)(int)> h(3, fake_close);
    h.get();              // 3
    h.valid();            // true
}
closed;                   // {3}
```

**Example 2**
```cpp
Handle<void (*)(int)> a(4, fake_close);
Handle<void (*)(int)> b(5, fake_close);
a = std::move(b);         // closes 4, a now owns 5
b.valid();                // false
a.reset();                // closes 5
closed;                   // {4, 5}
```

## Constraints

- Every valid id is closed exactly once, and `-1` is never passed to the closer.
- Self move-assignment must leave the handle unchanged and close nothing.
- Move assignment is only used with closers that are themselves assignable (function pointers, captureless lambdas).
