---
topic: "Templates & Compile Time"
difficulty: Hard
---
# Optional from Scratch

**Topic:** Templates & Compile Time · **Difficulty:** Hard

## Problem

"Maybe a value" types are everywhere in trading code: the best bid of an empty book, the last fill price, a parsed field that may be missing. `std::optional<T>` stores the `T` **inline**, with no heap allocation, by reserving correctly aligned raw bytes and constructing the object there only when needed. Writing one yourself tests object lifetime rules: placement new, explicit destructor calls and getting every constructor and destructor call exactly right.

Implement `Optional<T>`:

```cpp
template <class T>
class Optional {
public:
    Optional() noexcept;                     // empty
    Optional(const T& value);                // engaged, copy of value
    Optional(T&& value);                     // engaged, moved from value
    Optional(const Optional& other);
    Optional(Optional&& other) noexcept(std::is_nothrow_move_constructible_v<T>);
    Optional& operator=(const Optional& other);
    Optional& operator=(Optional&& other) noexcept(...);
    ~Optional();

    bool has_value() const noexcept;
    explicit operator bool() const noexcept;
    T& value();                              // throws std::bad_optional_access if empty
    const T& value() const;
    T& operator*();                          // no check (precondition: has_value())
    const T& operator*() const;
    T* operator->();
    const T* operator->() const;

    template <class... Args>
    T& emplace(Args&&... args);              // destroy any current value, construct a new one in place
    void reset() noexcept;                   // destroy the value if there is one
};
```

Rules:
- Storage is an `alignas(T)` byte array inside the object. No heap allocation, no `std::optional`, `std::variant` or `std::any`.
- Every `T` that is constructed is destroyed exactly once. A test type counts constructor and destructor calls.
- Copy / move from an engaged `Optional` constructs a `T`; from an empty one gives an empty result. After a move the source stays engaged, holding a moved-from `T` (as `std::optional` does).
- Assignment: both engaged → assign the `T`; only the source engaged → construct; only the target engaged → destroy; self-assignment is a no-op.

## Examples

**Example 1**
```cpp
Optional<int> a;
a.has_value();          // false
a = Optional<int>(42);
*a;                     // 42
a.reset();
a.value();              // throws std::bad_optional_access
```

**Example 2**
```cpp
Optional<std::string> s(std::string("bid"));
s.emplace(3, 'x');      // destroys "bid", builds "xxx" in place
s->size();              // 3
Optional<std::string> t = s;
*t;                     // "xxx"
```

## Constraints

- `T` need not be default constructible or copy assignable for the operations you don't use.
- `sizeof(Optional<T>) <= sizeof(T) + alignof(T)`.
