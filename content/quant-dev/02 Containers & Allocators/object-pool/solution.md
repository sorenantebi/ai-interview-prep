---
topic: "Containers & Allocators"
difficulty: Medium
---
# Fixed-Capacity Object Pool - Solution

## Intuition

Keep an array of `N` slots, each big enough and aligned enough for one `T`. A free slot holds no object, so its bytes can store something else: a pointer to the next free slot. That gives an *intrusive* free list that costs no extra memory. `acquire` pops the head of the list and placement-news a `T` into it; `release` runs `~T` and pushes the slot back on the head. Both are O(1), and pushing and popping at the head is what makes reuse LIFO.

## Approach

1. `union Slot { Slot* next; alignas(T) unsigned char storage[sizeof(T)]; };` and `Slot slots_[N]`. The union has the size and alignment of the larger member.
2. Constructor: chain the slots, `slots_[i].next = &slots_[i + 1]`, last one `nullptr`; `free_ = &slots_[0]`.
3. `acquire(args...)`: if `free_` is null return `nullptr`. Otherwise construct `T` in `free_->storage` *first*, and only then pop the slot. If the constructor throws, the list is untouched.
4. `release(p)`: the slot's address equals `p` (the storage is at offset 0 of the union). Call `std::destroy_at(p)`, then push the slot.
5. For the destructor to clean up objects still in use, keep a `bool live_[N]` flag per slot (set on acquire, cleared on release).

## Code

```cpp
#include <cstddef>
#include <memory>
#include <new>
#include <utility>

template <class T, std::size_t N>
class ObjectPool {
    union Slot {
        Slot* next;
        alignas(T) unsigned char storage[sizeof(T)];
    };

public:
    ObjectPool() {
        for (std::size_t i = 0; i + 1 < N; ++i) slots_[i].next = &slots_[i + 1];
        slots_[N - 1].next = nullptr;
        free_ = &slots_[0];
    }

    ~ObjectPool() {
        for (std::size_t i = 0; i < N; ++i)
            if (live_[i]) std::destroy_at(object(&slots_[i]));
    }

    ObjectPool(const ObjectPool&) = delete;
    ObjectPool& operator=(const ObjectPool&) = delete;

    template <class... Args>
    T* acquire(Args&&... args) {
        if (!free_) return nullptr;
        Slot* s = free_;
        Slot* next = s->next;
        T* p = ::new (static_cast<void*>(s->storage)) T(std::forward<Args>(args)...);  // may throw: list untouched
        free_ = next;
        live_[s - slots_] = true;
        --available_;
        return p;
    }

    void release(T* p) {
        Slot* s = reinterpret_cast<Slot*>(p);
        std::destroy_at(p);
        live_[s - slots_] = false;
        s->next = free_;
        free_ = s;
        ++available_;
    }

    std::size_t available() const noexcept { return available_; }
    static constexpr std::size_t capacity() noexcept { return N; }

private:
    static T* object(Slot* s) { return std::launder(reinterpret_cast<T*>(s->storage)); }

    Slot slots_[N];
    bool live_[N] = {};
    Slot* free_ = nullptr;
    std::size_t available_ = N;
};
```

## Complexity

- Time: O(1) for `acquire`, `release` and `available`; O(N) once for construction and destruction.
- Space: `N * max(sizeof(T), sizeof(void*))` plus one flag per slot, all inside the pool object.

## Interview follow-ups

- Make `acquire` return a `std::unique_ptr<T, PoolDeleter>` so objects go back to the pool automatically.
- Make it thread-safe. A lock-free free list with a CAS on the head has the ABA problem: what is it, and how do tagged pointers fix it?
- Grow the pool when it is full by chaining extra fixed-size blocks, without moving existing objects (pointers handed out must stay valid).
- Why might FIFO reuse be preferable to LIFO in some situations (e.g. catching use-after-release bugs)?
- How would you place the slots so that two hot objects used by different threads don't share a cache line (false sharing)?
