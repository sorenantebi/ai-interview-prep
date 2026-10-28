---
topic: "Low Latency & Bits"
difficulty: Medium
---
# Integer to String, Fast - Solution

## Intuition

Peeling digits with `% 10` and `/ 10` produces them **backwards**. Instead of writing to a temporary and reversing, count the digits first, then fill the buffer from the right end towards the left. To handle `INT64_MIN`, take the magnitude as `uint64_t`: `0 - static_cast<uint64_t>(v)` is well-defined modular arithmetic and gives 9223372036854775808 correctly.

The classic speed-up halves the number of (slow) divisions: divide by 100 and copy two characters at once from a 200-byte table `"000102...99"`.

## Approach

1. If `v < 0`, write `-` and set `u = 0 - uint64_t(v)`; else `u = v`.
2. Count digits of `u` (compare against powers of ten; at most 20).
3. Set `p` to one past the last digit. While `u >= 100`, write the two digits of `u % 100` from the table and `u /= 100`.
4. Write the last one or two digits.
5. Return the sign length plus the digit count.

## Code

```cpp
#include <cstddef>
#include <cstdint>
#include <cstring>

namespace {
constexpr char kDigitPairs[] =
    "00010203040506070809101112131415161718192021222324252627282930313233343536373839"
    "40414243444546474849505152535455565758596061626364656667686970717273747576777879"
    "8081828384858687888990919293949596979899";

int count_digits(std::uint64_t u) {
    int n = 1;
    for (std::uint64_t p = 10; n < 20 && u >= p; p *= 10) ++n;
    return n;
}
}  // namespace

std::size_t format_int(std::int64_t v, char* buf) {
    std::size_t sign = 0;
    std::uint64_t u = static_cast<std::uint64_t>(v);
    if (v < 0) {
        *buf = '-';
        sign = 1;
        u = 0 - u;  // modular negation: correct even for INT64_MIN
    }
    int digits = count_digits(u);
    char* p = buf + sign + digits;
    while (u >= 100) {
        p -= 2;
        std::memcpy(p, kDigitPairs + 2 * (u % 100), 2);
        u /= 100;
    }
    if (u >= 10) {
        p -= 2;
        std::memcpy(p, kDigitPairs + 2 * u, 2);
    } else {
        *--p = static_cast<char>('0' + u);
    }
    return sign + digits;
}
```

## Complexity

- Time: O(d) for d digits, with about d/2 divisions by a constant (which the compiler turns into a multiply and shift).
- Space: O(1) plus a 200-byte constant table that stays in L1 cache.

## Interview follow-ups

- Why does `count_digits` stop at `n < 20`? (`p *= 10` would overflow past 10^19; 20 digits is the maximum for `uint64_t`.)
- Count digits faster: `log2_floor(u) * 1233 >> 12` approximates log10, then one comparison fixes it.
- Format a fixed-point price (ticks with 4 decimals) the same way: integer part, `.`, exactly 4 zero-padded fraction digits.
- FIX fields are often fixed width with leading zeros. How would you write a zero-padded version without counting digits?
- What does `std::to_chars` (C++17) give you that `sprintf` doesn't? (No locale, no allocation, no format parsing: it's close to this code.)
