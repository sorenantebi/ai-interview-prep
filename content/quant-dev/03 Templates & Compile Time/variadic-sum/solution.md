---
topic: "Templates & Compile Time"
difficulty: Easy
---
# Variadic Sum, Count and Join - Solution

## Intuition

A fold expression applies a binary operator across a whole parameter pack: `(args + ...)` expands to `a1 + (a2 + (a3 ...))`. A **binary** fold with an initial value, `(args + ... + 0)`, also handles the empty pack. `sizeof...(Ts)` gives the pack size at compile time. For `join`, a fold over the comma operator runs a small lambda once per argument, in order.

## Approach

1. `sum`: `(0 + ... + args)`, a left fold seeded with `0` so `sum()` is `0` and the type follows normal promotion (`0 + 1 + 2.5` is a `double`).
2. `count_args`: return `sizeof...(Ts)`; nothing is evaluated.
3. `all_true`: `(true && ... && static_cast<bool>(args))`, seeded with `true` for the empty pack.
4. `join`: stream into a `std::ostringstream`; a flag tracks whether a separator is needed, and `(emit(args), ...)` calls `emit` on each argument left to right (the comma operator guarantees order).

## Code

```cpp
#include <cstddef>
#include <sstream>
#include <string>
#include <string_view>

template <class... Ts>
constexpr auto sum(Ts... args) {
    return (0 + ... + args);
}

template <class... Ts>
constexpr std::size_t count_args(const Ts&...) {
    return sizeof...(Ts);
}

template <class... Ts>
constexpr bool all_true(Ts... args) {
    return (true && ... && static_cast<bool>(args));
}

template <class... Ts>
std::string join(std::string_view sep, const Ts&... args) {
    std::ostringstream out;
    bool first = true;
    auto emit = [&](const auto& a) {
        if (!first) out << sep;
        first = false;
        out << a;
    };
    (emit(args), ...);
    return out.str();
}
```

## Complexity

- Time: O(number of arguments), unrolled at compile time; `join` is also linear in the output length.
- Space: O(1) besides the output string.

## Interview follow-ups

- What's the difference between `(args + ...)` and `(... + args)`? (Right vs left fold: matters for non-associative operators like `-` or for floating-point rounding.)
- Why does a unary fold over `+` fail on an empty pack while `&&`, `||` and `,` don't?
- Write the pre-C++17 recursive version (`sum(T first, Rest... rest)`) and compare the number of instantiations.
- How would a low-latency logger avoid `ostringstream` entirely? (Copy the raw arguments into a ring buffer and format them on a background thread.)
