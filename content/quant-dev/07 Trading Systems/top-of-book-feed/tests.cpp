#include "qtest.h"
#include "attempt.cpp"
#include <map>
#include <ostream>
#include <random>

using Lvl = std::optional<std::pair<std::int64_t, std::int64_t>>;
using Sp = std::optional<std::int64_t>;

std::ostream& operator<<(std::ostream& o, const Quote& q) {
  o << "{bid ";
  if (q.bid) o << q.bid->first << "x" << q.bid->second; else o << "none";
  o << ", ask ";
  if (q.ask) o << q.ask->first << "x" << q.ask->second; else o << "none";
  o << ", spread ";
  if (q.spread) o << *q.spread; else o << "none";
  return o << ", crossed " << (q.crossed ? "true" : "false") << "}";
}

static Lvl L(std::int64_t p, std::int64_t q) { return std::pair<std::int64_t, std::int64_t>{p, q}; }
static Quote Q(Lvl bid, Lvl ask, Sp spread, bool crossed) { return Quote{bid, ask, spread, crossed}; }

EXAMPLE("Example 1: building the book, replacing and removing levels") {
  TopOfBook b;
  CHECK_EQ(b.apply(Side::Bid, 100, 5), Q(L(100, 5), {}, {}, false));
  CHECK_EQ(b.apply(Side::Ask, 103, 2), Q(L(100, 5), L(103, 2), 3, false));
  CHECK_EQ(b.apply(Side::Bid, 101, 1), Q(L(101, 1), L(103, 2), 2, false));
  CHECK_NEAR(b.mid().value_or(-1), 102.0, 1e-12);
  CHECK_EQ(b.apply(Side::Bid, 101, 0), Q(L(100, 5), L(103, 2), 3, false));
  CHECK_EQ(b.apply(Side::Ask, 103, 9), Q(L(100, 5), L(103, 9), 3, false));
}

EXAMPLE("Example 2: a locked book is flagged, negative qty throws") {
  TopOfBook b;
  b.apply(Side::Ask, 50, 1);
  CHECK_EQ(b.apply(Side::Bid, 50, 4), Q(L(50, 4), L(50, 1), 0, true));
  CHECK_EQ(b.apply(Side::Ask, 50, 0), Q(L(50, 4), {}, {}, false));
  CHECK_THROWS(b.apply(Side::Bid, 49, -1));
}

CASE("empty book") {
  TopOfBook b;
  CHECK_EQ(b.quote(), Q({}, {}, {}, false));
  CHECK(!b.mid().has_value());
  CHECK_EQ(b.apply(Side::Ask, 10, 0), Q({}, {}, {}, false));  // removing a missing level is a no-op
}

CASE("strictly crossed book has a negative spread") {
  TopOfBook b;
  b.apply(Side::Bid, 105, 1);
  CHECK_EQ(b.apply(Side::Ask, 102, 3), Q(L(105, 1), L(102, 3), -3, true));
  CHECK_NEAR(b.mid().value_or(-1), 103.5, 1e-12);
  CHECK_EQ(b.apply(Side::Bid, 105, 0), Q({}, L(102, 3), {}, false));
}

CASE("negative quantity leaves the book unchanged") {
  TopOfBook b;
  b.apply(Side::Bid, 10, 1);
  b.apply(Side::Ask, 12, 1);
  bool threw = false;
  try { b.apply(Side::Ask, 11, -5); } catch (const std::invalid_argument&) { threw = true; }
  CHECK(threw);
  CHECK_EQ(b.quote(), Q(L(10, 1), L(12, 1), 2, false));
}

CASE("worse levels don't change the top until the top is removed") {
  TopOfBook b;
  b.apply(Side::Ask, 200, 1);
  b.apply(Side::Ask, 205, 2);
  b.apply(Side::Ask, 201, 3);
  b.apply(Side::Bid, 190, 4);
  b.apply(Side::Bid, 180, 5);
  CHECK_EQ(b.quote(), Q(L(190, 4), L(200, 1), 10, false));
  CHECK_EQ(b.apply(Side::Ask, 200, 0), Q(L(190, 4), L(201, 3), 11, false));
  CHECK_EQ(b.apply(Side::Bid, 190, 0), Q(L(180, 5), L(201, 3), 21, false));
  CHECK_EQ(b.apply(Side::Ask, 201, 0), Q(L(180, 5), L(205, 2), 25, false));
}

CASE("mid uses doubles and works for negative and large prices") {
  TopOfBook b;
  b.apply(Side::Bid, -3, 1);
  b.apply(Side::Ask, 0, 1);
  CHECK_NEAR(b.mid().value_or(1), -1.5, 1e-12);
  TopOfBook big;
  big.apply(Side::Bid, 4000000000000000000LL, 1);
  big.apply(Side::Ask, 4000000000000000002LL, 1);
  CHECK_EQ(big.quote().spread, Sp(2));
  CHECK_NEAR(big.mid().value_or(0), 4000000000000000001.0, 1024.0);
}

CASE("random updates match a brute-force rebuild") {
  std::mt19937_64 rng(8);
  auto rnd = [&](long lo, long hi) { return std::uniform_int_distribution<long>(lo, hi)(rng); };
  TopOfBook b;
  std::map<std::int64_t, std::int64_t> bids, asks;
  for (int i = 0; i < 20000; ++i) {
    Side s = rnd(0, 1) ? Side::Bid : Side::Ask;
    std::int64_t p = rnd(90, 110), q = rnd(0, 3) == 0 ? 0 : rnd(1, 100);
    auto& m = s == Side::Bid ? bids : asks;
    if (q == 0) m.erase(p); else m[p] = q;
    Quote e;
    if (!bids.empty()) e.bid = *bids.rbegin();
    if (!asks.empty()) e.ask = *asks.begin();
    if (e.bid && e.ask) { e.spread = e.ask->first - e.bid->first; e.crossed = e.bid->first >= e.ask->first; }
    CHECK_EQ(b.apply(s, p, q), e);
    if (e.bid && e.ask) CHECK_NEAR(b.mid().value_or(-1), (e.bid->first + e.ask->first) / 2.0, 1e-12);
    else CHECK(!b.mid().has_value());
  }
}

CASE("a million updates over 100000 levels stay fast") {
  TopOfBook b;
  for (std::int64_t i = 0; i < 1000000; ++i) {
    std::int64_t lvl = (i * 7919) % 100000;
    b.apply(i % 2 ? Side::Ask : Side::Bid, i % 2 ? 1000000 + lvl : 999999 - lvl, i % 10);
  }
  Quote q = b.quote();
  CHECK(q.bid.has_value() && q.ask.has_value());
  CHECK(!q.crossed);
}
