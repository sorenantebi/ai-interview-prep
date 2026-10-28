---
topic: "Templates & Compile Time"
difficulty: Easy
---
# Variadic Sum, Count and Join

**Topic:** Templates & Compile Time · **Difficulty:** Easy

## Problem

Variadic templates let one function take any number of arguments of any types, with the loop unrolled by the compiler. Logging libraries in trading systems use exactly this: `log("fill", px, qty, side)` is formatted without a format string being parsed at run time.

Implement these with **fold expressions** (C++17), not recursion:

```cpp
template <class... Ts> constexpr auto sum(Ts... args);           // args added left to right; sum() == 0
template <class... Ts> constexpr std::size_t count_args(const Ts&... args);  // number of arguments
template <class... Ts> constexpr bool all_true(Ts... args);      // logical AND of all args; all_true() == true
template <class... Ts> std::string join(std::string_view sep, const Ts&... args);
// Streams each argument with operator<< and puts sep between them; join(sep) == ""
```

## Examples

**Example 1**
```cpp
sum(1, 2, 3);          // 6
sum(1, 2.5);           // 3.5 (a double: the usual arithmetic conversions apply)
sum();                 // 0
count_args('a', "b", 3.0);   // 3
```

**Example 2**
```cpp
all_true(true, 1 < 2, 3);     // true
all_true(true, false);        // false
join(", ", "px", 101.25, 7);  // "px, 101.25, 7"
join("-");                    // ""
```

## Constraints

- `sum`, `count_args` and `all_true` must be usable in constant expressions.
- No recursion and no `std::initializer_list` tricks: one fold expression each (plus whatever `join` needs for the separator).
