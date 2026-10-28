---
topic: "C++ Basics"
difficulty: Easy
---
# Const-Correct Portfolio - Solution

## Intuition

A `const` member function promises not to modify the object: inside it, `this` is a `const Portfolio*`, so `positions_` is a `const std::vector`. Only `const` member functions can be called on a `const` object or through a `const&`, which is why `report(const Portfolio&)` forces `find`, `value` and `size` to be `const`. Because `find` is `const`, it can only hand out a `const Position*`: a pointer through which the caller can read but not modify the position. Taking `const std::string&` / `const Position&` avoids copies while promising not to change the arguments.

## Approach

1. `find`: loop `for (const Position& p : positions_)`, return `&p` on a match.
2. `add`: look the symbol up in the non-const vector; update or `push_back`.
3. `value`: sum `qty * price`.
4. `report` and the final line use `std::fixed << std::setprecision(2)`.

## Code

```cpp
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Position {
    std::string symbol;
    int qty;
    double price;
};

class Portfolio {
public:
    void add(const Position& p) {
        for (Position& existing : positions_) {
            if (existing.symbol == p.symbol) {
                existing.qty += p.qty;
                existing.price = p.price;
                return;
            }
        }
        positions_.push_back(p);
    }

    const Position* find(const std::string& symbol) const {
        for (const Position& p : positions_)
            if (p.symbol == symbol) return &p;
        return nullptr;
    }

    double value() const {
        double total = 0;
        for (const Position& p : positions_) total += p.qty * p.price;
        return total;
    }

    int size() const { return static_cast<int>(positions_.size()); }

private:
    std::vector<Position> positions_;
};

void report(const Portfolio& pf, const std::string& symbol) {
    const Position* p = pf.find(symbol);
    if (!p) std::cout << symbol << " not found\n";
    else std::cout << symbol << ' ' << p->qty << " @ " << p->price << " = " << p->qty * p->price << '\n';
}

int main() {
    std::cout << std::fixed << std::setprecision(2);
    int n;
    std::cin >> n;
    Portfolio pf;
    for (int i = 0; i < n; ++i) {
        Position p;
        std::cin >> p.symbol >> p.qty >> p.price;
        pf.add(p);
    }
    int q;
    std::cin >> q;
    for (int i = 0; i < q; ++i) {
        std::string symbol;
        std::cin >> symbol;
        report(pf, symbol);
    }
    std::cout << "positions " << pf.size() << " value " << pf.value() << '\n';
    return 0;
}
```

## Complexity

- Time: O(n) per `add` / `find` (linear scan), so O(n^2 + q*n) overall; a hash map would make each O(1) on average.
- Space: O(n)

## Interview follow-ups

- Read these right to left: `const int* p`, `int const* p`, `int* const p`, `const int* const p`. Which can be reseated, which can modify the int?
- Can you overload a member function on `const`? (Yes: `Position* find(...)` and `const Position* find(...) const`, which is how `std::vector::operator[]` works.)
- What does `mutable` do, and when is it legitimate? (Caches, mutexes inside a logically-const object.)
- Is `const_cast`-ing away const and writing to the object ever OK? (Only if the object itself wasn't declared `const`; otherwise UB.)
- The pointer returned by `find` points into the vector. When does it dangle? (After any `push_back` that reallocates.)
