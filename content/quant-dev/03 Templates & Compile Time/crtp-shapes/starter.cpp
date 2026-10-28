#include <numbers>
#include <tuple>

template <class Derived>
class Shape {
public:
    double area() const { return 0.0; }
    static int live_count() { return 0; }

protected:
    Shape() {}
    Shape(const Shape&) {}
    Shape& operator=(const Shape&) { return *this; }
    ~Shape() {}
};

class Circle : public Shape<Circle> {
public:
    explicit Circle(double r) {}
    double area_impl() const { return 0.0; }
};

class Rectangle : public Shape<Rectangle> {
public:
    Rectangle(double w, double h) {}
    double area_impl() const { return 0.0; }
};

template <class... Shapes>
double total_area(const std::tuple<Shapes...>& shapes) {
    return 0.0;
}
