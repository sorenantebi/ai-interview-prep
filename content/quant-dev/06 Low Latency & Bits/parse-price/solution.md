---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Parse a Price into Ticks - Solution

## Intuition

Walk the string once with an index. Accumulate the integer part as a non-negative number, checking for overflow **before** each multiply-add. Then read up to 4 fractional digits and pad them to exactly 4 (`.25` means 2500 ticks). The result is `whole * 10000 + frac`, again overflow-checked, and finally negated if there was a minus sign. Any character that doesn't fit the grammar means `nullopt`.

## Approach

1. If `s` starts with `-`, remember it and skip it.
2. Read digits for the integer part. Require at least one. Before `whole = whole * 10 + d`, check `whole > (INT64_MAX - d) / 10`.
3. If the next character is `.`, read 1 to 4 digits into `frac`, then multiply `frac` by 10 for each missing digit so it's always in units of 0.0001. Zero digits or a fifth digit is an error.
4. If anything is left over, it's an error.
5. Check `whole <= (INT64_MAX - frac) / 10000`, then return `±(whole * 10000 + frac)`. Working in the positive range and negating at the end is safe because `-INT64_MAX` is representable.

## Code

```cpp
#include <cstdint>
#include <limits>
#include <optional>
#include <string_view>

std::optional<std::int64_t> parse_price(std::string_view s) {
    constexpr std::int64_t kMax = std::numeric_limits<std::int64_t>::max();
    constexpr std::int64_t kScale = 10000;
    std::size_t i = 0, n = s.size();
    auto is_digit = [](char c) { return c >= '0' && c <= '9'; };

    bool negative = false;
    if (i < n && s[i] == '-') {
        negative = true;
        ++i;
    }

    std::size_t start = i;
    std::int64_t whole = 0;
    while (i < n && is_digit(s[i])) {
        int d = s[i] - '0';
        if (whole > (kMax - d) / 10) return std::nullopt;
        whole = whole * 10 + d;
        ++i;
    }
    if (i == start) return std::nullopt;  // no integer digits

    std::int64_t frac = 0;
    if (i < n && s[i] == '.') {
        ++i;
        int digits = 0;
        while (i < n && is_digit(s[i])) {
            if (++digits > 4) return std::nullopt;
            frac = frac * 10 + (s[i] - '0');
            ++i;
        }
        if (digits == 0) return std::nullopt;  // "7."
        for (; digits < 4; ++digits) frac *= 10;
    }
    if (i != n) return std::nullopt;  // trailing junk

    if (whole > (kMax - frac) / kScale) return std::nullopt;
    std::int64_t ticks = whole * kScale + frac;
    return negative ? -ticks : ticks;
}
```

## Complexity

- Time: O(length of the string), one pass, no allocation.
- Space: O(1).

## Interview follow-ups

- Why not `std::llround(std::stod(s) * 10000)`? (Slower, locale-dependent, allocates for `std::string`, and `double` can't represent most decimal prices exactly, so large values round wrongly.)
- Speed it up with SWAR: load 8 ASCII digits as one `uint64_t` and convert them in three multiply-add steps.
- Support instruments with different tick sizes (2, 4 or 8 decimals) chosen at run time, or at compile time as a template parameter.
- Should `"1.23450"` (5 decimals but the last is 0) be accepted? Discuss the trade-off with the exchange's spec.
- How do you handle `INT64_MIN`'s extra negative value if the spec requires it?
