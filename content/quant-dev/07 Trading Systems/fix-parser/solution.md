---
topic: "Trading Systems"
difficulty: Medium
---
# FIX Message Parser - Solution

## Intuition

Split on SOH, split each field on its first `=`, and remember where each field starts in the raw buffer. With those start offsets, both integrity checks are simple arithmetic on the original bytes:

- the body runs from the start of field 3 (`35=`) to the start of the last field (`10=`), so `BodyLength = start[last] - start[2]`;
- the checksum covers bytes `[0, start[last])`.

Do the structural checks first, because the length and checksum checks assume the 8/9/35/10 layout is in place.

## Approach

1. Reject empty input or input not ending in SOH (this also guarantees every `find(SOH)` succeeds).
2. Walk the fields: find the next SOH, find the first `=`, validate tag (1-9 digits, no leading zero) and value (non-empty). Record `(tag, value)` and the field's start offset.
3. Check the layout: at least 4 fields, tags `8, 9, 35` first, `10` last, and no `8/9/10` in between.
4. Parse tag 9 as digits only and compare with `start[last] - start[2]`.
5. Sum bytes `[0, start[last])` as `unsigned char`, mod 256, and compare with tag 10 (exactly 3 digits).

## Code

```cpp
#include <cstddef>
#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

enum class FixError { Ok, Malformed, BadBodyLength, BadChecksum };

struct FixMessage {
    std::vector<std::pair<int, std::string>> fields;

    std::optional<std::string> get(int tag) const {
        for (const auto& [t, v] : fields)
            if (t == tag) return v;
        return std::nullopt;
    }

    std::string msg_type() const { return get(35).value_or(""); }
};

struct ParseResult {
    FixError error;
    FixMessage message;
};

namespace detail {
// Digits-only number of at most 9 digits (fits in int). nullopt otherwise.
inline std::optional<long> digits(std::string_view s) {
    if (s.empty() || s.size() > 9) return std::nullopt;
    long v = 0;
    for (char c : s) {
        if (c < '0' || c > '9') return std::nullopt;
        v = v * 10 + (c - '0');
    }
    return v;
}
}  // namespace detail

ParseResult parse_fix(std::string_view raw) {
    constexpr char SOH = '\x01';
    ParseResult bad{FixError::Malformed, {}};
    if (raw.empty() || raw.back() != SOH) return bad;

    FixMessage msg;
    std::vector<std::size_t> start;
    for (std::size_t pos = 0; pos < raw.size();) {
        const std::size_t end = raw.find(SOH, pos);  // exists: raw ends with SOH
        const std::string_view field = raw.substr(pos, end - pos);
        const std::size_t eq = field.find('=');
        if (eq == std::string_view::npos || eq + 1 == field.size() || field[0] == '0') return bad;
        const auto tag = detail::digits(field.substr(0, eq));
        if (!tag) return bad;
        msg.fields.emplace_back(static_cast<int>(*tag), std::string(field.substr(eq + 1)));
        start.push_back(pos);
        pos = end + 1;
    }

    const auto& f = msg.fields;
    const std::size_t n = f.size();
    if (n < 4 || f[0].first != 8 || f[1].first != 9 || f[2].first != 35 || f[n - 1].first != 10) return bad;
    for (std::size_t i = 2; i + 1 < n; ++i)
        if (f[i].first == 8 || f[i].first == 9 || f[i].first == 10) return bad;

    const auto body_len = detail::digits(f[1].second);
    if (!body_len || static_cast<std::size_t>(*body_len) != start[n - 1] - start[2])
        return {FixError::BadBodyLength, {}};

    unsigned sum = 0;
    for (std::size_t i = 0; i < start[n - 1]; ++i) sum += static_cast<unsigned char>(raw[i]);
    const auto check = detail::digits(f[n - 1].second);
    if (f[n - 1].second.size() != 3 || !check || static_cast<unsigned>(*check) != sum % 256)
        return {FixError::BadChecksum, {}};

    return {FixError::Ok, std::move(msg)};
}
```

## Complexity

- Time: O(L) for a message of L bytes (one pass to split, one to sum; `get` is O(fields)).
- Space: O(L) for the copied values.

## Interview follow-ups

- **Zero copy.** On a hot path, store `std::string_view`s into the receive buffer instead of `std::string`s (the buffer must outlive the message), and put the fields into a small fixed array or a tag-indexed table for O(1) `get`.
- **Don't parse what you don't need.** Gateways often scan only for the handful of tags they care about (35, 11, 39, 150, ...) and skip the rest.
- **Repeating groups.** Tags like `268` (NoMDEntries) are followed by a count of repeated sub-blocks; a flat map loses them. That's why `fields` keeps wire order and duplicates.
- **Streaming / TCP framing.** A TCP read can contain half a message or three messages. Use `8=...|9=N|` to know exactly how many more bytes to wait for (`N` + the 7-byte `10=xxx|` trailer) before parsing.
- **Numbers.** Prices arrive as decimal text (`25.5`); convert to integer ticks with a hand-written parser (or `std::from_chars`), never via `double` round trips.
- **Binary protocols.** Most low-latency venues offer binary alternatives (SBE, ITCH/OUCH, exchange-native formats) with fixed offsets: no parsing at all, just reinterpreting bytes.
