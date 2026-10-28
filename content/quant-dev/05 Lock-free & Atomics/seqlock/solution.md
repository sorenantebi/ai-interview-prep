---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# SeqLock for a Quote - Solution

## Intuition

The sequence counter is a version number whose low bit means "write in progress". A reader that sees the same **even** value before and after its copy knows no write overlapped, so the copy is consistent.

The subtle part is the memory model. Two things must hold:

1. **No data race.** The reader copies while the writer may be writing. If the payload were a plain `T`, that overlap would be undefined behaviour, and the compiler is allowed to assume it never happens. Storing the payload as an array of `std::atomic<std::uint64_t>` words and accessing them with `memory_order_relaxed` makes every concurrent access well defined (and on x86/ARM it compiles to plain loads and stores).
2. **Ordering.** Relaxed accesses can be reordered with the sequence-counter accesses unless fences prevent it:
   - Writer: `seq = odd` must become visible **before** any data word. A release fence after the odd store gives exactly that: any reader that sees one of the new data words also sees the odd counter on its second read.
   - Writer: data words before `seq = even`: a release store.
   - Reader: the first counter read is an acquire load, so the data loads cannot move above it.
   - Reader: the data loads must not move below the second counter read: an acquire fence between them.

This is the construction from Hans Boehm's paper "Can Seqlocks Get Along with Programming Language Memory Models?".

## Approach

1. Payload: `N = ceil(sizeof(T) / 8)` atomic 64-bit words. To write, `memcpy` the `T` into a local `uint64_t[N]` buffer and store each word relaxed; to read, load each word relaxed into a local buffer and `memcpy` it out into a `T`.
2. `write(v)`: `s = seq_.load(relaxed)`; `seq_.store(s + 1, relaxed)`; `atomic_thread_fence(release)`; store the words (relaxed); `seq_.store(s + 2, release)`.
3. `read()`: loop: `s1 = seq_.load(acquire)`; if odd, spin and retry; load the words (relaxed); `atomic_thread_fence(acquire)`; `s2 = seq_.load(relaxed)`; if `s1 == s2`, convert and return.
4. `sequence()`: `seq_.load(acquire)`.

Only one writer exists, so the writer can read `seq_` relaxed and needs no read-modify-write.

## Code

```cpp
#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <type_traits>

template <class T>
class SeqLock {
    static_assert(std::is_trivially_copyable_v<T>, "SeqLock needs a trivially copyable T");
    static constexpr std::size_t N = (sizeof(T) + 7) / 8;

public:
    explicit SeqLock(const T& initial = T{}) { store_words(initial); }

    void write(const T& value) {
        const std::uint64_t s = seq_.load(std::memory_order_relaxed);
        seq_.store(s + 1, std::memory_order_relaxed);         // odd: write in progress
        std::atomic_thread_fence(std::memory_order_release);  // odd counter before any data word
        store_words(value);
        seq_.store(s + 2, std::memory_order_release);         // even: data before the new counter
    }

    T read() const {
        std::uint64_t buf[N];
        for (;;) {
            const std::uint64_t s1 = seq_.load(std::memory_order_acquire);
            if (s1 & 1) continue;  // writer is mid-update
            for (std::size_t i = 0; i < N; ++i) buf[i] = data_[i].load(std::memory_order_relaxed);
            std::atomic_thread_fence(std::memory_order_acquire);  // data loads before the re-check
            if (seq_.load(std::memory_order_relaxed) == s1) break;
        }
        T out;
        std::memcpy(&out, buf, sizeof(T));
        return out;
    }

    std::uint64_t sequence() const { return seq_.load(std::memory_order_acquire); }

private:
    void store_words(const T& value) {
        std::uint64_t buf[N] = {};
        std::memcpy(buf, &value, sizeof(T));
        for (std::size_t i = 0; i < N; ++i) data_[i].store(buf[i], std::memory_order_relaxed);
    }

    alignas(64) std::atomic<std::uint64_t> seq_{0};
    std::atomic<std::uint64_t> data_[N];
};
```

## Complexity

- Time: `write` is O(sizeof(T)) and never waits. `read` is O(sizeof(T)) per attempt; it retries only while a write overlaps, so readers can starve under a writer that never pauses (fine for market data, where readers want the latest value anyway).
- Space: `sizeof(T)` rounded up to 8 bytes, plus the counter.

## Interview follow-ups

- Why is the "obvious" version (plain `T` member, `memcpy` in `read`) undefined behaviour, and what can a compiler actually do with it? (Hoist or tear loads; assume the value cannot change between the two counter reads.)
- Why is a release *store* of the odd counter not enough on its own in `write`? (A release store orders earlier accesses before it, not later ones: the data stores could become visible before the odd counter.)
- Multiple writers: serialise them with a spinlock, or make the odd step a CAS.
- Why put `seq_` and the payload on their own cache line, and what happens to readers when the writer updates at a very high rate?
- Compare with a double buffer / RCU pointer swap and with a reader-writer lock: who pays the cost in each?
- How do Linux's kernel seqlocks (`read_seqbegin` / `read_seqretry`) and the proposed byte-wise atomic `memcpy` (`atomic_load_per_byte_memcpy`, paper P1478) relate to this?
