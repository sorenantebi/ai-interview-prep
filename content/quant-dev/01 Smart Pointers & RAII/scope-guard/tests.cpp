#include "qtest.h"
#include "attempt.cpp"
#include <functional>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

EXAMPLE("Example 1: runs at scope exit, dismiss cancels it") {
  int undo = 0;
  {
    ScopeGuard g([&] { ++undo; });
  }
  CHECK_EQ(undo, 1);
  {
    auto g = make_scope_guard([&] { ++undo; });
    g.dismiss();
  }
  CHECK_EQ(undo, 1);
}

EXAMPLE("Example 2: runs during exception unwinding") {
  std::vector<std::string> log;
  try {
    ScopeGuard g([&] { log.push_back("rollback"); });
    throw std::runtime_error("venue rejected");
  } catch (const std::exception&) {
  }
  CHECK_EQ(log, std::vector<std::string>{"rollback"});
}

CASE("does not run before the scope ends") {
  int n = 0;
  {
    ScopeGuard g([&] { ++n; });
    CHECK_EQ(n, 0);
  }
  CHECK_EQ(n, 1);
}

CASE("guards run in reverse order of construction") {
  std::string order;
  {
    ScopeGuard a([&] { order += 'a'; });
    ScopeGuard b([&] { order += 'b'; });
    ScopeGuard c([&] { order += 'c'; });
  }
  CHECK_EQ(order, std::string("cba"));
}

CASE("moved-from guard does not run, the new one runs once") {
  int n = 0;
  {
    auto g1 = make_scope_guard([&] { ++n; });
    {
      ScopeGuard g2(std::move(g1));
      CHECK_EQ(n, 0);
    }
    CHECK_EQ(n, 1);
  }
  CHECK_EQ(n, 1);
}

CASE("moving a dismissed guard keeps it dismissed") {
  int n = 0;
  {
    ScopeGuard g1([&] { ++n; });
    g1.dismiss();
    ScopeGuard g2(std::move(g1));
  }
  CHECK_EQ(n, 0);
}

CASE("commit pattern: dismissed only when every step succeeds") {
  auto place = [](bool fail, int& reserved) {
    ++reserved;
    ScopeGuard undo([&] { --reserved; });
    if (fail) throw std::runtime_error("risk check failed");
    undo.dismiss();
  };
  int reserved = 0;
  place(false, reserved);
  CHECK_EQ(reserved, 1);
  CHECK_THROWS(place(true, reserved));
  CHECK_EQ(reserved, 1);
}

CASE("works with a function pointer and std::function") {
  static int calls = 0;
  calls = 0;
  {
    ScopeGuard<void (*)()> g(+[] { ++calls; });
    ScopeGuard<std::function<void()>> h(std::function<void()>([] { calls += 10; }));
  }
  CHECK_EQ(calls, 11);
}

CASE("guards stored in a vector run once each after reallocations") {
  int n = 0;
  {
    std::vector<ScopeGuard<std::function<void()>>> v;
    for (int i = 0; i < 100; ++i) v.emplace_back(std::function<void()>([&n] { ++n; }));
    CHECK_EQ(n, 0);
    v[5].dismiss();
  }
  CHECK_EQ(n, 99);
}

CASE("move-only") {
  using G = ScopeGuard<void (*)()>;
  CHECK(!std::is_copy_constructible_v<G>);
  CHECK(!std::is_copy_assignable_v<G>);
  CHECK(std::is_nothrow_move_constructible_v<G>);
}
