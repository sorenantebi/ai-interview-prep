#include "qtest.h"
#include "attempt.cpp"
#include <cstdint>
#include <string>
#include <vector>

EXAMPLE("Example 1: 0.1 + 0.2 is exactly 0.3") {
  CHECK(0.1 + 0.2 != 0.3);  // the problem with doubles
  Price a = Price::from_double(0.1), b = Price::from_double(0.2);
  CHECK((a + b) == Price::from_double(0.3));
  CHECK_EQ((a + b).to_string(), std::string("0.3000"));
}

EXAMPLE("Example 2: to_string, multiplication and rounding") {
  Price p = Price::from_ticks(1234500);
  CHECK_EQ(p.to_string(), std::string("123.4500"));
  CHECK_EQ((p * 3).to_string(), std::string("370.3500"));
  CHECK_EQ(Price::from_double(-0.25).to_string(), std::string("-0.2500"));
  CHECK_EQ(Price::from_double(1.23456).ticks(), 12346);
}

CASE("default is zero and from_ticks round-trips") {
  Price z;
  CHECK_EQ(z.ticks(), 0);
  CHECK_EQ(z.to_string(), std::string("0.0000"));
  CHECK_EQ(Price::from_ticks(-7).ticks(), -7);
  constexpr Price c = Price::from_ticks(5) + Price::from_ticks(6);
  CHECK_EQ(c.ticks(), 11);
}

CASE("from_double rounds to the nearest tick") {
  CHECK_EQ(Price::from_double(123.45678).ticks(), 1234568);
  CHECK_EQ(Price::from_double(123.45672).ticks(), 1234567);
  CHECK_EQ(Price::from_double(-123.45678).ticks(), -1234568);
  CHECK_EQ(Price::from_double(0.00004).ticks(), 0);
  CHECK_EQ(Price::from_double(0.00006).ticks(), 1);
  CHECK_EQ(Price::from_double(99.99).ticks(), 999900);
  CHECK_EQ(Price::from_double(0.0).ticks(), 0);
}

CASE("to_string pads fractions and keeps the sign for small negatives") {
  CHECK_EQ(Price::from_ticks(1).to_string(), std::string("0.0001"));
  CHECK_EQ(Price::from_ticks(-1).to_string(), std::string("-0.0001"));
  CHECK_EQ(Price::from_ticks(10000).to_string(), std::string("1.0000"));
  CHECK_EQ(Price::from_ticks(-10050).to_string(), std::string("-1.0050"));
  CHECK_EQ(Price::from_ticks(999999).to_string(), std::string("99.9999"));
  CHECK_EQ(Price::from_ticks(INT64_MAX).to_string(), std::string("922337203685477.5807"));
  CHECK_EQ(Price::from_ticks(INT64_MIN).to_string(), std::string("-922337203685477.5808"));
}

CASE("addition, subtraction and quantity multiplication") {
  Price bid = Price::from_double(99.95), ask = Price::from_double(100.05);
  CHECK_EQ((ask - bid).to_string(), std::string("0.1000"));
  CHECK_EQ((bid - ask).to_string(), std::string("-0.1000"));
  CHECK_EQ((bid * 0).ticks(), 0);
  CHECK_EQ((bid * -2).to_string(), std::string("-199.9000"));
  CHECK_EQ((Price::from_ticks(1) * 1000000).to_string(), std::string("100.0000"));
}

CASE("all six comparison operators") {
  Price a = Price::from_ticks(100), b = Price::from_ticks(200), c = Price::from_ticks(100);
  CHECK(a == c);
  CHECK(a != b);
  CHECK(a < b);
  CHECK(a <= c);
  CHECK(b > a);
  CHECK(b >= a);
  CHECK(!(a < c));
  CHECK(!(b <= a));
  CHECK(Price::from_ticks(-5) < Price());
}

CASE("summing many small prices doesn't drift") {
  Price total;
  double dtotal = 0.0;
  for (int i = 0; i < 100000; ++i) {
    total = total + Price::from_double(0.1);
    dtotal += 0.1;
  }
  CHECK_EQ(total, Price::from_double(10000.0));
  CHECK_EQ(total.to_string(), std::string("10000.0000"));
  CHECK(dtotal != 10000.0);
  CHECK_NEAR(total.to_double(), 10000.0, 1e-9);
}

CASE("to_double and back") {
  std::vector<std::int64_t> ticks = {0, 1, -1, 12345, -98765, 1000000000};
  for (auto t : ticks) {
    Price p = Price::from_ticks(t);
    CHECK_NEAR(p.to_double(), t / 10000.0, 1e-12);
    CHECK_EQ(Price::from_double(p.to_double()), p);
  }
}
