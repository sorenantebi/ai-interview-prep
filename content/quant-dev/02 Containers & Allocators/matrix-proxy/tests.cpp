#include "qtest.h"
#include "attempt.cpp"
#include <stdexcept>

EXAMPLE("Example 1: write, update and read through the row proxy") {
  Matrix m(2, 3);
  m[1][2] = 4.5;
  m[1][2] += 0.5;
  CHECK_EQ(m[1][2], 5.0);
  CHECK_EQ(m[0][0], 0.0);
  CHECK_EQ(m.rows(), 2u);
  CHECK_EQ(m.cols(), 3u);
}

EXAMPLE("Example 2: const access and bounds checks") {
  Matrix m(2, 3);
  m[1][2] = 5.0;
  const Matrix& cm = m;
  CHECK_EQ(cm[1][2], 5.0);
  CHECK_THROWS(m[2][0]);
  CHECK_THROWS(m[0][3]);
}

CASE("new matrix is all zeros") {
  Matrix m(4, 5);
  for (std::size_t r = 0; r < 4; ++r)
    for (std::size_t c = 0; c < 5; ++c) CHECK_EQ(m[r][c], 0.0);
}

CASE("out-of-range indices throw std::out_of_range specifically") {
  Matrix m(3, 2);
  const Matrix& cm = m;
  auto throws_oor = [](auto f) {
    try { f(); } catch (const std::out_of_range&) { return true; } catch (...) { return false; }
    return false;
  };
  CHECK(throws_oor([&] { m[3]; }));
  CHECK(throws_oor([&] { m[0][2]; }));
  CHECK(throws_oor([&] { cm[100][0]; }));
  CHECK(throws_oor([&] { cm[2][2]; }));
  CHECK(!throws_oor([&] { m[2][1] = 1.0; }));
}

CASE("empty dimensions: every index is out of range") {
  Matrix a(0, 5), b(5, 0);
  CHECK_EQ(a.rows(), 0u);
  CHECK_THROWS(a[0]);
  CHECK_THROWS(b[0][0]);
  CHECK_EQ(b.cols(), 0u);
}

CASE("1x1 matrix") {
  Matrix m(1, 1);
  m[0][0] = -3.25;
  CHECK_EQ(m[0][0], -3.25);
  CHECK_THROWS(m[0][1]);
  CHECK_THROWS(m[1][0]);
}

CASE("row-major contiguous layout") {
  Matrix m(3, 4);
  double* base = &m[0][0];
  for (std::size_t r = 0; r < 3; ++r)
    for (std::size_t c = 0; c < 4; ++c) CHECK(&m[r][c] == base + r * 4 + c);
}

CASE("proxy references alias the matrix storage") {
  Matrix m(2, 2);
  auto row = m[1];
  row[0] = 7.0;
  CHECK_EQ(m[1][0], 7.0);
  double& ref = m[0][1];
  ref = 2.0;
  const Matrix& cm = m;
  CHECK_EQ(cm[0][1], 2.0);
  CHECK(&cm[0][1] == &ref);
}

CASE("copies are independent") {
  Matrix a(2, 2);
  a[0][0] = 1.0;
  Matrix b = a;
  b[0][0] = 2.0;
  CHECK_EQ(a[0][0], 1.0);
  CHECK_EQ(b[0][0], 2.0);
  a = b;
  CHECK_EQ(a[0][0], 2.0);
}

CASE("non-square 300x700 fill and sum") {
  Matrix m(300, 700);
  for (std::size_t r = 0; r < 300; ++r)
    for (std::size_t c = 0; c < 700; ++c) m[r][c] = static_cast<double>(r * 700 + c);
  double sum = 0;
  for (std::size_t r = 0; r < 300; ++r)
    for (std::size_t c = 0; c < 700; ++c) sum += m[r][c];
  const double n = 300.0 * 700.0;
  CHECK_NEAR(sum, (n - 1) * n / 2, 1e-3);
  CHECK_EQ(m[299][699], n - 1);
}
