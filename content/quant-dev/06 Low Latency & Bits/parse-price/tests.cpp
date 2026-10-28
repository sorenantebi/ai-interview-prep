#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <optional>
#include <string>

using P = std::optional<std::int64_t>;

EXAMPLE("Example 1: valid prices") {
  CHECK_EQ(parse_price("123.4500"), P(1234500));
  CHECK_EQ(parse_price("-0.25"), P(-2500));
  CHECK_EQ(parse_price("7"), P(70000));
}

EXAMPLE("Example 2: invalid prices") {
  CHECK(!parse_price("1.23456").has_value());
  CHECK(!parse_price("12a").has_value());
  CHECK(!parse_price("").has_value());
}

CASE("fraction digits are padded to 4 places") {
  CHECK_EQ(parse_price("0.1"), P(1000));
  CHECK_EQ(parse_price("0.01"), P(100));
  CHECK_EQ(parse_price("0.001"), P(10));
  CHECK_EQ(parse_price("0.0001"), P(1));
  CHECK_EQ(parse_price("99.9999"), P(999999));
  CHECK_EQ(parse_price("5.0"), P(50000));
}

CASE("zeros, negative zero and leading zeros") {
  CHECK_EQ(parse_price("0"), P(0));
  CHECK_EQ(parse_price("-0"), P(0));
  CHECK_EQ(parse_price("-0.0000"), P(0));
  CHECK_EQ(parse_price("007.5"), P(75000));
  CHECK_EQ(parse_price("-0001"), P(-10000));
}

CASE("malformed syntax is rejected") {
  const char* bad[] = {"-", ".", ".5", "-.5", "7.", "-7.", "1.2.3", "--1", "+1", " 1", "1 ",
                       "1,5", "abc", "1e5", "0x10", "1.-2", "1..2", "-1-", "\t2"};
  for (const char* s : bad) CHECK(!parse_price(s).has_value());
}

CASE("more than four decimals is rejected even with trailing zeros") {
  CHECK(!parse_price("1.00000").has_value());
  CHECK(!parse_price("0.12345").has_value());
  CHECK(!parse_price("-3.141592").has_value());
}

CASE("limits of int64 ticks") {
  CHECK_EQ(parse_price("922337203685477.5807"), P(INT64_MAX));
  CHECK_EQ(parse_price("-922337203685477.5807"), P(-INT64_MAX));
  CHECK_EQ(parse_price("922337203685477"), P(9223372036854770000LL));
  CHECK(!parse_price("922337203685477.5808").has_value());
  CHECK(!parse_price("922337203685478").has_value());
  CHECK(!parse_price("9223372036854775807").has_value());
  CHECK(!parse_price("99999999999999999999999").has_value());
  CHECK(!parse_price("-99999999999999999999999.9999").has_value());
}

CASE("string_view that is a slice of a larger buffer") {
  std::string msg = "44=101.25|38=100";
  std::string_view px(msg.data() + 3, 6);
  CHECK_EQ(parse_price(px), P(1012500));
  CHECK(!parse_price(std::string_view(msg.data() + 3, 7)).has_value());  // includes '|'
}

CASE("round-trips every whole-and-fraction combination in a grid") {
  for (std::int64_t whole = 0; whole < 300; whole += 7) {
    for (std::int64_t frac = 0; frac < 10000; frac += 37) {
      std::string f = std::to_string(frac);
      f = std::string(4 - f.size(), '0') + f;
      std::string s = std::to_string(whole) + "." + f;
      CHECK_EQ(parse_price(s), P(whole * 10000 + frac));
      CHECK_EQ(parse_price("-" + s), P(-(whole * 10000 + frac)));
    }
  }
}
