---
topic: "Smart Pointers & RAII"
difficulty: Hard
---
# Implement SharedPtr and WeakPtr with a Shared Control Block - Solution

## Intuition

Two lifetimes are in play: the object's and the bookkeeping's. The object lives while `strong > 0`. The control block must outlive every `WeakPtr`, because `expired()` reads the strong count from it. So the block is freed only when both counts are zero.

A clean way to get "both are zero" without a race is the trick `std::shared_ptr` implementations use: **all strong owners together hold one weak reference**. The weak count starts at 1. When the strong count drops to 0, that thread deletes the object and then drops the group's weak reference. Whoever takes the weak count to 0 frees the block. There is now a single counter that decides when the block dies, so no two threads can both think they are last.

`lock()` must not do a blind `++strong`: if the count is already 0 the object is gone (or being destroyed). It uses a compare-and-swap loop that only increments a non-zero count.

## Approach

1. `ControlBlock { T* ptr; std::atomic<long> strong{1}; std::atomic<long> weak{1}; }`.
2. `SharedPtr` copy: `strong.fetch_add(1)`. Release: if `strong.fetch_sub(1) == 1`, `delete ptr`, then `release_weak()`.
3. `release_weak()`: if `weak.fetch_sub(1) == 1`, `delete cb`.
4. `WeakPtr` from a `SharedPtr` or another `WeakPtr`: `weak.fetch_add(1)`. Destructor: `release_weak()`.
5. `lock()`: load `strong`; while it is non-zero, try `compare_exchange_weak(n, n + 1)`. On success build a `SharedPtr` around the block *without* incrementing again (a private constructor, reached through `friend`). If it is 0, return an empty `SharedPtr`.
6. Assignments use copy-and-swap so self-assignment is automatically safe.

## Code

```cpp
#include <atomic>
#include <cstddef>
#include <stdexcept>
#include <utility>

template <class T> class WeakPtr;

namespace detail {
template <class T>
struct ControlBlock {
    explicit ControlBlock(T* p) : ptr(p) {}
    T* ptr;
    std::atomic<long> strong{1};
    std::atomic<long> weak{1};  // +1 held collectively by all strong owners

    void release_weak() noexcept {
        if (weak.fetch_sub(1, std::memory_order_acq_rel) == 1) delete this;
    }
    void release_strong() noexcept {
        if (strong.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            delete ptr;
            ptr = nullptr;
            release_weak();
        }
    }
};
}  // namespace detail

template <class T>
class SharedPtr {
public:
    SharedPtr() noexcept = default;
    explicit SharedPtr(T* p) {
        if (p) cb_ = new detail::ControlBlock<T>(p);
    }
    SharedPtr(const SharedPtr& other) noexcept : cb_(other.cb_) {
        if (cb_) cb_->strong.fetch_add(1, std::memory_order_relaxed);
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
    ~SharedPtr() {
        if (cb_) cb_->release_strong();
    }

    void reset() noexcept { SharedPtr().swap(*this); }
    T* get() const noexcept { return cb_ ? cb_->ptr : nullptr; }
    long use_count() const noexcept { return cb_ ? cb_->strong.load(std::memory_order_relaxed) : 0; }
    T& operator*() const { return *get(); }
    T* operator->() const noexcept { return get(); }
    explicit operator bool() const noexcept { return get() != nullptr; }
    void swap(SharedPtr& other) noexcept { std::swap(cb_, other.cb_); }

private:
    friend class WeakPtr<T>;
    // Adopts a strong reference that the caller already added (used by lock()).
    explicit SharedPtr(detail::ControlBlock<T>* cb) noexcept : cb_(cb) {}

    detail::ControlBlock<T>* cb_ = nullptr;
};

template <class T>
class WeakPtr {
public:
    WeakPtr() noexcept = default;
    WeakPtr(const SharedPtr<T>& s) noexcept : cb_(s.cb_) { add_weak(); }
    WeakPtr(const WeakPtr& other) noexcept : cb_(other.cb_) { add_weak(); }
    WeakPtr(WeakPtr&& other) noexcept : cb_(std::exchange(other.cb_, nullptr)) {}
    WeakPtr& operator=(const WeakPtr& other) noexcept {
        WeakPtr(other).swap(*this);
        return *this;
    }
    WeakPtr& operator=(WeakPtr&& other) noexcept {
        WeakPtr(std::move(other)).swap(*this);
        return *this;
    }
    ~WeakPtr() {
        if (cb_) cb_->release_weak();
    }

    void reset() noexcept { WeakPtr().swap(*this); }
    long use_count() const noexcept { return cb_ ? cb_->strong.load(std::memory_order_relaxed) : 0; }
    bool expired() const noexcept { return use_count() == 0; }

    SharedPtr<T> lock() const noexcept {
        if (!cb_) return SharedPtr<T>();
        long n = cb_->strong.load(std::memory_order_relaxed);
        while (n != 0) {
            if (cb_->strong.compare_exchange_weak(n, n + 1, std::memory_order_acq_rel, std::memory_order_relaxed))
                return SharedPtr<T>(cb_);
        }
        return SharedPtr<T>();
    }

    void swap(WeakPtr& other) noexcept { std::swap(cb_, other.cb_); }

private:
    void add_weak() noexcept {
        if (cb_) cb_->weak.fetch_add(1, std::memory_order_relaxed);
    }
    detail::ControlBlock<T>* cb_ = nullptr;
};
```

## Complexity

- Time: O(1) per operation; `lock()` is a CAS loop that only retries when another thread changes the count at the same moment.
- Space: one pointer per handle, one control block (pointer + two counters) per managed object.

## Interview follow-ups

- Why can't `lock()` simply do `if (!expired()) return SharedPtr(copy)`? Describe the interleaving that resurrects a dying object.
- With a single allocation for object and control block (`make_shared`), when is the object's *memory* returned if weak pointers remain? Why can that matter for large objects?
- Implement `enable_shared_from_this`: how does an object get a `SharedPtr` to itself without creating a second control block?
- Show a parent/child cycle of `SharedPtr`s that leaks, and fix it with a `WeakPtr`.
- What memory orderings does each operation need, and which could be relaxed?
