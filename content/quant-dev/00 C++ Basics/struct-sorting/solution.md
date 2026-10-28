---
topic: "C++ Basics"
difficulty: Easy
---
# Sorting Trades With Custom Comparators - Solution

## Intuition

`std::sort` only needs a "less than" predicate. For multi-key ordering compare the first key; only if it's equal fall through to the next one. Descending order on a key is just `a.key > b.key`. `std::tie` builds tuples that compare lexicographically, which makes the chain a one-liner, and negating a numeric key (`-a.price`) flips its direction. The comparator must be a strict weak ordering, so it must return `false` for equal elements (never use `<=`).

## Approach

1. `bySymbol`: `std::tie(a.symbol, b.price, a.qty) < std::tie(b.symbol, a.price, b.qty)`: putting `b.price` on the left side makes price descend.
2. `byNotional`: if notionals differ return `a.notional() > b.notional()`, else `a.symbol < b.symbol`.
3. `std::sort(v.begin(), v.end(), mode == "symbol" ? bySymbol : byNotional);`: both functions have the same type, so the conditional yields a function pointer.
4. Print with `std::fixed << std::setprecision(2)`.

## Code

```cpp
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <tuple>
#include <vector>

struct Trade {
    std::string symbol;
    double price;
    int qty;
    double notional() const { return price * qty; }
};

bool bySymbol(const Trade& a, const Trade& b) {
    return std::tie(a.symbol, b.price, a.qty) < std::tie(b.symbol, a.price, b.qty);
}

bool byNotional(const Trade& a, const Trade& b) {
    if (a.notional() != b.notional()) return a.notional() > b.notional();
    return a.symbol < b.symbol;
}

int main() {
    std::string mode;
    int n;
    std::cin >> mode >> n;
    std::vector<Trade> trades(n);
    for (Trade& t : trades) std::cin >> t.symbol >> t.price >> t.qty;

    std::sort(trades.begin(), trades.end(), mode == "symbol" ? bySymbol : byNotional);

    std::cout << std::fixed << std::setprecision(2);
    double total = 0;
    for (const Trade& t : trades) {
        std::cout << t.symbol << ' ' << t.price << ' ' << t.qty << ' ' << t.notional() << '\n';
        total += t.notional();
    }
    std::cout << "total " << total << '\n';
    return 0;
}
```

## Complexity

- Time: O(n log n) comparisons.
- Space: O(n)

## Interview follow-ups

- What happens if a comparator uses `<=`? (Violates strict weak ordering: UB, and in practice `std::sort` can read out of bounds or crash.)
- `std::sort` vs `std::stable_sort`: when do you need stability, and what do they cost?
- Comparing `double`s with `!=` for ties: when is that risky, and why do trading systems keep prices as integer ticks?
- Function pointer vs lambda vs functor as a comparator: which one can `std::sort` inline?
- How would you get only the top 10 trades by notional without sorting everything? (`std::partial_sort`, `std::nth_element`, or a size-10 heap.)
