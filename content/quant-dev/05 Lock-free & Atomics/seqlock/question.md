---
topic: "Lock-free & Atomics"
difficulty: Hard
---
# SeqLock for a Quote

**Topic:** Lock-free & Atomics · **Difficulty:** Hard

## Problem

A market-data thread updates the top-of-book `Quote{bid, ask}` for an instrument millions of times a second, and several strategy threads read it. A mutex or a reader-writer lock would make every reader *write* shared memory (the lock word), so readers would slow down each other and the writer. A **sequence lock** lets the writer never wait and readers never write:

- The writer bumps a sequence counter to an **odd** number, writes the data, then bumps it to the next **even** number.
- A reader reads the counter, copies the data, reads the counter again. If the counter was odd, or changed, a write overlapped the copy and the reader retries.

Readers may therefore copy a half-written value, but they always detect it and throw that copy away: they never *return* a torn quote.

Implement it for any trivially copyable `T`:

```cpp
template <class T>   // T is trivially copyable and default-constructible
class SeqLock {
public:
    explicit SeqLock(const T& initial = T{});
    void write(const T& value);       // called by ONE writer thread only
    T read() const;                   // any number of reader threads; retries until consistent
    std::uint64_t sequence() const;   // even when no write is in progress; +2 per completed write
};
```

**The catch.** Copying `T` with plain loads while another thread writes it is a data race, which is undefined behaviour in C++ even if you discard the result. Make the implementation race-free under the C++ memory model: keep the payload in `std::atomic` words (for example `std::atomic<std::uint64_t>` chunks, accessed with `memory_order_relaxed`) and get the ordering right with acquire/release operations or `std::atomic_thread_fence`.

## Examples

**Example 1**
```cpp
struct Quote { double bid, ask; };
SeqLock<Quote> q(Quote{100.25, 100.50});
q.sequence();     // 0
q.read();         // {100.25, 100.50}
q.write({100.50, 100.75});
q.read();         // {100.50, 100.75}
q.sequence();     // 2
```

**Example 2**
```cpp
SeqLock<Quote> q(Quote{0, 0});
// writer thread: for x in 1..N: q.write({x, x});
// reader threads: every Quote r = q.read(); has r.bid == r.ask, and never goes backwards
```

## Constraints

- `T` is trivially copyable, default-constructible, and at most 256 bytes.
- Exactly one writer thread; any number of readers.
- `write` never blocks. `read` never writes shared memory.
- No mutex. No data races: every shared variable is a `std::atomic`.
