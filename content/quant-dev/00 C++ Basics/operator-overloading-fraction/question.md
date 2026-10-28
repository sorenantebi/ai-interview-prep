---
topic: "C++ Basics"
difficulty: Medium
---
# Fraction Class With Operator Overloading

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) with a `Fraction` class that is always kept **normalised**: numerator and denominator have no common factor and the denominator is positive (so `2/-4` is stored as `-1/2`, and zero as `0/1`).

```cpp
class Fraction {
public:
    Fraction(long long num = 0, long long den = 1);   // normalises
    long long num() const;
    long long den() const;
};
Fraction operator+(const Fraction& a, const Fraction& b);
Fraction operator-(const Fraction& a, const Fraction& b);
Fraction operator*(const Fraction& a, const Fraction& b);
Fraction operator/(const Fraction& a, const Fraction& b);
bool operator==(const Fraction& a, const Fraction& b);
bool operator<(const Fraction& a, const Fraction& b);
std::ostream& operator<<(std::ostream& os, const Fraction& f);  // "p/q", or just "p" when q == 1
```

The program reads `q`, then `q` lines `a/b op c/d` where `op` is one of `+ - * / == <`. For arithmetic operators print the resulting fraction with `<<`; for `==` and `<` print `true` or `false`.

## Examples

**Example 1**
```text
Input:
3
1/2 + 1/3
2/4 == 1/2
3/4 - 3/4
Output:
5/6
true
0
```

**Example 2**
```text
Input:
2
-2/3 * 3/-4
1/3 < 1/4
Output:
1/2
false
```

## Constraints

- `1 <= q <= 1000`; inputs are written `a/b` with `|a|, |b| <= 10^4`, `b != 0` (signs may appear on either part).
- Division never divides by a zero fraction.
- `std::gcd` from `<numeric>` is allowed.
