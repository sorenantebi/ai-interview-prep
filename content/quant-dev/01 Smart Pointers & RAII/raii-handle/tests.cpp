#include "qtest.h"
#include "attempt.cpp"
#include <type_traits>
#include <vector>

static std::vector<int> closed;  // ids passed to the fake close function, in order
void fake_close(int fd) { closed.push_back(fd); }
using FdHandle = Handle<void (*)(int)>;

EXAMPLE("Example 1: closes on scope exit") {
  closed.clear();
  {
    FdHandle h(3, fake_close);
    CHECK_EQ(h.get(), 3);
    CHECK(h.valid());
    CHECK(closed.empty());
  }
  CHECK_EQ(closed, std::vector<int>{3});
}

EXAMPLE("Example 2: move assignment closes the old resource") {
  closed.clear();
  FdHandle a(4, fake_close);
  FdHandle b(5, fake_close);
  a = std::move(b);
  CHECK_EQ(closed, std::vector<int>{4});
  CHECK(!b.valid());
  CHECK_EQ(a.get(), 5);
  a.reset();
  CHECK_EQ(closed, (std::vector<int>{4, 5}));
}

CASE("an invalid handle never calls the closer") {
  closed.clear();
  {
    FdHandle h(-1, fake_close);
    CHECK(!h.valid());
    CHECK_EQ(h.get(), -1);
    h.reset();
  }
  CHECK(closed.empty());
}

CASE("move construction transfers ownership, closes once") {
  closed.clear();
  {
    FdHandle a(7, fake_close);
    FdHandle b(std::move(a));
    CHECK(!a.valid());
    CHECK_EQ(b.get(), 7);
  }
  CHECK_EQ(closed, std::vector<int>{7});
}

CASE("self move-assignment changes nothing") {
  closed.clear();
  {
    FdHandle a(8, fake_close);
    FdHandle& alias = a;
    a = std::move(alias);
    CHECK_EQ(a.get(), 8);
    CHECK(closed.empty());
  }
  CHECK_EQ(closed, std::vector<int>{8});
}

CASE("release gives up ownership without closing") {
  closed.clear();
  int id;
  {
    FdHandle h(9, fake_close);
    id = h.release();
    CHECK(!h.valid());
  }
  CHECK_EQ(id, 9);
  CHECK(closed.empty());
}

CASE("reset closes the old id and owns the new one") {
  closed.clear();
  {
    FdHandle h(10, fake_close);
    h.reset(11);
    CHECK_EQ(h.get(), 11);
    h.reset(12);
  }
  CHECK_EQ(closed, (std::vector<int>{10, 11, 12}));
}

CASE("works with a capturing lambda as the closer") {
  int count = 0, last = 0;
  auto closer = [&](int fd) { ++count; last = fd; };
  {
    Handle<decltype(closer)> a(20, closer);
    Handle<decltype(closer)> b(std::move(a));
    CHECK_EQ(count, 0);
  }
  CHECK_EQ(count, 1);
  CHECK_EQ(last, 20);
}

CASE("move assignment with a captureless lambda type") {
  closed.clear();
  auto closer = [](int fd) { closed.push_back(fd * 100); };
  Handle<decltype(closer)> a(1, closer), b(2, closer);
  a = std::move(b);
  a = Handle<decltype(closer)>(3, closer);
  CHECK_EQ(closed, (std::vector<int>{100, 200}));
}

CASE("a vector of 500 handles closes each id exactly once") {
  closed.clear();
  {
    std::vector<FdHandle> v;
    for (int i = 0; i < 500; ++i) v.emplace_back(i, fake_close);
    CHECK(closed.empty());
  }
  CHECK_EQ(closed.size(), 500u);
  std::vector<int> seen(500, 0);
  for (int fd : closed) seen[fd]++;
  for (int c : seen) CHECK_EQ(c, 1);
}

CASE("rule of five: move-only") {
  CHECK(!std::is_copy_constructible_v<FdHandle>);
  CHECK(!std::is_copy_assignable_v<FdHandle>);
  CHECK(std::is_nothrow_move_constructible_v<FdHandle>);
  CHECK(std::is_nothrow_move_assignable_v<FdHandle>);
}
