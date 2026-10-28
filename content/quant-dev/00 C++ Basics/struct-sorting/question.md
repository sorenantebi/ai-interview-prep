---
topic: "C++ Basics"
difficulty: Easy
---
# Sorting Trades With Custom Comparators

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`) that sorts a blotter of trades:

```cpp
struct Trade {
    std::string symbol;
    double price;
    int qty;
    double notional() const;   // price * qty
};

bool bySymbol(const Trade& a, const Trade& b);     // symbol ascending, then price descending, then qty ascending
bool byNotional(const Trade& a, const Trade& b);   // notional descending, then symbol ascending
```

The first line is the sort mode, `symbol` or `notional`. Then comes `n` and `n` lines `symbol price qty`. Read them into a `std::vector<Trade>`, sort with `std::sort` and the matching comparator **function** (pass the function name as the comparator), and print each trade as

```text
<symbol> <price> <qty> <notional>
```

with price and notional to 2 decimals, followed by a final line `total <sum of notionals>`.

## Examples

**Example 1**
```text
Input:
symbol
4
MSFT 300 10
AAPL 150.5 20
AAPL 151 5
MSFT 300 2
Output:
AAPL 151.00 5 755.00
AAPL 150.50 20 3010.00
MSFT 300.00 2 600.00
MSFT 300.00 10 3000.00
total 7365.00
```

**Example 2**
```text
Input:
notional
3
A 10 10
B 50 1
C 1 100
Output:
A 10.00 10 100.00
C 1.00 100 100.00
B 50.00 1 50.00
total 250.00
```

## Constraints

- `1 <= n <= 10^4`; symbols are 1 to 8 upper-case letters; `0 < price <= 10^5` with at most 2 decimals; `1 <= qty <= 10^4`.
- No two trades are equal under the chosen comparator, so the order is unique.
- A comparator must be a strict weak ordering: return `false` for equal elements.
