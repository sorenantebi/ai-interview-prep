---
topic: "Trading Systems"
difficulty: Medium
---
# FIX Message Parser

**Topic:** Trading Systems · **Difficulty:** Medium

## Problem

**FIX** (Financial Information eXchange) is the classic text protocol between brokers, banks and exchanges. A message is a list of `tag=value` fields, each ended by the SOH byte (`'\x01'`). Tags are numbers with standard meanings, for example `35` = message type (`D` = new order, `8` = execution report, `0` = heartbeat), `55` = symbol, `54` = side, `38` = quantity, `44` = price.

Every message is framed by three special fields:

- `8` (**BeginString**, e.g. `FIX.4.4`) must be the first field, `9` (**BodyLength**) the second, and `35` (**MsgType**) the third.
- `9` = the number of bytes **after** the SOH that ends the `9=` field, up to **and including** the SOH just before `10=`.
- `10` (**CheckSum**) must be the last field: the sum of every byte before `10=` (from the `8` up to and including the SOH right before `10=`), modulo 256, written as exactly 3 digits (`007`, `216`).

In the examples below `|` stands for SOH so the messages are readable; real messages (and the tests) use `'\x01'`.

Implement:

```cpp
enum class FixError { Ok, Malformed, BadBodyLength, BadChecksum };

struct FixMessage {
    std::vector<std::pair<int, std::string>> fields;  // every field in wire order, including 8, 9 and 10
    std::optional<std::string> get(int tag) const;    // value of the first field with this tag
    std::string msg_type() const;                      // value of tag 35 ("" if absent)
};

struct ParseResult {
    FixError error;
    FixMessage message;  // meaningful only when error == FixError::Ok
};

ParseResult parse_fix(std::string_view raw);
```

Check in this order and return the first error found:

1. **Malformed**: the input is empty or doesn't end with SOH; a field has no `=`; a tag is empty, has a non-digit, starts with `0`, or has more than 9 digits; a value is empty; there are fewer than 4 fields; the first three tags are not `8, 9, 35` or the last is not `10`; or tag `8`, `9` or `10` appears anywhere else.
2. **BadBodyLength**: the value of `9` is not all digits, has more than 9 digits, or differs from the real body length.
3. **BadChecksum**: the value of `10` is not exactly 3 digits or differs from the computed checksum.

## Examples

**Example 1**
```cpp
// "8=FIX.4.4|9=57|35=D|49=ALPHA|56=XCHG|11=ord1|55=ABC|54=1|38=100|44=25.5|10=216|"
ParseResult r = parse_fix(msg);
r.error;                  // FixError::Ok
r.message.msg_type();     // "D"
r.message.get(55);        // "ABC"
r.message.get(44);        // "25.5"
r.message.get(99);        // std::nullopt
r.message.fields.size();  // 11
```

**Example 2**
```cpp
parse_fix("8=FIX.4.4|9=5|35=0|10=163|").error;  // Ok (a heartbeat)
parse_fix("8=FIX.4.4|9=6|35=0|10=163|").error;  // BadBodyLength
parse_fix("8=FIX.4.4|9=5|35=0|10=164|").error;  // BadChecksum
parse_fix("8=FIX.4.4|9=5|35=0|10=163").error;   // Malformed: no final SOH
```

## Constraints

- Messages are at most `64 KiB`. Values may contain any byte except SOH (including `=`; only the first `=` of a field separates tag and value).
- One pass over the input plus copying the values: O(length).
- Never read out of bounds, whatever the input.
