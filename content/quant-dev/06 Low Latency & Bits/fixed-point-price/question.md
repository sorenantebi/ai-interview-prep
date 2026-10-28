---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Fixed-Point Price

**Topic:** Low Latency & Bits · **Difficulty:** Medium

## Problem

In floating point, `0.1 + 0.2 != 0.3`. For a trading system that's not a curiosity: a limit price that is off by 1e-17 may fail to match a resting order at "the same" price, and sums of many fills drift. The standard fix is a fixed-point price type: store an integer count of ticks and only convert to or from decimal at the edges.

Implement `Price`, storing an `int64_t` number of ticks with 4 implied decimals (1 tick = 0.0001):

```cpp
class Price {
public:
    static constexpr std::int64_t kScale = 10000;

    constexpr Price() = default;                       // 0
    static constexpr Price from_ticks(std::int64_t ticks);
    static Price from_double(double value);            // round to the nearest tick, halves away from zero
    constexpr std::int64_t ticks() const;
    double to_double() const;
    std::string to_string() const;                     // always 4 decimals: "123.4500", "-0.2500", "0.0000"

    constexpr Price operator+(Price other) const;
    constexpr Price operator-(Price other) const;
    constexpr Price operator*(std::int64_t qty) const; // notional = price * quantity
    // ==, !=, <, <=, >, >= comparing ticks
};
```

## Examples

**Example 1**
```cpp
Price a = Price::from_double(0.1), b = Price::from_double(0.2);
(a + b) == Price::from_double(0.3);   // true (with doubles: 0.1 + 0.2 == 0.3 is false)
(a + b).to_string();                  // "0.3000"
```

**Example 2**
```cpp
Price p = Price::from_ticks(1234500);
p.to_string();                        // "123.4500"
(p * 3).to_string();                  // "370.3500"
Price::from_double(-0.25).to_string();// "-0.2500"
Price::from_double(1.23456).ticks();  // 12346 (rounded)
```

## Constraints

- All arithmetic is integer arithmetic on ticks; `double` appears only in `from_double` / `to_double`.
- Results stay within `int64_t` (no overflow checks needed).
- `to_string` must handle negative prices between -1 and 0 (the integer part is 0 but the sign must show).
