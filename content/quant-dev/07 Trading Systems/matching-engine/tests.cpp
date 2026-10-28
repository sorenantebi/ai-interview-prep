#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <ostream>
#include <random>

std::ostream& operator<<(std::ostream& o, const Fill& f) {
  return o << "{maker " << f.maker_id << ", taker " << f.taker_id << ", px " << f.price << ", qty " << f.qty << "}";
}
using Fills = std::vector<Fill>;
using Lvl = std::optional<std::pair<Price, Qty>>;
static Lvl L(Price p, Qty q) { return std::pair<Price, Qty>{p, q}; }

EXAMPLE("Example 1: a limit buy sweeps one level and rests the remainder") {
  MatchingEngine m;
  CHECK(m.submit_limit(1, Side::Sell, 101, 5).empty());
  CHECK(m.submit_limit(2, Side::Sell, 101, 3).empty());
  CHECK(m.submit_limit(3, Side::Sell, 103, 4).empty());
  CHECK_EQ(m.submit_limit(4, Side::Buy, 102, 10), (Fills{{1, 4, 101, 5}, {2, 4, 101, 3}}));
  CHECK_EQ(m.best_bid(), L(102, 2));
  CHECK_EQ(m.best_ask(), L(103, 4));
}

EXAMPLE("Example 2: market sell, partial maker, cancel, market into empty book") {
  MatchingEngine m;
  m.submit_limit(1, Side::Buy, 99, 4);
  m.submit_limit(2, Side::Buy, 100, 2);
  CHECK_EQ(m.submit_market(3, Side::Sell, 5), (Fills{{2, 3, 100, 2}, {1, 3, 99, 3}}));
  CHECK_EQ(m.resting_qty(1), Qty{1});
  CHECK(m.cancel(1));
  CHECK(m.submit_market(4, Side::Sell, 5).empty());
  CHECK(!m.best_bid().has_value());
}

CASE("non-crossing orders just rest") {
  MatchingEngine m;
  CHECK(m.submit_limit(1, Side::Buy, 100, 5).empty());
  CHECK(m.submit_limit(2, Side::Sell, 101, 5).empty());
  CHECK(m.submit_limit(3, Side::Buy, 100, 1).empty());
  CHECK_EQ(m.best_bid(), L(100, 6));
  CHECK_EQ(m.best_ask(), L(101, 5));
  CHECK_EQ(m.resting_qty(3), Qty{1});
  CHECK_EQ(m.resting_qty(99), Qty{0});
}

CASE("one aggressive sell sweeps three bid levels at the makers' prices") {
  MatchingEngine m;
  m.submit_limit(1, Side::Buy, 100, 2);
  m.submit_limit(2, Side::Buy, 102, 3);
  m.submit_limit(3, Side::Buy, 101, 4);
  m.submit_limit(4, Side::Buy, 102, 1);
  m.submit_limit(5, Side::Buy, 99, 10);
  // sell 9 down to 100: 102 (#2 then #4), 101 (#3), 100 (#1 partially); 99 is below the limit
  CHECK_EQ(m.submit_limit(6, Side::Sell, 100, 9), (Fills{{2, 6, 102, 3}, {4, 6, 102, 1}, {3, 6, 101, 4}, {1, 6, 100, 1}}));
  CHECK_EQ(m.best_bid(), L(100, 1));
  CHECK_EQ(m.resting_qty(1), Qty{1});
  CHECK_EQ(m.resting_qty(6), Qty{0});  // fully filled, nothing rests
  CHECK(!m.best_ask().has_value());
  CHECK(!m.cancel(2));                   // filled orders can't be cancelled
}

CASE("taker larger than the whole crossing side rests at its own limit") {
  MatchingEngine m;
  m.submit_limit(1, Side::Sell, 50, 1);
  m.submit_limit(2, Side::Sell, 51, 1);
  m.submit_limit(3, Side::Sell, 60, 1);
  CHECK_EQ(m.submit_limit(4, Side::Buy, 55, 5), (Fills{{1, 4, 50, 1}, {2, 4, 51, 1}}));
  CHECK_EQ(m.best_bid(), L(55, 3));
  CHECK_EQ(m.best_ask(), L(60, 1));
  CHECK_EQ(m.resting_qty(4), Qty{3});
  // and the rested remainder is now a maker for the next seller
  CHECK_EQ(m.submit_limit(5, Side::Sell, 55, 2), (Fills{{4, 5, 55, 2}}));
  CHECK_EQ(m.resting_qty(4), Qty{1});
}

CASE("a partly filled maker keeps the front of its queue") {
  MatchingEngine m;
  m.submit_limit(1, Side::Sell, 10, 5);
  m.submit_limit(2, Side::Sell, 10, 5);
  CHECK_EQ(m.submit_market(3, Side::Buy, 2), (Fills{{1, 3, 10, 2}}));
  CHECK_EQ(m.submit_market(4, Side::Buy, 4), (Fills{{1, 4, 10, 3}, {2, 4, 10, 1}}));
  CHECK_EQ(m.best_ask(), L(10, 4));
}

