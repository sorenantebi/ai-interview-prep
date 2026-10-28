---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Integer to String, Fast

**Topic:** Low Latency & Bits · **Difficulty:** Medium

## Problem

Order entry gateways write FIX or other text messages: quantities, order ids and prices as decimal digits. `std::to_string` allocates a `std::string` and `sprintf` parses a format string and checks the locale, both far too slow per field. Instead, you format straight into a pre-allocated send buffer.

Implement:

```cpp
// Writes the decimal form of v into buf (no '\0' terminator) and returns the number of chars written.
// buf has room for at least 20 chars ("-9223372036854775808" is the longest).
std::size_t format_int(std::int64_t v, char* buf);
```

Rules:
- Negative numbers get a leading `-`; no `+`, no leading zeros, `0` is written as `"0"`.
- `INT64_MIN` must work. Careful: `-v` overflows for it.
- Don't write past the returned length.
- **No `std::to_string`, `sprintf`/`snprintf`, `std::to_chars`, streams or `std::format`.**

## Examples

**Example 1**
```cpp
char buf[32];
std::size_t n = format_int(12345, buf);    // n == 5, buf starts with "12345"
n = format_int(-42, buf);                   // n == 3, "-42"
n = format_int(0, buf);                     // n == 1, "0"
```

**Example 2**
```cpp
format_int(INT64_MIN, buf);   // 20, "-9223372036854775808"
format_int(INT64_MAX, buf);   // 19, "9223372036854775807"
```

## Constraints

- O(number of digits), no heap allocation, no temporary `std::string`.
