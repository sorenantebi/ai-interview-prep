---
topic: "Containers & Allocators"
difficulty: Medium
---
# Implement a Dynamic Array (Vector)

**Topic:** Containers & Allocators · **Difficulty:** Medium

## Problem

`std::vector` is the default container in latency-sensitive code: contiguous memory, cache-friendly scans, and an amortized O(1) `push_back`. Writing one by hand shows whether you understand the difference between *allocating memory* and *constructing objects*. A vector with capacity 1000 and size 3 holds exactly 3 live objects; the other 997 slots are raw bytes. That is why `Vector<T>` must work for a `T` with no default constructor.

Implement `Vector<T>`:

```cpp
template <class T>
class Vector {
public:
    Vector() noexcept;                          // size 0, capacity 0, no allocation
    Vector(const Vector& other);                // deep copy
    Vector(Vector&& other) noexcept;            // steals the buffer; other becomes empty
    Vector& operator=(const Vector& other);
    Vector& operator=(Vector&& other) noexcept;
    ~Vector();                                  // destroys every element, frees the buffer

    void push_back(const T& value);
    void push_back(T&& value);
    template <class... Args>
    T& emplace_back(Args&&... args);            // constructs in place, returns the new element
    void pop_back();                            // destroys the last element (precondition: not empty)
    void reserve(std::size_t n);                // capacity() >= n afterwards; never shrinks
    void clear() noexcept;                      // destroys all elements, keeps the capacity

    std::size_t size() const noexcept;
    std::size_t capacity() const noexcept;
    bool empty() const noexcept;
    T& operator[](std::size_t i);               // unchecked
    const T& operator[](std::size_t i) const;
    T& at(std::size_t i);                       // throws std::out_of_range if i >= size()
    const T& at(std::size_t i) const;
};
```

## Examples

**Example 1**
```cpp
Vector<int> v;
v.push_back(1);
v.push_back(2);
v.emplace_back(3);
v.size();          // 3
v.capacity() >= 3; // true
v[1];              // 2
v.pop_back();
v.size();          // 2
v.at(5);           // throws std::out_of_range
```

**Example 2**
```cpp
struct Px { explicit Px(double p) : p(p) {} double p; };  // no default constructor
Vector<Px> book;
book.reserve(100);
book.capacity();   // 100 (or more); still only 0 Px objects exist
book.emplace_back(101.5).p;  // 101.5
```

## Constraints

- `push_back` / `emplace_back` are amortized O(1): grow the capacity geometrically (for example ×2), never by a constant.
- Elements are constructed with placement new in raw storage and destroyed explicitly; there are never more live `T` objects than `size()` (the tests count constructions and destructions).
- `v.push_back(v[0])` must work even when it triggers a reallocation.
- Copies are deep; moves don't touch the elements.
