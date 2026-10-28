---
topic: "Templates & Compile Time"
difficulty: Medium
---
# Hand-Rolled Type Traits

**Topic:** Templates & Compile Time · **Difficulty:** Medium

## Problem

Generic trading code (serialisers, message codecs, containers) picks different code paths depending on the type it gets: copy PODs with `memcpy`, strip `const` before storing, handle pointers differently. `<type_traits>` does this with partial template specialisation, and interviewers like to ask you to rebuild a few traits from scratch.

Implement these without using `<type_traits>` in your solution:

```cpp
template <class T, class U> struct IsSame;            // static constexpr bool value
template <class T> struct RemoveConst;                // using type = T without top-level const
template <class T> struct RemoveReference;            // using type = T without & or &&
template <class T> struct IsPointer;                  // static constexpr bool value (true for cv-qualified pointers too)
template <bool B, class T, class F> struct Conditional;  // using type = B ? T : F

// Shorthand aliases
template <class T, class U> inline constexpr bool IsSame_v = IsSame<T, U>::value;
template <class T> using RemoveConst_t = typename RemoveConst<T>::type;
template <class T> using RemoveReference_t = typename RemoveReference<T>::type;
template <class T> inline constexpr bool IsPointer_v = IsPointer<T>::value;
template <bool B, class T, class F> using Conditional_t = typename Conditional<B, T, F>::type;
```

`RemoveConst` only removes **top-level** `const`: `const int*` is a (non-const) pointer to const int and stays unchanged, while `int* const` becomes `int*`.

## Examples

**Example 1**
```cpp
IsSame_v<int, int>;                 // true
IsSame_v<int, const int>;           // false
RemoveConst_t<const double>;        // double
RemoveReference_t<std::string&&>;   // std::string
```

**Example 2**
```cpp
IsPointer_v<int*>;                  // true
IsPointer_v<int>;                   // false
Conditional_t<true, int, double>;   // int
Conditional_t<false, int, double>;  // double
```

## Constraints

- Everything is resolved at compile time; no run-time code.
- `IsPointer` is true for `T*`, `T* const`, `T* volatile` and `T* const volatile`, and false for references to pointers.
