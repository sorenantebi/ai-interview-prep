---
topic: "Smart Pointers & RAII"
difficulty: Easy
---
# RAII Handle for an OS Resource - Solution

## Intuition

It is `unique_ptr` for an `int`: the "null" value is `-1` and "delete" is the stored closer. Moves hand the id over and set the source to `-1`, so only one handle ever closes a given id. Everything funnels through `reset`, which is the single place that calls the closer.

## Approach

1. Members: `int id_` and `Closer closer_`.
2. `reset(id)`: swap the new id in first, then close the old one if it was valid. Swapping first means the handle never refers to an id that is being closed.
3. Destructor: `reset()`.
4. Move constructor: take `other`'s id with `std::exchange(other.id_, -1)`, copy or move the closer.
5. Move assignment: if `this != &other`, `reset(other.release())` and move the closer. The self check matters here because the closer is reassigned too.
6. `release()`: `std::exchange(id_, -1)`.

## Code

```cpp
#include <utility>

template <class Closer>
class Handle {
public:
    Handle(int id, Closer closer) : id_(id), closer_(std::move(closer)) {}
    ~Handle() { reset(); }

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;

    Handle(Handle&& other) noexcept
        : id_(std::exchange(other.id_, -1)), closer_(std::move(other.closer_)) {}

    Handle& operator=(Handle&& other) noexcept {
        if (this != &other) {
            reset(other.release());
            closer_ = std::move(other.closer_);
        }
        return *this;
    }

    int get() const noexcept { return id_; }
    bool valid() const noexcept { return id_ != -1; }
    int release() noexcept { return std::exchange(id_, -1); }

    void reset(int id = -1) {
        int old = std::exchange(id_, id);
        if (old != -1) closer_(old);
    }

private:
    int id_;
    Closer closer_;
};
```

## Complexity

- Time: O(1) per operation (plus the closer).
- Space: one `int` plus the closer; a captureless lambda can cost zero bytes with `[[no_unique_address]]`.

## Interview follow-ups

- Make the invalid value a template parameter (some APIs use `0` or `nullptr` as "no handle").
- What should happen if `close()` fails (e.g. `EINTR`)? Can a destructor report it?
- Write a factory `open_socket(...)` that returns a `Handle` or throws, and show that a failure halfway through a constructor with two handles leaks nothing.
- Why is `Handle` better than `std::unique_ptr<int, Closer>` for file descriptors?
