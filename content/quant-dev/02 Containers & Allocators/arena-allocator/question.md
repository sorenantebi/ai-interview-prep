---
topic: "Containers & Allocators"
difficulty: Medium
---
# Arena (Bump) Allocator

**Topic:** Containers & Allocators · **Difficulty:** Medium

## Problem

Processing one market data packet may create dozens of short-lived objects (parsed messages, temporary book deltas), all of which die together when the packet is done. An arena makes that pattern almost free: grab one big block up front, hand out memory by bumping an offset forward, and "free" everything at once by resetting the offset to zero. There is no per-object free and no fragmentation, and consecutive allocations are adjacent in memory.

Implement `Arena`:

```cpp
class Arena {
public:
    explicit Arena(std::size_t bytes);      // allocates one buffer of `bytes`, aligned to 64
    ~Arena();
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    // Returns a pointer to `size` bytes aligned to `alignment` (a power of two, at most 4096),
    // or nullptr if they don't fit in the remaining space.
    void* allocate(std::size_t size, std::size_t alignment = alignof(std::max_align_t));
    void reset() noexcept;                  // forget every allocation; the whole buffer is free again
    std::size_t used() const noexcept;      // bytes consumed so far, including alignment padding
    std::size_t capacity() const noexcept;  // the size passed to the constructor
};
```

`used()` is the end offset of the last successful allocation: allocating `size` bytes first rounds the current offset up to the alignment, then adds `size`.

## Examples

**Example 1**
```cpp
Arena a(256);
void* p = a.allocate(10, 1);   // offset 0..10
a.used();                      // 10
void* q = a.allocate(8, 8);    // offset rounded up to 16, then 16..24
a.used();                      // 24
(char*)q - (char*)p;           // 16
a.allocate(1000);              // nullptr: doesn't fit
a.used();                      // still 24
a.reset();
a.allocate(10, 1) == p;        // true: memory is reused from the start
```

**Example 2**
```cpp
Arena a(1024);
a.allocate(3, 1);
void* line = a.allocate(64, 64);  // cache-line aligned
(uintptr_t)line % 64;             // 0
a.used();                         // 128
```

## Constraints

- `allocate` and `reset` are O(1). Only the constructor allocates memory.
- A failed allocation leaves `used()` unchanged.
- Returned blocks never overlap and always lie inside the buffer.
- `0 <= bytes <= 10^8`, `size >= 1`.
