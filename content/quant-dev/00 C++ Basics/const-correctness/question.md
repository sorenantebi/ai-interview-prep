---
topic: "C++ Basics"
difficulty: Easy
---
# Const-Correct Portfolio

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`) with a `Portfolio` class whose read-only member functions are marked `const`, and reporting functions that only ever see the portfolio through a **`const` reference**:

```cpp
struct Position {
    std::string symbol;
    int qty;
    double price;
};

class Portfolio {
public:
    void add(const Position& p);                            // if the symbol exists: add qty and set price to p.price
    const Position* find(const std::string& symbol) const;  // nullptr if absent
    double value() const;                                   // sum of qty * price
    int size() const;                                       // number of distinct symbols
private:
    std::vector<Position> positions_;                       // kept in insertion order
};

void report(const Portfolio& pf, const std::string& symbol);  // prints one query line
```

The program reads `n` positions (`symbol qty price`, one per line) and adds them, then reads `q` symbols and calls `report` for each. `report` prints `<symbol> <qty> @ <price> = <qty*price>` or `<symbol> not found`. Finally print `positions <size> value <value>`. All money values have exactly 2 decimals.

## Examples

**Example 1**
```text
Input:
3
AAPL 10 150.5
MSFT 5 300
AAPL 5 151
2
AAPL
TSLA
Output:
AAPL 15 @ 151.00 = 2265.00
TSLA not found
positions 2 value 3765.00
```

**Example 2**
```text
Input:
1
X 1 0.25
1
X
Output:
X 1 @ 0.25 = 0.25
positions 1 value 0.25
```

## Constraints

- `1 <= n, q <= 1000`; symbols are 1 to 8 upper-case letters; `1 <= qty <= 10^6`; `0 < price <= 10^5`.
- `report` and `find` must compile with a `const Portfolio&` (that's the exercise: `const` member functions, and a pointer-to-const return).
