---
topic: "Templates & Compile Time"
difficulty: Easy
---
# constexpr Math - Solution

## Intuition

Since C++14 a `constexpr` function may contain loops and local variables, so you write ordinary iterative code. The compiler evaluates it when the result is needed as a constant (a template argument, an array bound, a `constexpr` variable) and otherwise compiles it as a normal function.

## Approach

1. `factorial`: multiply `1 * 2 * ... * n` in a loop.
2. `fibonacci`: keep the last two values and step forward `n` times. The textbook double recursion is O(2^n) and would hit the compiler's constexpr step limit long before n = 93.
3. `is_prime`: handle `n < 2`, then try divisors `d` while `d * d <= n`. Skipping even divisors after 2 halves the work. Write `d <= n / d` so `d * d` can't overflow for huge `n`.

## Code

```cpp
#include <cstdint>

constexpr unsigned long long factorial(unsigned n) {
    unsigned long long r = 1;
    for (unsigned i = 2; i <= n; ++i) r *= i;
    return r;
}

constexpr unsigned long long fibonacci(unsigned n) {
    unsigned long long a = 0, b = 1;  // F(i), F(i+1)
    for (unsigned i = 0; i < n; ++i) {
        unsigned long long next = a + b;
        a = b;
        b = next;
    }
    return a;
}

constexpr bool is_prime(unsigned long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (unsigned long long d = 3; d <= n / d; d += 2)
        if (n % d == 0) return false;
    return true;
}
```

## Complexity

- Time: O(n) for `factorial` and `fibonacci`, O(sqrt(n)) for `is_prime`. Zero at run time when the result is used as a constant.
- Space: O(1).

## Interview follow-ups

- What is the difference between `constexpr` and `consteval`? (`consteval` must run at compile time; calling it with a run-time value is a compile error.)
- Build a `constexpr std::array` of the first 100 primes and use it as a lookup table.
- What happens if a `constexpr` evaluation overflows a signed integer? (It's undefined behaviour, so the compiler rejects it in a constant expression: a free UB detector.)
- How would you do this before C++11 with template metaprogramming (`template <int N> struct Factorial`)?
