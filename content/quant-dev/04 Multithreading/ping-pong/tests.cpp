#include "qtest.h"
#include "attempt.cpp"
#include <sstream>
#include <string>
#include <vector>

static std::string expected(int n) {
  std::string s;
  for (int i = 0; i < n; ++i) s += (i ? " ping pong" : "ping pong");
  return s;
}

static bool alternates(const std::string& s, int n) {
  std::istringstream in(s);
  std::string w;
  int i = 0;
  while (in >> w) {
    if (w != (i % 2 == 0 ? "ping" : "pong")) return false;
    ++i;
  }
  return i == 2 * n;
}

EXAMPLE("Example 1: play(1)") {
  CHECK_EQ(play(1), std::string("ping pong"));
}

EXAMPLE("Example 2: play(3)") {
  CHECK_EQ(play(3), std::string("ping pong ping pong ping pong"));
}

EXAMPLE("Example 3: play(0)") {
  CHECK_EQ(play(0), std::string(""));
}

CASE("play(2)") {
  CHECK_EQ(play(2), std::string("ping pong ping pong"));
}

CASE("play(10) matches exactly") {
  CHECK_EQ(play(10), expected(10));
}

CASE("play(1000) strictly alternates") {
  std::string s = play(1000);
  CHECK(alternates(s, 1000));
  CHECK_EQ(s, expected(1000));
}

CASE("play(20000) strictly alternates") {
  CHECK(alternates(play(20000), 20000));
}

CASE("many short games in a row") {
  bool ok = true;
  for (int n = 0; n < 60; ++n) ok = ok && play(n) == expected(n);
  CHECK(ok);
}

CASE("repeated 3 times gives the same answer") {
  std::vector<std::string> runs;
  for (int r = 0; r < 3; ++r) runs.push_back(play(5000));
  CHECK(runs[0] == expected(5000));
  CHECK(runs[1] == runs[0]);
  CHECK(runs[2] == runs[0]);
}
