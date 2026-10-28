---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Parse a Price into Ticks

**Topic:** Low Latency & Bits · **Difficulty:** Medium

## Problem

Text protocols such as FIX send prices as decimal strings (`44=123.4500`). Trading systems never keep those as `double`: they convert them to an integer number of **ticks** so arithmetic and comparisons are exact. The conversion sits on the hot path for every message, so it must be fast and must never silently accept garbage.

Write a parser that turns a decimal string into an `int64_t` with 4 implied decimals (1 tick = 0.0001):

```cpp
std::optional<std::int64_t> parse_price(std::string_view s);
```

Accepted format, nothing else:
- an optional leading `-`,
- one or more digits,
- optionally a `.` followed by **1 to 4** digits.

Return `std::nullopt` for anything else: empty input, spaces, a `+` sign, a lone `-`, a missing integer part (`.5`), a trailing dot (`7.`), more than 4 decimals, a second dot, letters, or a magnitude that doesn't fit in `int64_t` ticks (above 922337203685477.5807).

Do it by hand, digit by digit. **`std::stod`, `atof`, `strtod`, `std::from_chars` and `sscanf` are off limits** (the tests can't detect them, so this is on your honour: those are exactly what the interviewer asked you not to use).

## Examples

**Example 1**
```cpp
parse_price("123.4500");   // 1234500
parse_price("-0.25");      // -2500
parse_price("7");          // 70000
```

**Example 2**
```cpp
parse_price("1.23456");    // std::nullopt (more than 4 decimals)
parse_price("12a");        // std::nullopt
parse_price("");           // std::nullopt
```

## Constraints

- One pass over the input, O(length), no allocation.
- Leading zeros are allowed (`"007.5"` is 75000); `"-0"` is 0.
- Overflow must be detected, not wrapped (signed overflow is undefined behaviour).
