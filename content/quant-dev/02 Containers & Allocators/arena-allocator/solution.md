---
topic: "Containers & Allocators"
difficulty: Medium
---
# Arena (Bump) Allocator - Solution

## Intuition

The arena's whole state is a buffer and one offset. To allocate, round the offset up to the requested alignment, check that `size` bytes still fit, return `buffer + aligned`, and move the offset to `aligned + size`. `reset` sets the offset back to 0. No bookkeeping per allocation is needed because nothing is ever freed individually.

Rounding up to a power-of-two alignment `a` is the bit trick `(x + a - 1) & ~(a - 1)`. Because the buffer itself starts on a 64-byte boundary, aligning the *offset* aligns the *address* for any alignment up to 64. For larger alignments, round the actual address instead, which works for any base. The code below always rounds the address, so it is correct either way.

## Approach

1. Constructor: `::operator new(bytes, std::align_val_t{64})`; store `base_`, `cap_`, and `off_ = 0`.
2. `allocate(size, a)`:
   - `addr = base + off_`; `aligned = (addr + a - 1) & ~(a - 1)`; `start = aligned - base`.
   - If `start > cap_` or `size > cap_ - start`, return `nullptr` without touching `off_`. Writing it as a subtraction avoids overflow for huge `size`.
   - Otherwise set `off_ = start + size` and return `base_ + start`.
3. `reset`: `off_ = 0`. `used`: `off_`.
4. Destructor: the matching aligned `::operator delete`.

## Code

```cpp
#include <cstddef>
#include <cstdint>
#include <new>

class Arena {
    static constexpr std::size_t kBufferAlign = 64;

public:
    explicit Arena(std::size_t bytes)
        : base_(static_cast<std::byte*>(::operator new(bytes, std::align_val_t{kBufferAlign}))), cap_(bytes) {}

    ~Arena() { ::operator delete(base_, std::align_val_t{kBufferAlign}); }

    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    void* allocate(std::size_t size, std::size_t alignment = alignof(std::max_align_t)) {
        const std::uintptr_t base = reinterpret_cast<std::uintptr_t>(base_);
        const std::uintptr_t aligned = (base + off_ + alignment - 1) & ~(std::uintptr_t(alignment) - 1);
        const std::size_t start = aligned - base;
        if (start > cap_ || size > cap_ - start) return nullptr;
        off_ = start + size;
        return base_ + start;
    }

    void reset() noexcept { off_ = 0; }
    std::size_t used() const noexcept { return off_; }
    std::size_t capacity() const noexcept { return cap_; }

private:
    std::byte* base_;
    std::size_t cap_;
    std::size_t off_ = 0;
};
```

## Complexity

- Time: O(1) for `allocate`, `reset`, `used`.
- Space: exactly `bytes` for the buffer plus three words.

## Interview follow-ups

- Add `template <class T, class... Args> T* create(Args&&...)` using placement new. What happens to objects with non-trivial destructors on `reset()`, and how could the arena run them?
- Plug the arena into standard containers via `std::pmr::monotonic_buffer_resource` or a custom allocator. Why is `deallocate` a no-op?
- When the buffer runs out, chain a new block instead of failing. How does that affect `reset()`?
- Why does an arena improve cache behavior compared to `malloc` for many small objects?
- How would you give each thread its own arena, and why does that remove the need for locking?
