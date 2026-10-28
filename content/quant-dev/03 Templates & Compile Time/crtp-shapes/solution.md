---
topic: "Templates & Compile Time"
difficulty: Medium
---
# CRTP Shapes - Solution

## Intuition

Inside `Shape<Derived>` the base knows its exact derived type at compile time, so `static_cast<const Derived&>(*this).area_impl()` is a direct, inlinable call. A static data member of a class template exists once **per instantiation**, so `Shape<Circle>` and `Shape<Rectangle>` each get their own counter for free.

## Approach

1. `area()`: downcast `*this` to `const Derived&` and call `area_impl()`. This is safe because `Derived` really is the dynamic type (that's the CRTP contract).
2. Counter: `inline static int count_` in the template. Increment in the default and copy constructors, decrement in the destructor, leave assignment alone. The derived classes' implicit copy and move constructors call the base copy constructor, so copies are counted too.
3. Keep the base constructors and destructor `protected`, so nobody creates a bare `Shape<X>` or deletes through a `Shape*` (there's no virtual destructor).
4. `total_area`: `std::apply` unpacks the tuple into a lambda, and a fold expression sums `area()`.

### CRTP vs virtual dispatch

| | `virtual` | CRTP |
|---|---|---|
| Call | load vptr, load slot, indirect call | direct call, usually inlined |
| Object size | + 8 bytes (vptr) | no overhead |
| Heterogeneous container | `std::vector<Shape*>` works | needs `std::tuple` / `std::variant`; types fixed at compile time |
| Code size | one function | one instantiation per derived type |

Use CRTP when the set of types is known at compile time and the call is hot; use virtual functions when types are chosen at run time (plugins, config-driven strategies).

## Code

```cpp
#include <numbers>
#include <tuple>

template <class Derived>
class Shape {
public:
    double area() const { return static_cast<const Derived&>(*this).area_impl(); }
    static int live_count() { return count_; }

protected:
    Shape() { ++count_; }
    Shape(const Shape&) { ++count_; }
    Shape& operator=(const Shape&) = default;
    ~Shape() { --count_; }

private:
    inline static int count_ = 0;
};

class Circle : public Shape<Circle> {
public:
    explicit Circle(double r) : r_(r) {}
    double area_impl() const { return std::numbers::pi * r_ * r_; }

private:
    double r_;
};

class Rectangle : public Shape<Rectangle> {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area_impl() const { return w_ * h_; }

private:
    double w_, h_;
};

template <class... Shapes>
double total_area(const std::tuple<Shapes...>& shapes) {
    return std::apply([](const auto&... s) { return (0.0 + ... + s.area()); }, shapes);
}
```

## Complexity

- Time: O(1) per `area()` call with no indirection; O(k) for `total_area` over k shapes, fully unrolled.
- Space: no per-object overhead (no vptr); one `int` counter per derived type.

## Interview follow-ups

- How do you stop `class Square : public Shape<Circle>` from compiling? (Make the base constructors private and add `friend Derived;`.)
- The counter isn't thread-safe. Fix it (`std::atomic<int>`) and discuss the cost on a hot path.
- Store mixed shapes in a `std::vector<std::variant<Circle, Rectangle>>` and sum with `std::visit`. How does that compare to CRTP and to virtual?
- C++23 "deducing this" (`double area(this const auto& self)`) removes the need for CRTP. Show it.
- When does the compiler devirtualise a virtual call anyway? (`final` classes, known dynamic type, LTO.)
