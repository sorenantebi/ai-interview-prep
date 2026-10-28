---
topic: "Smart Pointers & RAII"
difficulty: Hard
---
# Implement SharedPtr with a Thread-Safe Reference Count - Solution

## Intuition

All owners of one object must agree on a single counter, so the counter can't live inside any one `SharedPtr`: it goes in a separately allocated *control block* that every owner points to. Copying increments it, destroying decrements it, and whoever takes it from 1 to 0 deletes both the object and the control block.

With several threads, `++count` and `--count` must be atomic, and the "was I the last one?" test must come from the same atomic operation as the decrement. `fetch_sub` returns the old value, so exactly one thread sees `1`.

## Approach

1. `struct ControlBlock { T* ptr; std::atomic<long> count; }`. Each `SharedPtr` stores `ControlBlock* cb_` (null when empty).
2. Constructor from `T* p`: if `p` is non-null, allocate a control block with count 1.
3. Copy: point at the same block and `fetch_add(1, relaxed)`. Relaxed is enough: the copier already holds a reference, so the object cannot disappear under it.
4. Release (destructor, `reset`, assignment): `if (cb_->count.fetch_sub(1, acq_rel) == 1)` delete the object and the block. The release half makes each owner's writes visible to the deleting thread; the acquire half makes the deleter see them before it runs `~T`.
5. Copy assignment: copy first into a temporary, then swap (copy-and-swap). It handles self-assignment and gives the strong exception guarantee for free.
6. Move: take the pointer and null out the source; the count does not change.

## Code

```cpp
#include <atomic>
#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T>
class SharedPtr {
    struct ControlBlock {
        T* ptr;
        std::atomic<long> count;
    };

public:
    SharedPtr() noexcept = default;

    explicit SharedPtr(T* p) {
        if (p) cb_ = new ControlBlock{p, 1};
    }

    SharedPtr(const SharedPtr& other) noexcept : cb_(other.cb_) {
        if (cb_) cb_->count.fetch_add(1, std::memory_order_relaxed);
    }

    SharedPtr(SharedPtr&& other) noexcept : cb_(std::exchange(other.cb_, nullptr)) {}

    SharedPtr& operator=(const SharedPtr& other) noexcept {
        SharedPtr(other).swap(*this);
        return *this;
    }

    SharedPtr& operator=(SharedPtr&& other) noexcept {
        SharedPtr(std::move(other)).swap(*this);
        return *this;
    }

    ~SharedPtr() { release(); }

    void reset() noexcept { SharedPtr().swap(*this); }
    void reset(T* p) { SharedPtr(p).swap(*this); }

    T* get() const noexcept { return cb_ ? cb_->ptr : nullptr; }
    long use_count() const noexcept { return cb_ ? cb_->count.load(std::memory_order_relaxed) : 0; }
    T& operator*() const { return *get(); }
    T* operator->() const noexcept { return get(); }
    explicit operator bool() const noexcept { return get() != nullptr; }

    void swap(SharedPtr& other) noexcept { std::swap(cb_, other.cb_); }

private:
    void release() noexcept {
        if (cb_ && cb_->count.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            delete cb_->ptr;
            delete cb_;
        }
        cb_ = nullptr;
    }

    ControlBlock* cb_ = nullptr;
};

template <class T, class... Args>
SharedPtr<T> make_shared_ptr(Args&&... args) {
    return SharedPtr<T>(new T(std::forward<Args>(args)...));
}
```

## Complexity

- Time: O(1) per operation (one atomic read-modify-write for a copy or a release).
- Space: one pointer per `SharedPtr`, plus one control block (pointer + counter) per shared object.

## Interview follow-ups

- Real `std::make_shared` puts the object and the control block in one allocation. What does that save, and why does it keep the memory alive while `weak_ptr`s exist?
- Why does `std::shared_ptr` store the object pointer in the `shared_ptr` itself as well as in the control block? (Aliasing constructor, pointers to base classes.)
- Why is `fetch_add` allowed to be `relaxed` but `fetch_sub` is not?
- Is it safe for two threads to assign to the *same* `SharedPtr` object at once? What does `std::atomic<std::shared_ptr<T>>` add?
- Atomic reference counts cause cache-line contention when many cores copy one pointer. How would you avoid copying shared pointers on a hot path?
