#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <cstring>
#include <string>

// Formats with a sentinel-filled buffer and checks nothing past the returned length was touched.
static std::string fmt(std::int64_t v) {
  char buf[40];
  std::memset(buf, '#', sizeof buf);
  std::size_t n = format_int(v, buf);
  if (n == 0 || n > 20) throw qtest::Failure{"bad length " + std::to_string(n) + " for " + std::to_string(v)};
  for (std::size_t i = n; i < sizeof buf; ++i)
    if (buf[i] != '#') throw qtest::Failure{"wrote past the returned length for " + std::to_string(v)};
  return std::string(buf, n);
}

EXAMPLE("Example 1: positive, negative and zero") {
  char buf[32];
  CHECK_EQ(format_int(12345, buf), 5u);
  CHECK_EQ(std::string(buf, 5), std::string("12345"));
  CHECK_EQ(format_int(-42, buf), 3u);
  CHECK_EQ(std::string(buf, 3), std::string("-42"));
  CHECK_EQ(format_int(0, buf), 1u);
  CHECK_EQ(std::string(buf, 1), std::string("0"));
}

EXAMPLE("Example 2: INT64_MIN and INT64_MAX") {
  CHECK_EQ(fmt(INT64_MIN), std::string("-9223372036854775808"));
  CHECK_EQ(fmt(INT64_MAX), std::string("9223372036854775807"));
}

CASE("single digits and their negatives") {
  for (int d = 0; d <= 9; ++d) {
    CHECK_EQ(fmt(d), std::to_string(d));
    if (d) CHECK_EQ(fmt(-d), std::to_string(-d));
  }
}

CASE("powers of ten and their neighbours") {
  std::int64_t p = 1;
  for (int i = 0; i <= 18; ++i, p = i <= 18 ? p * 10 : p) {
    CHECK_EQ(fmt(p), std::to_string(p));
    CHECK_EQ(fmt(p - 1), std::to_string(p - 1));
    CHECK_EQ(fmt(p + 1), std::to_string(p + 1));
    CHECK_EQ(fmt(-p), std::to_string(-p));
    CHECK_EQ(fmt(-(p - 1)), std::to_string(-(p - 1)));
  }
}

CASE("values near the int64 limits") {
  CHECK_EQ(fmt(INT64_MIN + 1), std::string("-9223372036854775807"));
  CHECK_EQ(fmt(INT64_MAX - 1), std::string("9223372036854775806"));
  CHECK_EQ(fmt(-1), std::string("-1"));
}

CASE("odd and even digit counts (pair writing edge)") {
  CHECK_EQ(fmt(10), std::string("10"));
  CHECK_EQ(fmt(100), std::string("100"));
  CHECK_EQ(fmt(1000), std::string("1000"));
  CHECK_EQ(fmt(-99), std::string("-99"));
  CHECK_EQ(fmt(-100), std::string("-100"));
  CHECK_EQ(fmt(1000000007), std::string("1000000007"));
}

CASE("matches std::to_string on pseudo-random values of every magnitude") {
  std::uint64_t s = 31337;
  for (int i = 0; i < 20000; ++i) {
    s = s * 6364136223846793005ull + 1442695040888963407ull;
    std::int64_t v = static_cast<std::int64_t>(s) >> (s % 63);
    CHECK_EQ(fmt(v), std::to_string(v));
  }
}

CASE("writes at an offset inside a larger message buffer") {
  char msg[64];
  std::memset(msg, 0, sizeof msg);
  std::memcpy(msg, "38=", 3);
  std::size_t n = 3 + format_int(250, msg + 3);
  msg[n++] = '|';
  std::memcpy(msg + n, "44=", 3);
  n += 3;
  n += format_int(-1012500, msg + n);
  CHECK_EQ(std::string(msg, n), std::string("38=250|44=-1012500"));
}
