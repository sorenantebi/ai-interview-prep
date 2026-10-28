---
topic: "Trading Systems"
difficulty: Hard
---
# Price-Time Priority Matching Engine

**Topic:** Trading Systems · **Difficulty:** Hard

## Problem

The matching engine is the heart of an exchange. When a new order arrives it is first matched against the opposite side of the book; whatever cannot trade immediately then rests in the book and waits.

Vocabulary:
- A **limit order** says "buy (or sell) up to `qty` at a price no worse than `price`". A buy **crosses** a resting sell when `buy price >= sell price`; a sell crosses a resting buy when `sell price <= buy price`.
- A **market order** has no price: it trades against whatever is available and any unfilled remainder is discarded (it never rests).
- The incoming order is the **taker** (it takes liquidity); the resting order it trades with is the **maker**. Every trade happens at the **maker's** price.
- **Price-time priority:** the incoming order trades with the best price first (lowest ask for a buy, highest bid for a sell); among orders at the same price, the one that arrived first trades first (FIFO).
- A **partial fill** leaves the rest of an order alive: a partly filled maker keeps its place at the front of its queue; a partly filled limit taker rests its remainder at its own limit price.

Implement:

```cpp
enum class Side { Buy, Sell };
using OrderId = std::uint64_t;
using Price = std::int64_t;   // ticks
using Qty = std::int64_t;

struct Fill {
    OrderId maker_id;
    OrderId taker_id;
    Price price;   // always the maker's price
    Qty qty;
    bool operator==(const Fill&) const = default;
};

class MatchingEngine {
public:
    // Matches, then rests any remainder. Returns the fills in the order they happened.
    std::vector<Fill> submit_limit(OrderId id, Side side, Price price, Qty qty);

    // Matches against the book with no price limit; the remainder is dropped.
    std::vector<Fill> submit_market(OrderId id, Side side, Qty qty);

    // Removes a resting order. Returns false if it is not resting (unknown, fully filled or cancelled).
    bool cancel(OrderId id);

    // (price, total resting quantity) of the best level, or std::nullopt.
    std::optional<std::pair<Price, Qty>> best_bid() const;
    std::optional<std::pair<Price, Qty>> best_ask() const;

    // Quantity still resting for this order (0 if it is not resting).
    Qty resting_qty(OrderId id) const;
};
```

Order ids are unique across all submissions (you don't need to check). An order with `qty <= 0` does nothing and returns no fills.

## Examples

**Example 1**
```cpp
MatchingEngine m;
m.submit_limit(1, Side::Sell, 101, 5);   // []
m.submit_limit(2, Side::Sell, 101, 3);   // []
m.submit_limit(3, Side::Sell, 103, 4);   // []
// buy 10 up to 102: takes 101 x5 from #1, then 101 x3 from #2, cannot reach 103
m.submit_limit(4, Side::Buy, 102, 10);   // [{1,4,101,5}, {2,4,101,3}]
m.best_bid();                            // (102, 2): the remainder of #4 rests
m.best_ask();                            // (103, 4)
```

**Example 2**
```cpp
MatchingEngine m;
m.submit_limit(1, Side::Buy, 99, 4);
m.submit_limit(2, Side::Buy, 100, 2);
m.submit_market(3, Side::Sell, 5);       // [{2,3,100,2}, {1,3,99,3}]
m.resting_qty(1);                        // 1
m.cancel(1);                             // true
m.submit_market(4, Side::Sell, 5);       // []: book is empty, nothing rests
m.best_bid();                            // std::nullopt
```

## Constraints

- Up to `10^6` orders; prices are arbitrary `int64` ticks.
- Matching costs O(log P) per price level touched plus O(1) per fill; `cancel` O(log P) or better.
- Single-threaded.
