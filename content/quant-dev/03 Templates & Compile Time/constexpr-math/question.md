---
topic: "Templates & Compile Time"
difficulty: Easy
---
# constexpr Math

**Topic:** Templates & Compile Time · **Difficulty:** Easy

## Problem

Anything you can work out while compiling costs nothing at run time. Trading code uses this for lookup tables, tick-size tables and array sizes that the compiler fills in, so the hot path only does a memory load.

Write three `constexpr` functions that work both at compile time and at run time:

```cpp
constexpr unsigned long long factorial(unsigned n);   // n! ; factorial(0) == 1
constexpr unsigned long long fibonacci(unsigned n);   // F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
constexpr bool is_prime(unsigned long long n);        // 0 and 1 are not prime
```

Because they are `constexpr`, their results can be used wherever the language needs a constant: template arguments, array bounds, `static_assert`.

## Examples

**Example 1**
```cpp
constexpr auto f = factorial(5);     // 120, computed by the compiler
std::array<int, factorial(3)> a{};   // a.size() == 6
fibonacci(10);                        // 55
```

**Example 2**
```cpp
is_prime(97);    // true
is_prime(91);    // false (7 * 13)
is_prime(1);     // false
```

## Constraints

- `0 <= n <= 20` for `factorial` (21! overflows 64 bits).
- `0 <= n <= 93` for `fibonacci` (F(93) is the largest that fits in 64 bits).
- `is_prime` must take O(sqrt(n)) steps, and `fibonacci` O(n) (no exponential recursion: the compiler has a step limit).
