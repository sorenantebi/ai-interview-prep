---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/online-stock-span/
neetcode: https://neetcode.io/problems/online-stock-span
---
# Online Stock Span - Solution

## Intuition

The span of today is how far back we can go before hitting a strictly greater price. So we need the nearest previous day with a price greater than today's. Days whose prices are less than or equal to today's can never be that "nearest greater" blocker for any future day once today is present and at least as large, so they can be discarded. This is a monotonic (decreasing) stack, and each entry can also remember the span it already absorbed.

## Approach

1. Keep a stack of `(price, span)` pairs with strictly decreasing prices from bottom to top.
2. On `next(price)`, start with `span = 1` for today.
3. While the stack is non-empty and the top price is `<= price`, pop it and add its span to today's span.
4. Push `(price, span)` and return `span`.

## Code

```python
class StockSpanner:
    def __init__(self):
        self.stack = []  # pair: (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack[-1][1]
            self.stack.pop()
        self.stack.append((price, span))
        return span
```

## Complexity

- **Time:** `O(1)` amortized per call — each price is pushed once and popped at most once.
- **Space:** `O(n)` — the stack may hold all prices (e.g. strictly decreasing input).

## Other Approaches

- **Brute force scan:** store all prices and walk backward from today until a greater price is found — Time `O(n)` per call / Space `O(n)`
- **Monotonic stack of indices:** store indices instead of spans and compute span as `i - stack[-1]` after popping — Time `O(1)` amortized per call / Space `O(n)`

## C++

```cpp
class StockSpanner {
public:
    
    stack<pair<int, int>> st;
    pair<int, int> pr;
    StockSpanner() {
        pr = {0, 0};
    }
    
    int next(int price) {

        int ret = 1;
        while (!st.empty() && price >= pr.first)
        {
            ret += pr.second;
            st.pop();
            if (!st.empty())
                pr = st.top();
        }
        st.push(make_pair(price, ret));
        pr = st.top();
        return (ret);
    }
};

/**
 * Your StockSpanner object will be instantiated and called as such:
 * StockSpanner* obj = new StockSpanner();
 * int param_1 = obj->next(price);
 */
```
