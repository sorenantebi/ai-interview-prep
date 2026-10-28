---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Fixed-Point Price - Solution

## Intuition

Prices on an exchange are already discrete: they live on a tick grid. Storing the integer tick count makes `+`, `-`, `* qty` and comparisons exact and as cheap as integer instructions. Floating point only enters when converting at the boundary, and there you round once to the nearest tick, so `0.1` and `0.2` become exactly 1000 and 2000 ticks and their sum is exactly 3000.

## Approach

1. Store `int64_t ticks_`; a private constructor from ticks backs `from_ticks`.
2. `from_double`: `std::llround(value * kScale)`. `llround` rounds halves away from zero and returns an integer directly.
3. `to_double`: `ticks_ / double(kScale)`.
4. Arithmetic: operate on ticks. `operator*` multiplies by an integer quantity, so the result is still in ticks.
5. Comparisons: `= default` both `operator==` and `operator<=>`; with one `int64_t` member they compare ticks, and the compiler generates all six operators.
6. `to_string`: take the sign separately and work with the magnitude (as `uint64_t`, so even `INT64_MIN` is safe). Write `whole = mag / 10000`, a dot, then `frac = mag % 10000` padded to 4 digits. Using the magnitude is what gets `-0.2500` right: `-2500 / 10000` is `0`, which would lose the sign.

## Code

```cpp
#include <cmath>
#include <compare>
#include <cstdint>
#include <string>

class Price {
public:
    static constexpr std::int64_t kScale = 10000;

    constexpr Price() = default;
    static constexpr Price from_ticks(std::int64_t ticks) { return Price(ticks); }
    static Price from_double(double value) { return Price(std::llround(value * kScale)); }
    constexpr std::int64_t ticks() const { return ticks_; }
    double to_double() const { return static_cast<double>(ticks_) / kScale; }

    std::string to_string() const {
        std::uint64_t mag = ticks_ < 0 ? 0 - static_cast<std::uint64_t>(ticks_) : ticks_;
        std::string frac = std::to_string(mag % kScale);
        return (ticks_ < 0 ? "-" : "") + std::to_string(mag / kScale) + "." +
               std::string(4 - frac.size(), '0') + frac;
    }

    constexpr Price operator+(Price other) const { return Price(ticks_ + other.ticks_); }
    constexpr Price operator-(Price other) const { return Price(ticks_ - other.ticks_); }
    constexpr Price operator*(std::int64_t qty) const { return Price(ticks_ * qty); }

    constexpr bool operator==(const Price&) const = default;
    constexpr auto operator<=>(const Price&) const = default;

private:
    constexpr explicit Price(std::int64_t ticks) : ticks_(ticks) {}
    std::int64_t ticks_ = 0;
};
```

## Complexity

- Time: O(1) for arithmetic and comparisons (single integer instructions); `to_string` is O(digits).
- Space: 8 bytes, same as a `double`.

## Interview follow-ups

- Why can `from_double` still go wrong? (`value * kScale` can land just below a half, e.g. `1.00005 * 10000` might be `10000.499999...`. Parse from the decimal string instead when you can.)
- Add overflow-checked multiplication (`__builtin_mul_overflow` or compare against `INT64_MAX / qty`). What's a realistic bound for price × quantity?
- Make the scale a template parameter: `FixedPoint<int64_t, 8>` for crypto, `<..., 2>` for cents. How do you add two prices with different scales?
- Price × price or price / quantity (VWAP): what scale does the result have and how do you round it?
- Make `to_string` allocation-free by writing into a caller's buffer (see the int-to-string problem).
