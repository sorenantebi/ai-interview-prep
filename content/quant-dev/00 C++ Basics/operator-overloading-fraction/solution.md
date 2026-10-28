---
topic: "C++ Basics"
difficulty: Medium
---
# Fraction Class With Operator Overloading - Solution

## Intuition

If every constructor normalises, every `Fraction` has exactly one representation, so `==` is just "same numerator and same denominator" and printing is trivial. The arithmetic operators are the school formulas, each returning a new `Fraction` built through that normalising constructor. With positive denominators, `a/b < c/d` is `a*d < c*b` (no floating point).

## Approach

1. Constructor: if `den < 0` negate both; divide both by `gcd(|num|, den)` (`std::gcd(0, d) == d`, so zero becomes `0/1`).
2. Operators as **non-member** functions taking `const Fraction&`, so both sides get the same implicit conversions (e.g. `Fraction + 1` and `1 + Fraction` both work).
3. `operator<<` returns the stream so calls can be chained.
4. Parsing: `long long a, b; char slash; std::cin >> a >> slash >> b;` reads `-3/4`; read the operator as a `std::string`.

## Code

```cpp
#include <iostream>
#include <numeric>
#include <string>

class Fraction {
public:
    Fraction(long long num = 0, long long den = 1) : num_(num), den_(den) {
        if (den_ < 0) num_ = -num_, den_ = -den_;
        long long g = std::gcd(num_, den_);
        num_ /= g;
        den_ /= g;
    }
    long long num() const { return num_; }
    long long den() const { return den_; }

private:
    long long num_, den_;
};

Fraction operator+(const Fraction& a, const Fraction& b) { return {a.num() * b.den() + b.num() * a.den(), a.den() * b.den()}; }
Fraction operator-(const Fraction& a, const Fraction& b) { return {a.num() * b.den() - b.num() * a.den(), a.den() * b.den()}; }
Fraction operator*(const Fraction& a, const Fraction& b) { return {a.num() * b.num(), a.den() * b.den()}; }
Fraction operator/(const Fraction& a, const Fraction& b) { return {a.num() * b.den(), a.den() * b.num()}; }
bool operator==(const Fraction& a, const Fraction& b) { return a.num() == b.num() && a.den() == b.den(); }
bool operator<(const Fraction& a, const Fraction& b) { return a.num() * b.den() < b.num() * a.den(); }

std::ostream& operator<<(std::ostream& os, const Fraction& f) {
    os << f.num();
    if (f.den() != 1) os << '/' << f.den();
    return os;
}

Fraction readFraction() {
    long long n, d;
    char slash;
    std::cin >> n >> slash >> d;
    return Fraction(n, d);
}

int main() {
    int q;
    std::cin >> q;
    std::cout << std::boolalpha;
    while (q--) {
        Fraction a = readFraction();
        std::string op;
        std::cin >> op;
        Fraction b = readFraction();
        if (op == "+") std::cout << a + b << '\n';
        else if (op == "-") std::cout << a - b << '\n';
        else if (op == "*") std::cout << a * b << '\n';
        else if (op == "/") std::cout << a / b << '\n';
        else if (op == "==") std::cout << (a == b) << '\n';
        else std::cout << (a < b) << '\n';
    }
    return 0;
}
```

## Complexity

- Time: O(log(max value)) per operation (the gcd).
- Space: O(1)

## Interview follow-ups

- Why make `operator+` a free function instead of a member? Why must `operator<<` be a free function (or friend)?
- Implement `+=` as a member and `+` in terms of it. Which one should return a reference, and which by value?
- What do you get from C++20's `operator<=>` and defaulted `==`? Would a defaulted `==` be correct here? (Only because we normalise.)
- The non-`explicit` constructor allows `Fraction f = 3;`. When is such an implicit conversion helpful and when dangerous?
- How would you avoid overflow in `a.num() * b.den()`? (Reduce by gcds before multiplying, or use `__int128`.) Why do trading systems store prices as scaled integers (ticks) rather than `double` or fractions?
