---
topic: "Containers & Allocators"
difficulty: Hard
---
# Open-Addressing Hash Map with Linear Probing - Solution

## Intuition

Store the entries in one array of slots, each marked `Empty`, `Full` or `Deleted` (tombstone). A key's home slot is `hash(key) & (capacity - 1)` (capacity is a power of two). To look it up, walk forward from home until you find the key or hit an `Empty` slot. An empty slot ends the search because an insert would have used it. A tombstone does *not* end the search, because the key may have been placed further along before something earlier in its chain was erased.

Two details make it robust:

- **Hash mixing.** With an identity hash, keys like `k * 2^20` all share their low bits, so they land in the same slot and the table degrades to a linear scan. A cheap 64-bit finalizer (the one from SplitMix64) spreads every input bit across the output.
- **Counting tombstones toward the load.** A probe stops only at `Empty`. If tombstones were not counted, endless insert/erase churn could fill the table with them, and a failed lookup would never terminate. So trigger a rehash when `(size + tombstones + 1) > 0.7 * capacity`. When the *live* load is low, rehash at the same capacity, which simply clears the tombstones; otherwise double.

## Approach

1. `struct Slot { int64_t key; V value; State state; }`, `std::vector<Slot> slots_` (start with 16), `size_`, `tombs_`.
2. `find_index(key)`: probe from home; skip `Deleted`, return the index on a `Full` match, stop at `Empty`.
3. `insert`: if the key exists, overwrite the value and return `false`. Otherwise grow or clean up if the load would exceed 0.7. Then probe from home, remember the first tombstone seen, stop at the first `Empty`, and put the entry in the tombstone if there was one (`--tombs_`), else in the empty slot.
4. `erase`: find, mark `Deleted`, reset the value, `--size_`, `++tombs_`.
5. `rehash(n)`: allocate `n` empty slots and reinsert every `Full` entry (no tombstones survive).

## Code

```cpp
#include <cstddef>
#include <cstdint>
#include <utility>
#include <vector>

template <class V>
class HashMap {
    enum class State : unsigned char { Empty, Full, Deleted };
    struct Slot {
        std::int64_t key = 0;
        V value{};
        State state = State::Empty;
    };
    static constexpr std::size_t npos = static_cast<std::size_t>(-1);

public:
    HashMap() : slots_(16) {}

    bool insert(std::int64_t key, const V& value) {
        if (std::size_t i = find_index(key); i != npos) {
            slots_[i].value = value;
            return false;
        }
        if ((size_ + tombs_ + 1) * 10 > slots_.size() * 7) {
            // Many live keys: grow. Mostly tombstones: rebuild at the same size to clear them.
            rehash((size_ + 1) * 10 > slots_.size() * 5 ? slots_.size() * 2 : slots_.size());
        }
        const std::size_t mask = slots_.size() - 1;
        std::size_t i = home(key), target = npos;
        while (slots_[i].state != State::Empty) {
            if (slots_[i].state == State::Deleted && target == npos) target = i;
            i = (i + 1) & mask;
        }
        if (target == npos) target = i;
        else --tombs_;
        slots_[target] = Slot{key, value, State::Full};
        ++size_;
        return true;
    }

    V* find(std::int64_t key) {
        std::size_t i = find_index(key);
        return i == npos ? nullptr : &slots_[i].value;
    }
    const V* find(std::int64_t key) const {
        std::size_t i = find_index(key);
        return i == npos ? nullptr : &slots_[i].value;
    }

    bool erase(std::int64_t key) {
        std::size_t i = find_index(key);
        if (i == npos) return false;
        slots_[i].state = State::Deleted;
        slots_[i].value = V{};
        --size_;
        ++tombs_;
        return true;
    }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return slots_.size(); }

private:
    static std::uint64_t mix(std::uint64_t x) {  // SplitMix64 finalizer
        x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27; x *= 0x94d049bb133111ebULL;
        x ^= x >> 31;
        return x;
    }
    std::size_t home(std::int64_t key) const {
        return static_cast<std::size_t>(mix(static_cast<std::uint64_t>(key))) & (slots_.size() - 1);
    }

    std::size_t find_index(std::int64_t key) const {
        const std::size_t mask = slots_.size() - 1;
        for (std::size_t i = home(key);; i = (i + 1) & mask) {
            const Slot& s = slots_[i];
            if (s.state == State::Empty) return npos;
            if (s.state == State::Full && s.key == key) return i;
        }
    }

    void rehash(std::size_t new_cap) {
        std::vector<Slot> old(new_cap);
        old.swap(slots_);
        size_ = tombs_ = 0;
        const std::size_t mask = new_cap - 1;
        for (Slot& s : old) {
            if (s.state != State::Full) continue;
            std::size_t i = home(s.key);
            while (slots_[i].state != State::Empty) i = (i + 1) & mask;
            slots_[i] = std::move(s);
            ++size_;
        }
    }

    std::vector<Slot> slots_;
    std::size_t size_ = 0, tombs_ = 0;
};
```

## Complexity

- Time: expected O(1) for `insert`, `find`, `erase` (load ≤ 0.7 keeps expected probe lengths short); a rehash is O(capacity) but happens rarely enough to be amortized O(1).
- Space: O(capacity) = O(size), one flat array.

## Interview follow-ups

- **Backward-shift deletion**: instead of tombstones, move later entries of the cluster back one slot when erasing. When is that valid, and why does it remove the need to clear tombstones?
- **Robin Hood hashing**: on insert, take a slot from an entry that is closer to its home. What does it do to the variance of probe lengths?
- Struct-of-arrays layout (separate key and metadata arrays, as in Abseil's Swiss tables): why does it make probing faster with SIMD?
- Pre-size the table for a known number of instruments so no rehash ever happens during trading hours.
- Why do power-of-two capacities need a good hash, while prime capacities tolerate a weak one?
