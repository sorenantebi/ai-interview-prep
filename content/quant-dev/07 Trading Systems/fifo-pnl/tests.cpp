#include "qtest.h"
#include "attempt.cpp"
#include <deque>
#include <random>

using I = std::int64_t;

EXAMPLE("Example 1: two long lots, partial FIFO close") {
  PositionTracker t;
  t.on_fill(Side::Buy, 100, 10);
  t.on_fill(Side::Buy, 110, 10);
  CHECK_NEAR(t.average_cost().value_or(-1), 105.0, 1e-9);
  t.on_fill(Side::Sell, 120, 15);
  CHECK_EQ(t.position(), I{5});
  CHECK_EQ(t.realized_pnl(), I{250});
  CHECK_EQ(t.unrealized_pnl(108), I{-10});
  CHECK_NEAR(t.average_cost().value_or(-1), 110.0, 1e-9);
}

EXAMPLE("Example 2: flip through zero into a short and cover it") {
  PositionTracker t;
  t.on_fill(Side::Buy, 50, 5);
  t.on_fill(Side::Sell, 48, 8);
  CHECK_EQ(t.position(), I{-3});
  CHECK_EQ(t.realized_pnl(), I{-10});
  CHECK_EQ(t.unrealized_pnl(45), I{9});
  t.on_fill(Side::Buy, 45, 3);
  CHECK_EQ(t.position(), I{0});
  CHECK_EQ(t.realized_pnl(), I{-1});
  CHECK(!t.average_cost().has_value());
}

CASE("fresh tracker is flat") {
  PositionTracker t;
  CHECK_EQ(t.position(), I{0});
  CHECK_EQ(t.realized_pnl(), I{0});
  CHECK_EQ(t.unrealized_pnl(123), I{0});
  CHECK(!t.average_cost().has_value());
}

CASE("short position built over several sells, covered FIFO") {
  PositionTracker t;
  t.on_fill(Side::Sell, 200, 2);
  t.on_fill(Side::Sell, 210, 2);
  t.on_fill(Side::Sell, 190, 1);
  CHECK_EQ(t.position(), I{-5});
  CHECK_NEAR(t.average_cost().value_or(-1), 1010.0 / 5, 1e-9);
  CHECK_EQ(t.unrealized_pnl(195), I{(200 - 195) * 2 + (210 - 195) * 2 + (190 - 195) * 1});
  t.on_fill(Side::Buy, 205, 3);  // covers 2 @200 (-10) and 1 @210 (+5)
  CHECK_EQ(t.realized_pnl(), I{-5});
  CHECK_EQ(t.position(), I{-2});
  CHECK_NEAR(t.average_cost().value_or(-1), (210.0 + 190.0) / 2, 1e-9);
}

CASE("flip from short to long opens the new lot at the fill price") {
  PositionTracker t;
  t.on_fill(Side::Sell, 30, 4);
  t.on_fill(Side::Buy, 25, 10);  // +20 on the short, then long 6 @25
  CHECK_EQ(t.realized_pnl(), I{20});
  CHECK_EQ(t.position(), I{6});
  CHECK_NEAR(t.average_cost().value_or(-1), 25.0, 1e-9);
  CHECK_EQ(t.unrealized_pnl(27), I{12});
  t.on_fill(Side::Sell, 24, 6);
  CHECK_EQ(t.realized_pnl(), I{14});
  CHECK_EQ(t.unrealized_pnl(999), I{0});
}

CASE("FIFO, not LIFO: the oldest lot closes first") {
  PositionTracker t;
  t.on_fill(Side::Buy, 10, 1);
  t.on_fill(Side::Buy, 20, 1);
  t.on_fill(Side::Sell, 20, 1);
  CHECK_EQ(t.realized_pnl(), I{10});  // LIFO would give 0
  CHECK_NEAR(t.average_cost().value_or(-1), 20.0, 1e-9);
}

CASE("exact close to flat then reopen") {
  PositionTracker t;
  t.on_fill(Side::Buy, 100, 3);
  t.on_fill(Side::Sell, 101, 3);
  CHECK_EQ(t.position(), I{0});
  CHECK(!t.average_cost().has_value());
  t.on_fill(Side::Sell, 99, 2);
  CHECK_EQ(t.position(), I{-2});
  CHECK_EQ(t.realized_pnl(), I{3});
  CHECK_EQ(t.unrealized_pnl(100), I{-2});
}

CASE("large values: 10^6 units at 10^7 ticks") {
  PositionTracker t;
  t.on_fill(Side::Buy, 10000000, 1000000);
  t.on_fill(Side::Sell, 1, 1000000);
  CHECK_EQ(t.realized_pnl(), I{-9999999LL * 1000000LL});
  t.on_fill(Side::Sell, 10000000, 1000000);
  CHECK_EQ(t.unrealized_pnl(1), I{9999999LL * 1000000LL});
}

CASE("random fills match a unit-lot oracle") {
  std::mt19937_64 rng(99);
  auto rnd = [&](long lo, long hi) { return std::uniform_int_distribution<long>(lo, hi)(rng); };
  PositionTracker t;
  std::deque<I> units;  // one entry per open unit (its entry price), all with the sign of pos
  I pos = 0, realized = 0;
  for (int i = 0; i < 5000; ++i) {
    I dir = rnd(0, 1) ? 1 : -1;
    I price = rnd(90, 110), qty = rnd(1, 12);
    t.on_fill(dir == 1 ? Side::Buy : Side::Sell, price, qty);
    for (I k = 0; k < qty; ++k) {
      if (pos * dir < 0) { realized += -dir * (price - units.front()); units.pop_front(); }
      else units.push_back(price);
      pos += dir;
    }
    CHECK_EQ(t.position(), pos);
    CHECK_EQ(t.realized_pnl(), realized);
    I mark = rnd(80, 120), unreal = 0, cost = 0;
    for (I e : units) { unreal += (pos > 0 ? mark - e : e - mark); cost += e; }
    CHECK_EQ(t.unrealized_pnl(mark), unreal);
    if (pos == 0) CHECK(!t.average_cost().has_value());
    else CHECK_NEAR(t.average_cost().value_or(-1), static_cast<double>(cost) / units.size(), 1e-9);
  }
}

CASE("a million alternating fills stay fast") {
  PositionTracker t;
  for (int i = 0; i < 1000000; ++i) t.on_fill(i % 2 ? Side::Sell : Side::Buy, 100 + i % 7, 1 + i % 3);
  CHECK(t.position() > 0);
  CHECK(t.average_cost().has_value());
}
