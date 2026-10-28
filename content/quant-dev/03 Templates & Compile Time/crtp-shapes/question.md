---
topic: "Templates & Compile Time"
difficulty: Medium
---
# CRTP Shapes

**Topic:** Templates & Compile Time · **Difficulty:** Medium

## Problem

A virtual call goes through a vtable pointer: an extra memory load, an indirect branch the CPU may mispredict, and a call the compiler usually can't inline. On a hot path (order handlers, strategy callbacks) many HFT codebases replace runtime polymorphism with the **Curiously Recurring Template Pattern**: the base class is a template on its derived class and calls into it with a `static_cast`, so every call is resolved at compile time.

Build a small CRTP hierarchy:

```cpp
template <class Derived>
class Shape {
public:
    double area() const;              // forwards to Derived::area_impl() with no virtual call
    static int live_count();          // how many Derived objects currently exist
protected:
    Shape();                          // count bookkeeping lives here
    Shape(const Shape&);
    Shape& operator=(const Shape&);
    ~Shape();
};

class Circle : public Shape<Circle> {
public:
    explicit Circle(double r);
    double area_impl() const;         // pi * r * r
};

class Rectangle : public Shape<Rectangle> {
public:
    Rectangle(double w, double h);
    double area_impl() const;         // w * h
};

template <class... Shapes>
double total_area(const std::tuple<Shapes...>& shapes);   // sum of area() over the tuple
```

The counter is **per derived type**: creating a `Circle` doesn't change `Rectangle::live_count()`. Copies count as new objects; assignment doesn't change the count. Use `std::numbers::pi` for pi.

## Examples

**Example 1**
```cpp
Circle c(1.0);
Rectangle r(2.0, 3.0);
c.area();                          // 3.14159...
r.area();                          // 6.0
total_area(std::tuple{c, r});      // 9.14159...
```

**Example 2**
```cpp
int before = Circle::live_count();
{
    Circle a(1), b(2);
    Circle copy = a;
    Circle::live_count() - before;     // 3
    Rectangle::live_count();           // unchanged
}
Circle::live_count() - before;         // 0
```

## Constraints

- No `virtual` anywhere: `Circle` and `Rectangle` must not be polymorphic types and `sizeof(Circle) == sizeof(double)`.
- Any class `X : public Shape<X>` with a `double area_impl() const` must work with `area`, `live_count` and `total_area`.
