#include "qtest.h"
#include "attempt.cpp"
#include <algorithm>
#include <map>
#include <random>

using Lvl = std::optional<std::pair<Price, Qty>>;
using Levels = std::vector<std::pair<Price, Qty>>;

EXAMPLE("Example 1: best levels, depth and cancel") {
  OrderBook b;
  CHECK(b.add(1, Side::Buy, 100, 5));
  CHECK(b.add(2, Side::Buy, 101, 3));
  CHECK(b.add(3, Side::Buy, 100, 7));
  CHECK(b.add(4, Side::Sell, 103, 4));
  CHECK_EQ(b.best_bid(), Lvl(std::pair<Price, Qty>{101, 3}));
  CHECK_EQ(b.best_ask(), Lvl(std::pair<Price, Qty>{103, 4}));
  CHECK_EQ(b.depth(Side::Buy, 5), (Levels{{101, 3}, {100, 12}}));
  CHECK(b.cancel(2));
  CHECK_EQ(b.best_bid(), Lvl(std::pair<Price, Qty>{100, 12}));
  CHECK(!b.cancel(2));
}

EXAMPLE("Example 2: reduce keeps priority, increase loses it") {
  OrderBook b;
  b.add(1, Side::Sell, 50, 10);
  b.add(2, Side::Sell, 50, 10);
  CHECK(b.modify(1, 4));
  CHECK_EQ(b.queue_at(Side::Sell, 50), (std::vector<OrderId>{1, 2}));
  CHECK(b.modify(1, 8));
  CHECK_EQ(b.queue_at(Side::Sell, 50), (std::vector<OrderId>{2, 1}));
  CHECK_EQ(b.volume_at(Side::Sell, 50), Qty{18});
}

CASE("empty book") {
  OrderBook b;
  CHECK(!b.best_bid().has_value());
  CHECK(!b.best_ask().has_value());
  CHECK(b.depth(Side::Buy, 3).empty());
  CHECK_EQ(b.volume_at(Side::Sell, 10), Qty{0});
  CHECK(b.queue_at(Side::Buy, 10).empty());
  CHECK_EQ(b.order_count(), 0u);
  CHECK(!b.cancel(1));
  CHECK(!b.modify(1, 5));
}

CASE("rejects duplicate ids and non-positive quantities") {
  OrderBook b;
  CHECK(b.add(7, Side::Buy, 10, 1));
  CHECK(!b.add(7, Side::Sell, 20, 1));
  CHECK(!b.add(8, Side::Buy, 10, 0));
  CHECK(!b.add(9, Side::Buy, 10, -3));
  CHECK_EQ(b.order_count(), 1u);
  CHECK(!b.best_ask().has_value());
  CHECK(!b.modify(7, -1));
  CHECK_EQ(b.volume_at(Side::Buy, 10), Qty{1});
  CHECK(b.cancel(7));
  CHECK(b.add(7, Side::Sell, 20, 2));  // id is free again after cancel
  CHECK_EQ(b.best_ask(), Lvl(std::pair<Price, Qty>{20, 2}));
}

CASE("ask depth is ascending, levels disappear when emptied") {
  OrderBook b;
  b.add(1, Side::Sell, 105, 1);
  b.add(2, Side::Sell, 102, 2);
  b.add(3, Side::Sell, 104, 3);
  b.add(4, Side::Sell, 102, 4);
  CHECK_EQ(b.depth(Side::Sell, 2), (Levels{{102, 6}, {104, 3}}));
  CHECK_EQ(b.depth(Side::Sell, 10), (Levels{{102, 6}, {104, 3}, {105, 1}}));
  b.cancel(2);
  b.cancel(4);
  CHECK_EQ(b.best_ask(), Lvl(std::pair<Price, Qty>{104, 3}));
  CHECK_EQ(b.volume_at(Side::Sell, 102), Qty{0});
  CHECK(b.queue_at(Side::Sell, 102).empty());
  CHECK(b.depth(Side::Sell, 0).empty());
}

CASE("modify to zero cancels; sides are independent at the same price") {
  OrderBook b;
  b.add(1, Side::Buy, 100, 5);
  b.add(2, Side::Sell, 100, 6);  // crossed is allowed: no matching here
  CHECK_EQ(b.volume_at(Side::Buy, 100), Qty{5});
  CHECK_EQ(b.volume_at(Side::Sell, 100), Qty{6});
  CHECK(b.modify(1, 0));
  CHECK_EQ(b.order_count(), 1u);
  CHECK(!b.best_bid().has_value());
  CHECK(!b.cancel(1));
  CHECK_EQ(b.best_ask(), Lvl(std::pair<Price, Qty>{100, 6}));
}

