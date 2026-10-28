// Tiny test runner for the C++ problems (Quant Dev). A problem's tests.cpp is:
//   #include "qtest.h"
//   #include "attempt.cpp"
//   EXAMPLE("pushes then pops") { RingBuffer<int> r(2); r.push(1); CHECK_EQ(r.pop(), 1); }
//   CASE("wraps around") { ... }
// `./tests` runs every case (Submit); `./tests --examples` only the EXAMPLE ones, with details (Run).
// Prints "PASS case N" / "FAIL case N (name): why" lines and "X/Y passed", like the Python tests
// (with --examples: "PASS <name>" / "FAIL <name><TAB>why").
#pragma once
#include <cmath>
#include <cstdio>
#include <cstring>
#include <exception>
#include <functional>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace qtest {
struct Failure { std::string msg; };
struct Case { const char* name; bool example; void (*fn)(); };
inline std::vector<Case>& cases() { static std::vector<Case> c; return c; }
struct Reg { Reg(const char* name, bool example, void (*fn)()) { cases().push_back({name, example, fn}); } };

template <class T> std::string show(const T& v) {
  if constexpr (requires(std::ostream& o) { o << v; }) {
    std::ostringstream s;
    s << std::boolalpha << v;
    return s.str();
  } else if constexpr (requires { v.begin(); v.end(); }) {
    std::string out = "[";
    for (auto it = v.begin(); it != v.end(); ++it) out += (it == v.begin() ? "" : ", ") + show(*it);
    return out + "]";
  } else if constexpr (requires { v.first; v.second; }) {
    return "(" + show(v.first) + ", " + show(v.second) + ")";
  } else {
    return "<value>";
  }
}
inline std::string at(int line) { return " (tests.cpp line " + std::to_string(line) + ")"; }
}  // namespace qtest

#define QT_CAT2(a, b) a##b
#define QT_CAT(a, b) QT_CAT2(a, b)
#define QT_DEFINE(name, example)                                                      \
  static void QT_CAT(qt_case_, __LINE__)();                                           \
  static qtest::Reg QT_CAT(qt_reg_, __LINE__)(name, example, QT_CAT(qt_case_, __LINE__)); \
  static void QT_CAT(qt_case_, __LINE__)()
#define CASE(name) QT_DEFINE(name, false)
#define EXAMPLE(name) QT_DEFINE(name, true)

#define CHECK(cond) \
  do { if (!(cond)) throw qtest::Failure{"CHECK(" #cond ") failed" + qtest::at(__LINE__)}; } while (0)
#define CHECK_EQ(got, expected)                                                                   \
  do {                                                                                            \
    auto&& qt_g = (got); auto&& qt_e = (expected);                                                \
    if (!(qt_g == qt_e))                                                                          \
      throw qtest::Failure{#got ": got " + qtest::show(qt_g) + ", expected " + qtest::show(qt_e) + qtest::at(__LINE__)}; \
  } while (0)
#define CHECK_NEAR(got, expected, eps)                                                            \
  do {                                                                                            \
    double qt_g = (got), qt_e = (expected);                                                       \
    if (!(std::fabs(qt_g - qt_e) <= (eps)))                                                       \
      throw qtest::Failure{#got ": got " + qtest::show(qt_g) + ", expected " + qtest::show(qt_e) + qtest::at(__LINE__)}; \
  } while (0)
#define CHECK_THROWS(expr)                                                                         \
  do {                                                                                             \
    bool qt_threw = false;                                                                         \
    try { (void)(expr); } catch (...) { qt_threw = true; }                                         \
    if (!qt_threw) throw qtest::Failure{#expr " should throw but didn't" + qtest::at(__LINE__)};   \
  } while (0)

int main(int argc, char** argv) {
  const bool examples = argc > 1 && !std::strcmp(argv[1], "--examples");
  int pass = 0, total = 0;
  for (auto& c : qtest::cases()) {
    if (examples && !c.example) continue;
    ++total;
    std::string why;
    try { c.fn(); } catch (const qtest::Failure& f) { why = f.msg; } catch (const std::exception& e) {
      why = std::string("threw an exception: ") + e.what();
    } catch (...) { why = "threw an exception"; }
    if (why.empty()) {
      ++pass;
      if (examples) std::printf("PASS %s\n", c.name); else std::printf("PASS case %d\n", total);
    } else if (examples) {
      std::printf("FAIL %s\t%s\n", c.name, why.c_str());  // a tab, since names may contain colons
    } else {
      std::printf("FAIL case %d (%s): %s\n", total, c.name, why.c_str());
    }
    std::fflush(stdout);
  }
  std::printf("%d/%d passed\n", pass, total);
  return pass == total ? 0 : 1;
}
