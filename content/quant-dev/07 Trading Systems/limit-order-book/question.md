---
topic: "Trading Systems"
difficulty: Hard
---
# Limit Order Book

**Topic:** Trading Systems · **Difficulty:** Hard

## Problem

An exchange keeps, for every instrument, a **limit order book**: all the buy orders (**bids**) and sell orders (**asks**) that are waiting to trade. Each order has an id, a side, a limit price and a quantity. Orders at the same price form a **price level**, and inside a level they queue in arrival order (**time priority**): the order that arrived first trades first. The **best bid** is the highest buy price, the **best ask** the lowest sell price; together they are the "top of book" every trading strategy watches.

Prices are integers in **ticks** (the minimum price increment), so no floating point is involved.

Implement the resting side of a book. It never matches orders (that is the matching engine's job): a buy priced at or above the best ask simply rests like any other order.

```cpp
enum class Side { Buy, Sell };
using OrderId = std::uint64_t;
using Price = std::int64_t;   // ticks
using Qty = std::int64_t;

class OrderBook {
public:
    // Rests a new order at the back of its price level.
    // Returns false (and changes nothing) if qty <= 0 or the id is already live.
    bool add(OrderId id, Side side, Price price, Qty qty);

    // Removes a live order. Returns false if the id is unknown.
    bool cancel(OrderId id);

    // Changes a live order's quantity. Returns false if the id is unknown or new_qty < 0.
    //  - new_qty == 0: same as cancel.
    //  - new_qty <= current qty: the order KEEPS its place in the queue.
    //  - new_qty >  current qty: the order LOSES its place and moves to the back of its level.
    bool modify(OrderId id, Qty new_qty);

    // (price, total quantity at that price) of the best level, or std::nullopt if the side is empty.
    std::optional<std::pair<Price, Qty>> best_bid() const;
    std::optional<std::pair<Price, Qty>> best_ask() const;

    // Up to n levels of one side, best first: bids by descending price, asks by ascending price.
    std::vector<std::pair<Price, Qty>> depth(Side side, std::size_t n) const;

    // Total quantity resting at exactly this price on this side (0 if none).
    Qty volume_at(Side side, Price price) const;

    // Ids resting at this price on this side, in time priority (front of the queue first).
    std::vector<OrderId> queue_at(Side side, Price price) const;

    // Number of live orders.
    std::size_t order_count() const;
};
```

Increasing size losing priority is the rule on most real exchanges: otherwise a trader could join a queue with a tiny order and then grow it while keeping the front spot.

## Examples

**Example 1**
```cpp
OrderBook b;
b.add(1, Side::Buy, 100, 5);
b.add(2, Side::Buy, 101, 3);
b.add(3, Side::Buy, 100, 7);
b.add(4, Side::Sell, 103, 4);
b.best_bid();               // (101, 3)
b.best_ask();               // (103, 4)
b.depth(Side::Buy, 5);      // [(101, 3), (100, 12)]
b.cancel(2);                // true
b.best_bid();               // (100, 12)
b.cancel(2);                // false: already gone
```

**Example 2**
```cpp
OrderBook b;
b.add(1, Side::Sell, 50, 10);
b.add(2, Side::Sell, 50, 10);
b.modify(1, 4);             // true: reduced, keeps its place
b.queue_at(Side::Sell, 50); // [1, 2]
b.modify(1, 8);             // true: increased, goes to the back
b.queue_at(Side::Sell, 50); // [2, 1]
b.volume_at(Side::Sell, 50);// 18
```

## Constraints

- Up to `10^6` live orders and `10^5` distinct price levels; any `int64` price is allowed (no fixed price range).
- `add`, `cancel` and `modify` in O(log P) or better (P = number of levels on that side); `best_bid` / `best_ask` in O(1) or O(log P).
- `depth(side, n)` in O(n) after locating the best level; `queue_at` in O(log P + length of the queue).
- Single-threaded.
