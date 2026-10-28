#include "qtest.h"
#include "attempt.cpp"
#include <string>
#include <type_traits>

EXAMPLE("Example 1: sum and count_args") {
  CHECK_EQ(sum(1, 2, 3), 6);
  CHECK_NEAR(sum(1, 2.5), 3.5, 1e-12);
  CHECK_EQ(sum(), 0);
  CHECK_EQ(count_args('a', "b", 3.0), 3u);
}

EXAMPLE("Example 2: all_true and join") {
  CHECK_EQ(all_true(true, 1 < 2, 3), true);
  CHECK_EQ(all_true(true, false), false);
  CHECK_EQ(join(", ", "px", 101.25, 7), std::string("px, 101.25, 7"));
  CHECK_EQ(join("-"), std::string(""));
}

CASE("sum follows arithmetic promotion") {
  CHECK((std::is_same_v<decltype(sum(1, 2.5)), double>));
  CHECK((std::is_same_v<decltype(sum(1LL, 2)), long long>));
  CHECK_EQ(sum(1000000000LL, 2000000000LL, 3000000000LL), 6000000000LL);
  CHECK_NEAR(sum(0.5, 0.25, 0.125, 0.125), 1.0, 1e-12);
  CHECK_EQ(sum(-5, 5), 0);
  CHECK_EQ(sum(42), 42);
}

CASE("sum, count_args and all_true work at compile time") {
  constexpr auto s = sum(1, 2, 3, 4);
  constexpr auto c = count_args(1, 2, 3, 4, 5);
  constexpr bool t = all_true(1, true, 'x');
  CHECK_EQ(s, 10);
  CHECK_EQ(c, 5u);
  CHECK(t);
}

CASE("count_args with zero and many arguments of mixed types") {
  CHECK_EQ(count_args(), 0u);
  CHECK_EQ(count_args(std::string("x")), 1u);
  CHECK_EQ(count_args(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 12u);
}

CASE("all_true on empty pack and with zero values") {
  CHECK_EQ(all_true(), true);
  CHECK_EQ(all_true(1, 2, 0), false);
  CHECK_EQ(all_true(false), false);
  CHECK_EQ(all_true(true, true, true, true), true);
  int* null = nullptr;
  int x = 1;
  CHECK_EQ(all_true(&x, null), false);
}

CASE("join with a single argument has no separator") {
  CHECK_EQ(join(", ", 7), std::string("7"));
  CHECK_EQ(join("", "a", "b", "c"), std::string("abc"));
}

CASE("join streams mixed types with a multi-char separator") {
  std::string side = "BUY";
  CHECK_EQ(join(" | ", side, 100, 'X', -2.5), std::string("BUY | 100 | X | -2.5"));
  CHECK_EQ(join(",", 1, 2, 3, 4, 5), std::string("1,2,3,4,5"));
}

CASE("join keeps empty string arguments") {
  CHECK_EQ(join("/", "", "", ""), std::string("//"));
  CHECK_EQ(join(", ", std::string(), 1), std::string(", 1"));
}
