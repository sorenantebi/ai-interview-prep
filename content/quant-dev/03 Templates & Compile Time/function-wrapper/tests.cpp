#include "qtest.h"
#include "attempt.cpp"
#include <functional>
#include <string>
#include <utility>
#include <vector>

struct Probe {
  static inline int ctors = 0, dtors = 0;
  static int alive() { return ctors - dtors; }
  Probe() { ++ctors; }
  Probe(const Probe&) { ++ctors; }
  Probe(Probe&&) noexcept { ++ctors; }
  ~Probe() { ++dtors; }
};

static int triple(int x) { return 3 * x; }

EXAMPLE("Example 1: lambda and function pointer") {
  Function<int(int, int)> add = [](int a, int b) { return a + b; };
  CHECK_EQ(add(2, 3), 5);
  int (*fp)(int, int) = [](int a, int b) { return a * b; };
  Function<int(int, int)> mul = fp;
  CHECK_EQ(mul(4, 5), 20);
}

EXAMPLE("Example 2: copies keep independent state; empty throws") {
  Function<int()> counter = [n = 0]() mutable { return ++n; };
  CHECK_EQ(counter(), 1);
  Function<int()> copy = counter;
  CHECK_EQ(counter(), 2);
  CHECK_EQ(copy(), 2);
  Function<void()> empty;
  CHECK(!static_cast<bool>(empty));
  CHECK_THROWS(empty());
}

struct Scale {
  double k;
  double operator()(double x) const { return k * x; }
};

CASE("functor objects and plain functions") {
  Function<double(double)> f = Scale{2.5};
  CHECK_NEAR(f(4.0), 10.0, 1e-12);
  Function<int(int)> g = triple;
  CHECK_EQ(g(7), 21);
  Function<int(int)> h = &triple;
  CHECK_EQ(h(-2), -6);
  CHECK(static_cast<bool>(g));
}

CASE("empty states: default, nullptr, moved-from") {
  Function<int(int)> a;
  Function<int(int)> b = nullptr;
  CHECK(!a);
  CHECK(!b);
  bool threw = false;
  try { b(1); } catch (const std::bad_function_call&) { threw = true; }
  CHECK(threw);
  Function<int(int)> c = triple;
  Function<int(int)> d = std::move(c);
  CHECK(!c);
  CHECK_EQ(d(2), 6);
  CHECK_THROWS(c(2));
}

CASE("copying a non-const Function copies, doesn't nest") {
  Function<std::string(std::string)> up = [](std::string s) { return s + "!"; };
  Function<std::string(std::string)> a = up;   // non-const lvalue
  Function<std::string(std::string)> b(a);
  CHECK_EQ(b("fill"), std::string("fill!"));
  a = nullptr;
  CHECK(!a);
  CHECK_EQ(up("x"), std::string("x!"));
}

CASE("reference parameters reach the caller's object") {
  Function<void(int&)> inc = [](int& x) { ++x; };
  int v = 41;
  inc(v);
  CHECK_EQ(v, 42);
  Function<void(std::vector<int>&, int)> push = [](std::vector<int>& vec, int x) { vec.push_back(x); };
  std::vector<int> book;
  push(book, 1);
  push(book, 2);
  CHECK_EQ(book.size(), 2u);
}

CASE("assignment: copy, move, self and reassign to another callable") {
  Function<int(int)> f = [](int x) { return x + 1; };
  Function<int(int)> g = [k = 10](int x) { return x * k; };
  f = g;
  CHECK_EQ(f(3), 30);
  f = f;
  CHECK_EQ(f(4), 40);
  Function<int(int)> h;
  h = std::move(f);
  CHECK_EQ(h(5), 50);
  CHECK(!f);
  h = [](int x) { return -x; };
  CHECK_EQ(h(5), -5);
  CHECK_EQ(g(1), 10);
}

CASE("captured state is destroyed exactly once") {
  {
    Probe p;
    Function<int()> f = [p] { return 1; };
    Function<int()> g = f;
    Function<int()> h = std::move(g);
    Function<int()> i;
    i = h;
    i = f;
    f = nullptr;
    CHECK_EQ(h() + i(), 2);
  }
  CHECK_EQ(Probe::alive(), 0);
}

CASE("recursive Function and a vector of callbacks") {
  Function<long long(int)> fact;
  fact = [&fact](int n) -> long long { return n <= 1 ? 1 : n * fact(n - 1); };
  CHECK_EQ(fact(15), 1307674368000LL);

  std::vector<Function<void(std::string&)>> handlers;
  handlers.push_back([](std::string& s) { s += "a"; });
  handlers.push_back([tag = std::string("b")](std::string& s) { s += tag; });
  handlers.emplace_back([](std::string& s) { s += "c"; });
  for (int i = 0; i < 100; ++i) handlers.push_back(handlers[i % 3]);  // reallocations copy/move
  std::string out;
  for (auto& h : handlers) h(out);
  CHECK_EQ(out.size(), 103u);
  CHECK_EQ(out.substr(0, 6), std::string("abcabc"));
}
