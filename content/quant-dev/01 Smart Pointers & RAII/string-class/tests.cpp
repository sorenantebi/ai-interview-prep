#include "qtest.h"
#include "attempt.cpp"
#include <atomic>
#include <cstdlib>
#include <new>
#include <string>
#include <vector>

// Count heap allocations: live blocks (for leaks) and total calls (for "moves don't allocate").
static std::atomic<long> g_live{0}, g_news{0};
void* operator new(std::size_t n) {
  void* p = std::malloc(n ? n : 1);
  if (!p) throw std::bad_alloc();
  ++g_live;
  ++g_news;
  return p;
}
void operator delete(void* p) noexcept {
  if (!p) return;
  --g_live;
  std::free(p);
}
void operator delete(void* p, std::size_t) noexcept { operator delete(p); }

static std::string str(const String& s) { return std::string(s.c_str()); }

EXAMPLE("Example 1: deep copy, append, size, equality") {
  String a("BUY");
  String b = a;
  b += " 100 AAPL";
  CHECK_EQ(str(a), std::string("BUY"));
  CHECK_EQ(str(b), std::string("BUY 100 AAPL"));
  CHECK_EQ(b.size(), 12u);
  CHECK(a == String("BUY"));
}

EXAMPLE("Example 2: self-append, move, moved-from is valid, copy assignment") {
  String s("ab");
  s += s;
  CHECK_EQ(str(s), std::string("abab"));
  String t = std::move(s);
  CHECK_EQ(str(t), std::string("abab"));
  CHECK_EQ(s.size(), 0u);
  CHECK(s.c_str() != nullptr);
  CHECK_EQ(str(s), std::string(""));
  s = t;
  CHECK(s == t);
}

CASE("empty strings") {
  String a;
  String b("");
  CHECK_EQ(a.size(), 0u);
  CHECK(a.c_str() != nullptr);
  CHECK_EQ(a.c_str()[0], '\0');
  CHECK(a == b);
  a += b;
  CHECK_EQ(a.size(), 0u);
  b += "x";
  CHECK(!(a == b));
  CHECK_EQ(str(b), std::string("x"));
}

CASE("copies are deep: changing one doesn't affect the other") {
  String a("abc");
  String b(a);
  String c;
  c = a;
  a += "def";
  CHECK_EQ(str(a), std::string("abcdef"));
  CHECK_EQ(str(b), std::string("abc"));
  CHECK_EQ(str(c), std::string("abc"));
  CHECK(b.c_str() != a.c_str());
}

CASE("self copy- and move-assignment are safe") {
  String a("hello");
  String& alias = a;
  a = alias;
  CHECK_EQ(str(a), std::string("hello"));
  a = std::move(alias);
  CHECK_EQ(str(a), std::string("hello"));
  CHECK_EQ(a.size(), 5u);
}

CASE("equality compares contents, not pointers or prefixes") {
  CHECK(String("abc") == String("abc"));
  CHECK(!(String("abc") == String("abd")));
  CHECK(!(String("abc") == String("ab")));
  CHECK(!(String("ab") == String("abc")));
  CHECK(String("x") == "x");
}

CASE("moves do not allocate") {
  String a("a fairly long string that certainly lives on the heap");
  long before = g_news.load();
  String b(std::move(a));
  String c;
  c = std::move(b);
  CHECK_EQ(g_news.load(), before);
  CHECK_EQ(str(c), std::string("a fairly long string that certainly lives on the heap"));
  CHECK_EQ(a.size(), 0u);
  CHECK_EQ(b.size(), 0u);
}

CASE("no leaks across copies, moves, assignments and appends") {
  long before = g_live.load();
  {
    String a("x");
    for (int i = 0; i < 10; ++i) a += a;  // 1024 chars, many reallocations
    CHECK_EQ(a.size(), 1024u);
    String b = a, c("y");
    c = b;
    b = std::move(c);
    c = String("z");
    c = a;
    std::vector<String> v;
    for (int i = 0; i < 100; ++i) v.push_back(String("item"));
    v.erase(v.begin(), v.begin() + 50);
  }
  CHECK_EQ(g_live.load(), before);
}

CASE("repeated self-append doubles correctly") {
  String s("ab");
  std::string expect = "ab";
  for (int i = 0; i < 12; ++i) {
    s += s;
    expect += expect;
    CHECK_EQ(s.size(), expect.size());
  }
  CHECK_EQ(str(s), expect);
}

CASE("100000 single-char appends: geometric growth, few allocations") {
  String s;
  std::string expect;
  long before = g_news.load();
  for (int i = 0; i < 100000; ++i) {
    char c[2] = {char('a' + i % 26), '\0'};
    String piece(c);
    s += piece;
  }
  // 100000 allocations for the temporary pieces; the String itself may add only a handful.
  CHECK(g_news.load() - before <= 100000 + 64);
  for (int i = 0; i < 100000; ++i) expect += char('a' + i % 26);
  CHECK_EQ(s.size(), 100000u);
  CHECK_EQ(str(s), expect);
}
