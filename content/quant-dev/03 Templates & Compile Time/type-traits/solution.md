---
topic: "Templates & Compile Time"
difficulty: Medium
---
# Hand-Rolled Type Traits - Solution

## Intuition

A trait is a class template whose **primary template** gives the default answer, plus **partial specialisations** that match the special shapes. The compiler picks the most specialised match, so pattern matching on types does all the work.

## Approach

1. `IsSame`: primary says `false`; the specialisation `IsSame<T, T>` (both arguments the same) says `true`.
2. `RemoveConst`: primary keeps `T`; `RemoveConst<const T>` matches a top-level `const` and yields `T`. `const int*` doesn't match `const T` (the pointer itself isn't const), so it is left alone.
3. `RemoveReference`: specialise for `T&` and `T&&`.
4. `IsPointer`: specialise for `T*` and its three cv-qualified forms. A reference to a pointer (`int*&`) matches none, so it stays false.
5. `Conditional`: primary for `B = true` returns `T`; specialise `Conditional<false, T, F>` to return `F`.

## Code

```cpp
template <class T, class U>
struct IsSame { static constexpr bool value = false; };
template <class T>
struct IsSame<T, T> { static constexpr bool value = true; };

template <class T> struct RemoveConst { using type = T; };
template <class T> struct RemoveConst<const T> { using type = T; };

template <class T> struct RemoveReference { using type = T; };
template <class T> struct RemoveReference<T&> { using type = T; };
template <class T> struct RemoveReference<T&&> { using type = T; };

template <class T> struct IsPointer { static constexpr bool value = false; };
template <class T> struct IsPointer<T*> { static constexpr bool value = true; };
template <class T> struct IsPointer<T* const> { static constexpr bool value = true; };
template <class T> struct IsPointer<T* volatile> { static constexpr bool value = true; };
template <class T> struct IsPointer<T* const volatile> { static constexpr bool value = true; };

template <bool B, class T, class F> struct Conditional { using type = T; };
template <class T, class F> struct Conditional<false, T, F> { using type = F; };

template <class T, class U> inline constexpr bool IsSame_v = IsSame<T, U>::value;
template <class T> using RemoveConst_t = typename RemoveConst<T>::type;
template <class T> using RemoveReference_t = typename RemoveReference<T>::type;
template <class T> inline constexpr bool IsPointer_v = IsPointer<T>::value;
template <bool B, class T, class F> using Conditional_t = typename Conditional<B, T, F>::type;
```

## Complexity

- Time: zero at run time; a handful of template instantiations at compile time.
- Space: none.

## Interview follow-ups

- The standard library derives these from `std::integral_constant<bool, V>` (`true_type` / `false_type`). Why is that handy? (Tag dispatch: overload on `std::true_type` vs `std::false_type`.)
- Implement `Decay<T>` (remove reference, then cv, then turn arrays and functions into pointers).
- Implement `IsConvertible<From, To>` or a "has member `.size()`" detector with SFINAE, then with a C++20 `requires` expression.
- Why does `RemoveConst_t<const int&>` stay `const int&`? (The `const` isn't top level: the reference itself isn't const.)
