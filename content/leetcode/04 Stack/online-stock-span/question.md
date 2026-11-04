---
video: https://www.youtube.com/watch?v=slYh0ZNEqSw
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/online-stock-span/
neetcode: https://neetcode.io/problems/online-stock-span
---
# Online Stock Span

**Topic:** Stack · **Difficulty:** Medium

## Problem

Design a class that collects daily stock price quotes one at a time and, for each new quote, returns the span of the stock's price for the current day.

The span of a day is the maximum number of consecutive days, starting from that day and going backward, for which the price was less than or equal to that day's price. The current day is included in the count.

For example, if the prices of the last four days are `[7, 2, 1, 2]` and today's price is `2`, the span is `4`, because the price was at most `2` on all four of those consecutive days (counting today). If the prices of the last four days are `[7, 34, 1, 2]` and today's price is `8`, the span is `3`.

Implement the `StockSpanner` class:

- `StockSpanner()` initializes the object.
- `int next(int price)` returns the span of the stock's price given that today's price is `price`.

## Examples

**Example 1**
```text
Input
["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
[[], [100], [80], [60], [70], [60], [75], [85]]
Output
[null, 1, 1, 1, 2, 1, 4, 6]
```

Explanation:
```text
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // return 1
stockSpanner.next(80);  // return 1
stockSpanner.next(60);  // return 1
stockSpanner.next(70);  // return 2
stockSpanner.next(60);  // return 1
stockSpanner.next(75);  // return 4, the last 4 prices (including today's 75) were <= 75
stockSpanner.next(85);  // return 6
```

## Constraints

- `1 <= price <= 10^5`
- At most `10^4` calls will be made to `next`.