CASE("modify to the same quantity keeps priority; negative prices work") {
  OrderBook b;
  b.add(1, Side::Buy, -5, 3);
  b.add(2, Side::Buy, -5, 3);
  b.add(3, Side::Buy, -7, 1);
  CHECK(b.modify(1, 3));
  CHECK_EQ(b.queue_at(Side::Buy, -5), (std::vector<OrderId>{1, 2}));
  CHECK_EQ(b.best_bid(), Lvl(std::pair<Price, Qty>{-5, 6}));
  CHECK(b.modify(2, 10));
  CHECK(b.modify(1, 1));
  CHECK_EQ(b.queue_at(Side::Buy, -5), (std::vector<OrderId>{1, 2}));
  CHECK_EQ(b.depth(Side::Buy, 2), (Levels{{-5, 11}, {-7, 1}}));
}

// Simple oracle: a flat list of orders with an arrival sequence number.
struct Oracle {
  struct O { OrderId id; Side side; Price price; Qty qty; long seq; };
  std::vector<O> v;
  long seq = 0;
  O* find(OrderId id) { for (auto& o : v) if (o.id == id) return &o; return nullptr; }
  void erase(OrderId id) { v.erase(std::remove_if(v.begin(), v.end(), [&](const O& o) { return o.id == id; }), v.end()); }
  bool add(OrderId id, Side s, Price p, Qty q) { if (q <= 0 || find(id)) return false; v.push_back({id, s, p, q, seq++}); return true; }
  bool cancel(OrderId id) { if (!find(id)) return false; erase(id); return true; }
  bool modify(OrderId id, Qty q) {
    O* o = find(id);
    if (!o || q < 0) return false;
    if (q == 0) erase(id);
    else if (q <= o->qty) o->qty = q;
    else { o->qty = q; o->seq = seq++; }
    return true;
  }
  Levels depth(Side s, std::size_t n) const {
    std::map<Price, Qty> m;
    for (auto& o : v) if (o.side == s) m[o.price] += o.qty;
    Levels out(m.begin(), m.end());
    if (s == Side::Buy) std::reverse(out.begin(), out.end());
    if (out.size() > n) out.resize(n);
    return out;
  }
  std::vector<OrderId> queue(Side s, Price p) const {
    std::vector<O> q;
    for (auto& o : v) if (o.side == s && o.price == p) q.push_back(o);
    std::sort(q.begin(), q.end(), [](const O& a, const O& b) { return a.seq < b.seq; });
    std::vector<OrderId> ids;
    for (auto& o : q) ids.push_back(o.id);
    return ids;
  }
};

CASE("20000 random operations match a brute-force oracle") {
  std::mt19937_64 rng(12345);
  OrderBook b;
  Oracle o;
  auto rnd = [&](long lo, long hi) { return std::uniform_int_distribution<long>(lo, hi)(rng); };
  for (int step = 0; step < 20000; ++step) {
    long op = rnd(0, 9);
    OrderId id = rnd(1, 300);
    if (op < 5) {
      Side s = rnd(0, 1) ? Side::Buy : Side::Sell;
      Price p = rnd(90, 110);
      Qty q = rnd(-1, 20);
      CHECK_EQ(b.add(id, s, p, q), o.add(id, s, p, q));
    } else if (op < 7) {
      CHECK_EQ(b.cancel(id), o.cancel(id));
    } else {
      Qty q = rnd(-1, 25);
      CHECK_EQ(b.modify(id, q), o.modify(id, q));
    }
    CHECK_EQ(b.order_count(), o.v.size());
    auto bd = o.depth(Side::Buy, 1), ad = o.depth(Side::Sell, 1);
    CHECK_EQ(b.best_bid(), bd.empty() ? Lvl() : Lvl(bd[0]));
    CHECK_EQ(b.best_ask(), ad.empty() ? Lvl() : Lvl(ad[0]));
    if (step % 10 == 0) {
      std::size_t n = rnd(0, 6);
      CHECK_EQ(b.depth(Side::Buy, n), o.depth(Side::Buy, n));
      CHECK_EQ(b.depth(Side::Sell, n), o.depth(Side::Sell, n));
      Side s = rnd(0, 1) ? Side::Buy : Side::Sell;
      Price p = rnd(90, 110);
      CHECK_EQ(b.queue_at(s, p), o.queue(s, p));
      Qty vol = 0;
      for (auto& x : o.v) if (x.side == s && x.price == p) vol += x.qty;
      CHECK_EQ(b.volume_at(s, p), vol);
    }
  }
}

CASE("200000 orders over 100000 sparse price levels stay fast") {
  OrderBook b;
  const long N = 200000;
  for (long i = 0; i < N; ++i) {
    Side s = i % 2 ? Side::Sell : Side::Buy;
    Price p = s == Side::Buy ? 1000000 - (i * 7919) % 100000 * 1000 : 1000000000 + (i * 104729) % 100000 * 1000;
    CHECK(b.add(i, s, p, 1 + i % 5));
  }
  CHECK_EQ(b.order_count(), static_cast<std::size_t>(N));
  for (long i = 0; i < N; i += 2) CHECK(b.modify(i, 1));
  for (long i = 0; i < N; ++i) CHECK(b.cancel(i));
  CHECK_EQ(b.order_count(), 0u);
  CHECK(!b.best_bid().has_value());
  CHECK(!b.best_ask().has_value());
}
