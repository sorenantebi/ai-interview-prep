#include "qtest.h"
#include "attempt.cpp"
#include <numbers>
#include <type_traits>
#include <vector>

constexpr double PI = 3.14159265358979323846;

EXAMPLE("Example 1: area and total_area") {
  Circle c(1.0);
  Rectangle r(2.0, 3.0);
  CHECK_NEAR(c.area(), PI, 1e-12);
  CHECK_NEAR(r.area(), 6.0, 1e-12);
  CHECK_NEAR(total_area(std::tuple{c, r}), PI + 6.0, 1e-12);
}

EXAMPLE("Example 2: per-type live counts") {
  int before = Circle::live_count();
  int rect_before = Rectangle::live_count();
  {
    Circle a(1), b(2);
    Circle copy = a;
    CHECK_EQ(Circle::live_count() - before, 3);
    CHECK_EQ(Rectangle::live_count(), rect_before);
  }
  CHECK_EQ(Circle::live_count() - before, 0);
}

struct Triangle : Shape<Triangle> {
  Triangle(double b, double h) : b(b), h(h) {}
  double area_impl() const { return 0.5 * b * h; }
  double b, h;
};

CASE("no virtual dispatch and no size overhead") {
  CHECK(!std::is_polymorphic_v<Circle>);
  CHECK(!std::is_polymorphic_v<Rectangle>);
  CHECK_EQ(sizeof(Circle), sizeof(double));
  CHECK_EQ(sizeof(Rectangle), 2 * sizeof(double));
}

CASE("a user-defined shape plugs into the base") {
  Triangle t(4.0, 3.0);
  CHECK_NEAR(t.area(), 6.0, 1e-12);
  CHECK_EQ(Triangle::live_count(), 1);
}

CASE("area through a const base reference") {
  const Circle c(2.0);
  const Shape<Circle>& base = c;
  CHECK_NEAR(base.area(), 4.0 * PI, 1e-12);
  Rectangle r(0.0, 5.0);
  CHECK_NEAR(r.area(), 0.0, 1e-12);
}

CASE("total_area over many types, one type and the empty tuple") {
  auto shapes = std::tuple{Circle(1.0), Rectangle(1.0, 2.0), Triangle(2.0, 2.0), Circle(2.0)};
  CHECK_NEAR(total_area(shapes), PI + 2.0 + 2.0 + 4.0 * PI, 1e-9);
  CHECK_NEAR(total_area(std::tuple{Rectangle(3.0, 3.0)}), 9.0, 1e-12);
  CHECK_NEAR(total_area(std::tuple<>{}), 0.0, 1e-12);
}

CASE("copies, moves and vector storage keep counts exact") {
  int base = Rectangle::live_count();
  {
    std::vector<Rectangle> v;
    v.reserve(10);
    for (int i = 0; i < 10; ++i) v.emplace_back(i, 1.0);
    CHECK_EQ(Rectangle::live_count() - base, 10);
    Rectangle moved = std::move(v[0]);
    CHECK_EQ(Rectangle::live_count() - base, 11);
    v.clear();
    CHECK_EQ(Rectangle::live_count() - base, 1);
  }
  CHECK_EQ(Rectangle::live_count() - base, 0);
}

CASE("assignment doesn't change the count") {
  int base = Circle::live_count();
  Circle a(1.0), b(3.0);
  a = b;
  CHECK_EQ(Circle::live_count() - base, 2);
  CHECK_NEAR(a.area(), 9.0 * PI, 1e-12);
}

CASE("counters are independent per type") {
  int c0 = Circle::live_count(), r0 = Rectangle::live_count(), t0 = Triangle::live_count();
  {
    Triangle t1(1, 1), t2(1, 1);
    Circle c(1);
    CHECK_EQ(Triangle::live_count() - t0, 2);
    CHECK_EQ(Circle::live_count() - c0, 1);
    CHECK_EQ(Rectangle::live_count() - r0, 0);
  }
  CHECK_EQ(Triangle::live_count(), t0);
  CHECK_EQ(Circle::live_count(), c0);
}
