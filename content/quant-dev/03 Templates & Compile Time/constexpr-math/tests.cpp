#include "qtest.h"
#include "attempt.cpp"
#include <array>
#include <type_traits>

EXAMPLE("Example 1: factorial and fibonacci as constants") {
  constexpr auto f = factorial(5);
  CHECK_EQ(f, 120ULL);
  std::array<int, factorial(3)> a{};
  CHECK_EQ(a.size(), 6u);
  CHECK_EQ(fibonacci(10), 55ULL);
}

EXAMPLE("Example 2: is_prime") {
  CHECK_EQ(is_prime(97), true);
  CHECK_EQ(is_prime(91), false);
  CHECK_EQ(is_prime(1), false);
}

CASE("factorial base cases and the largest that fits") {
  constexpr auto f0 = factorial(0), f1 = factorial(1), f20 = factorial(20);
  CHECK_EQ(f0, 1ULL);
  CHECK_EQ(f1, 1ULL);
  CHECK_EQ(f20, 2432902008176640000ULL);
}

CASE("factorial usable as a template argument") {
  CHECK_EQ((std::integral_constant<unsigned long long, factorial(10)>::value), 3628800ULL);
}

CASE("fibonacci small values and F(93)") {
  constexpr unsigned long long expect[] = {0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55};
  for (unsigned i = 0; i <= 10; ++i) CHECK_EQ(fibonacci(i), expect[i]);
  constexpr auto f93 = fibonacci(93);
  CHECK_EQ(f93, 12200160415121876738ULL);
}

CASE("fibonacci recurrence holds at compile time for large n") {
  constexpr auto a = fibonacci(80), b = fibonacci(81), c = fibonacci(82);
  CHECK_EQ(a + b, c);
  CHECK_EQ(c, 61305790721611591ULL);
}

CASE("is_prime on 0, 1, 2 and small numbers") {
  constexpr bool p[] = {false, false, true, true, false, true, false, true, false, false, false, true};
  for (unsigned long long n = 0; n < 12; ++n) CHECK_EQ(is_prime(n), p[n]);
}

CASE("is_prime agrees with a sieve up to 10000") {
  std::array<bool, 10001> composite{};
  for (int i = 2; i * i <= 10000; ++i)
    if (!composite[i]) for (int j = i * i; j <= 10000; j += i) composite[j] = true;
  for (unsigned long long n = 2; n <= 10000; ++n) CHECK_EQ(is_prime(n), !composite[n]);
}

CASE("is_prime on large numbers and squares of primes") {
  constexpr bool big = is_prime(1000000007ULL);
  CHECK(big);
  CHECK(is_prime(2147483647ULL));                  // 2^31 - 1
  CHECK(!is_prime(1000000007ULL * 3ULL));
  CHECK(!is_prime(49ULL));
  CHECK(!is_prime(1000003ULL * 1000003ULL));
  CHECK(is_prime(4294967291ULL));                  // largest prime below 2^32
}

CASE("results are compile-time constants") {
  constexpr bool ok = factorial(4) == 24 && fibonacci(12) == 144 && is_prime(13) && !is_prime(15);
  CHECK(ok);
}
