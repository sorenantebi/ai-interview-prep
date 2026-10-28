---
topic: "Containers & Allocators"
difficulty: Medium
---
# Fixed-Capacity Object Pool

**Topic:** Containers & Allocators · **Difficulty:** Medium

## Problem

An order gateway creates and destroys thousands of `Order` objects per second. Calling `new` / `delete` for each one costs a trip through the general-purpose allocator (locks, size classes, possible system calls) and scatters the objects across the heap. An object pool reserves room for `N` objects up front and recycles slots through a free list, so getting and returning an object is a couple of pointer moves with no allocation.

Implement `ObjectPool<T, N>`:

```cpp
template <class T, std::size_t N>
class ObjectPool {
public:
    ObjectPool();                                // all N slots free; no T is constructed yet
    ~ObjectPool();                               // destroys any objects still acquired
    ObjectPool(const ObjectPool&) = delete;
    ObjectPool& operator=(const ObjectPool&) = delete;

    template <class... Args>
    T* acquire(Args&&... args);                  // constructs a T in a free slot; nullptr if none is free
    void release(T* p);                          // destroys *p and returns its slot (p came from acquire)
    std::size_t available() const noexcept;      // number of free slots
    static constexpr std::size_t capacity() noexcept { return N; }
};
```

The free list is LIFO: `acquire` reuses the most recently released slot first (it is the one most likely to still be in cache).

## Examples

**Example 1**
```cpp
ObjectPool<Order, 2> pool;
Order* a = pool.acquire(1, 100.25);  // Order{id 1, price 100.25}
Order* b = pool.acquire(2, 100.50);
pool.acquire(3, 99.0);               // nullptr: pool exhausted
pool.available();                    // 0
pool.release(a);                     // ~Order runs for a
Order* c = pool.acquire(4, 101.0);
c == a;                              // true: the freed slot is reused
```

## Constraints

- `acquire` and `release` are O(1) and never allocate; all storage lives inside the pool.
- `T` need not be default-constructible. Exactly one constructor runs per successful `acquire` and one destructor per `release` (the tests count them).
- If `T`'s constructor throws, the exception propagates and the slot stays free.
- `1 <= N <= 10^6`.
