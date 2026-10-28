#include "qtest.h"
#include "attempt.cpp"
#include <string>

EXAMPLE("Example 1: push until full, then wrap around") {
  RingBuffer<int> rb(2);
  CHECK_EQ(rb.push(1), true);
  CHECK_EQ(rb.push(2), true);
  CHECK_EQ(rb.push(3), false);
  CHECK_EQ(rb.pop(), std::optional<int>(1));
  CHECK_EQ(rb.push(3), true);
  CHECK_EQ(rb.pop(), std::optional<int>(2));
  CHECK_EQ(rb.pop(), std::optional<int>(3));
  CHECK(!rb.pop().has_value());
}

EXAMPLE("Example 2: front, size and full with strings") {
  RingBuffer<std::string> rb(3);
  rb.push("a");
  rb.push("b");
  CHECK_EQ(rb.front(), std::string("a"));
  CHECK_EQ(rb.size(), 2u);
  CHECK_EQ(rb.full(), false);
}

CASE("new buffer is empty with the right capacity") {
  RingBuffer<int> rb(5);
  CHECK(rb.empty());
  CHECK(!rb.full());
  CHECK_EQ(rb.size(), 0u);
  CHECK_EQ(rb.capacity(), 5u);
}

CASE("front on an empty buffer throws out_of_range") {
  RingBuffer<int> rb(1);
  bool threw = false;
  try { rb.front(); } catch (const std::out_of_range&) { threw = true; }
  CHECK(threw);
}

CASE("capacity 1 alternates push and pop") {
  RingBuffer<int> rb(1);
  for (int i = 0; i < 100; ++i) {
    CHECK(rb.push(i));
    CHECK(rb.full());
    CHECK(!rb.push(-1));
    CHECK_EQ(rb.front(), i);
    CHECK_EQ(rb.pop(), std::optional<int>(i));
    CHECK(rb.empty());
  }
}

CASE("keeps FIFO order across many wrap-arounds") {
  RingBuffer<int> rb(7);
  int next_in = 0, next_out = 0;
  for (int round = 0; round < 1000; ++round) {
    for (int k = 0; k < (round % 7) + 1 && !rb.full(); ++k) CHECK(rb.push(next_in++));
    for (int k = 0; k < (round % 5) + 1 && !rb.empty(); ++k) CHECK_EQ(rb.pop(), std::optional<int>(next_out++));
    CHECK_EQ(rb.size(), static_cast<std::size_t>(next_in - next_out));
  }
}

CASE("rejected push leaves the buffer unchanged") {
  RingBuffer<int> rb(3);
  rb.push(1); rb.push(2); rb.push(3);
  CHECK(!rb.push(4));
  CHECK_EQ(rb.size(), 3u);
  CHECK_EQ(rb.pop(), std::optional<int>(1));
  CHECK_EQ(rb.pop(), std::optional<int>(2));
  CHECK_EQ(rb.pop(), std::optional<int>(3));
}

struct NoDefault {
  explicit NoDefault(int v) : v(v) {}
  int v;
};

CASE("works for types without a default constructor") {
  RingBuffer<NoDefault> rb(2);
  CHECK(rb.push(NoDefault(7)));
  CHECK_EQ(rb.front().v, 7);
  CHECK_EQ(rb.pop()->v, 7);
}

CASE("a million operations stay fast (O(1) each)") {
  RingBuffer<long long> rb(1 << 10);
  long long sum = 0;
  for (long long i = 0; i < 1000000; ++i) {
    if (rb.full()) sum += *rb.pop();
    rb.push(i);
  }
  while (!rb.empty()) sum += *rb.pop();
  CHECK_EQ(sum, 999999LL * 1000000LL / 2);
}