CASE("cancel removes from the middle of a queue; double cancel fails") {
  MatchingEngine m;
  m.submit_limit(1, Side::Buy, 7, 1);
  m.submit_limit(2, Side::Buy, 7, 2);
  m.submit_limit(3, Side::Buy, 7, 3);
  CHECK(m.cancel(2));
  CHECK(!m.cancel(2));
  CHECK_EQ(m.best_bid(), L(7, 4));
  CHECK_EQ(m.submit_limit(4, Side::Sell, 7, 4), (Fills{{1, 4, 7, 1}, {3, 4, 7, 3}}));
  CHECK(!m.best_bid().has_value());
  CHECK(!m.best_ask().has_value());
}

CASE("market order remainder is dropped, zero quantity does nothing") {
  MatchingEngine m;
  m.submit_limit(1, Side::Sell, 5, 2);
  CHECK_EQ(m.submit_market(2, Side::Buy, 10), (Fills{{1, 2, 5, 2}}));
  CHECK(!m.best_bid().has_value());
  CHECK_EQ(m.resting_qty(2), Qty{0});
  CHECK(m.submit_limit(3, Side::Buy, 5, 0).empty());
  CHECK(m.submit_market(4, Side::Sell, 0).empty());
  CHECK(!m.best_bid().has_value());
}

// Brute-force oracle: a flat vector of resting orders with arrival numbers.
struct Oracle {
  struct O { OrderId id; Side side; Price price; Qty qty; long seq; };
  std::vector<O> v;
  long seq = 0;
  Fills submit(OrderId id, Side side, std::optional<Price> limit, Qty qty) {
    Fills fills;
    while (qty > 0) {
      O* best = nullptr;
      for (auto& o : v) {
        if (o.side == side) continue;
        if (limit && (side == Side::Buy ? o.price > *limit : o.price < *limit)) continue;
        bool better = !best || (side == Side::Buy ? o.price < best->price : o.price > best->price) ||
                      (o.price == best->price && o.seq < best->seq);
        if (better) best = &o;
      }
      if (!best) break;
      Qty t = std::min(qty, best->qty);
      fills.push_back({best->id, id, best->price, t});
      qty -= t;
      best->qty -= t;
      if (best->qty == 0) v.erase(v.begin() + (best - v.data()));
    }
    if (qty > 0 && limit) v.push_back({id, side, *limit, qty, seq++});
    return fills;
  }
  bool cancel(OrderId id) {
    auto it = std::find_if(v.begin(), v.end(), [&](const O& o) { return o.id == id; });
    if (it == v.end()) return false;
    v.erase(it);
    return true;
  }
  Lvl best(Side s) const {
    Lvl out;
    for (auto& o : v) if (o.side == s && (!out || (s == Side::Buy ? o.price > out->first : o.price < out->first))) out = L(o.price, 0);
    if (out) for (auto& o : v) if (o.side == s && o.price == out->first) out->second += o.qty;
    return out;
  }
};

CASE("20000 random limit/market/cancel operations match a brute-force oracle") {
  std::mt19937_64 rng(2024);
  auto rnd = [&](long lo, long hi) { return std::uniform_int_distribution<long>(lo, hi)(rng); };
  MatchingEngine m;
  Oracle o;
  OrderId next = 1;
  for (int step = 0; step < 20000; ++step) {
    long op = rnd(0, 9);
    Side s = rnd(0, 1) ? Side::Buy : Side::Sell;
    if (op < 6) {
      OrderId id = next++;
      Price p = rnd(95, 105);
      Qty q = rnd(1, 15);
      CHECK_EQ(m.submit_limit(id, s, p, q), o.submit(id, s, p, q));
    } else if (op < 7) {
      OrderId id = next++;
      Qty q = rnd(1, 30);
      CHECK_EQ(m.submit_market(id, s, q), o.submit(id, s, std::nullopt, q));
    } else {
      OrderId id = rnd(1, static_cast<long>(next));
      CHECK_EQ(m.cancel(id), o.cancel(id));
    }
    CHECK_EQ(m.best_bid(), o.best(Side::Buy));
    CHECK_EQ(m.best_ask(), o.best(Side::Sell));
    if (step % 50 == 0)
      for (auto& x : o.v) CHECK_EQ(m.resting_qty(x.id), x.qty);
  }
}

CASE("100000 resting orders swept by one market order stays fast") {
  MatchingEngine m;
  const long N = 100000;
  for (long i = 0; i < N; ++i) m.submit_limit(i + 1, Side::Sell, 1000 + i % 5000, 1);
  CHECK_EQ(m.best_ask(), L(1000, 20));
  Fills f = m.submit_market(N + 1, Side::Buy, N + 10);
  CHECK_EQ(f.size(), static_cast<std::size_t>(N));
  CHECK_EQ(f.front(), (Fill{1, N + 1, 1000, 1}));
  CHECK_EQ(f.back(), (Fill{N, N + 1, 1000 + (N - 1) % 5000, 1}));
  CHECK(!m.best_ask().has_value());
}
