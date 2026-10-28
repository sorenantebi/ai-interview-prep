---
topic: "Containers & Allocators"
difficulty: Hard
---
# Open-Addressing Hash Map with Linear Probing

**Topic:** Containers & Allocators · **Difficulty:** Hard

## Problem

Order books and position caches look things up by integer id (order id, instrument id) millions of times per second. `std::unordered_map` stores every entry in its own heap node, so each lookup chases a pointer to a random cache line. An open-addressing table keeps all entries in one flat array: on a collision it simply tries the next slot (linear probing), so a lookup usually touches one or two adjacent cache lines.

The difficult part is deletion. You can't just empty a slot, because that would break the probe chain for keys stored after it. Mark it as a **tombstone** instead: lookups skip over it, inserts may reuse it.

Implement `HashMap<V>` with `std::int64_t` keys:

```cpp
template <class V>
class HashMap {
public:
    HashMap();                                      // empty; capacity() is a power of two (e.g. 16)
    bool insert(std::int64_t key, const V& value);  // true if the key was new; otherwise overwrite, return false
    V* find(std::int64_t key);                      // pointer to the value, nullptr if absent
    const V* find(std::int64_t key) const;
    bool erase(std::int64_t key);                   // true if the key was present
    std::size_t size() const noexcept;              // number of keys stored
    std::size_t capacity() const noexcept;          // number of slots
};
```

## Examples

**Example 1**
```cpp
HashMap<double> px;
px.insert(1001, 99.5);     // true
px.insert(1002, 100.0);    // true
px.insert(1001, 99.75);    // false: overwritten
*px.find(1001);            // 99.75
px.find(7);                // nullptr
px.erase(1001);            // true
px.erase(1001);            // false
px.size();                 // 1
```

**Example 2**
```cpp
HashMap<int> m;
for (int i = 0; i < 1000; ++i) m.insert(i, i * i);
m.size();                          // 1000
m.size() <= 0.7 * m.capacity();    // true: the table grew automatically
*m.find(999);                      // 998001
```

## Constraints

- Linear probing in a single array; resize (rehash) automatically so that the load factor stays at most 0.7.
- Every `int64_t` value is a valid key, including 0, negative numbers, `INT64_MIN` and `INT64_MAX` (don't reserve a key as an "empty" marker).
- Keys can follow patterns, such as all multiples of 2^20. Operations must stay expected O(1), so mix the key bits before masking.
- Tombstones must not accumulate forever: with a bounded number of live keys, any number of insert/erase cycles must keep `capacity()` bounded and `find` fast.
- `V` is default-constructible and copyable.
