---
topic: "C++ Basics"
difficulty: Medium
---
# Virtual Dispatch Through Base Pointers - Solution

## Intuition

Marking a member function `virtual` makes the call resolve at run time from the object's **dynamic** type, not the pointer's static type. Each polymorphic class has a vtable (a table of function pointers) and each object a hidden pointer to its class's vtable, so `s->area()` on a `Shape*` looks up the right `area` for a `Circle` or `Rect`. `Square` inherits `Rect::area` and overrides only `name`. Because we `delete` through `Shape*`, the base destructor must be virtual; otherwise the derived destructor would never run (undefined behaviour).

## Approach

1. Read the kind word; `new` the matching class and store it as `Shape*`.
2. Loop over the pointers: print `s->name()` and `s->area()` with `std::fixed << std::setprecision(2)`, accumulate the total.
3. `delete` each pointer.

## Code

```cpp
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

const double PI = 3.14159265358979;

class Shape {
public:
    virtual ~Shape() {}
    virtual double area() const = 0;
    virtual const char* name() const = 0;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : r_(r) {}
    double area() const override { return PI * r_ * r_; }
    const char* name() const override { return "circle"; }
private:
    double r_;
};

class Rect : public Shape {
public:
    Rect(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
    const char* name() const override { return "rect"; }
private:
    double w_, h_;
};

class Square : public Rect {
public:
    explicit Square(double s) : Rect(s, s) {}
    const char* name() const override { return "square"; }
};

int main() {
    int n;
    std::cin >> n;
    std::vector<Shape*> shapes;
    for (int i = 0; i < n; ++i) {
        std::string kind;
        double x, y;
        std::cin >> kind >> x;
        if (kind == "circle") shapes.push_back(new Circle(x));
        else if (kind == "square") shapes.push_back(new Square(x));
        else { std::cin >> y; shapes.push_back(new Rect(x, y)); }
    }

    std::cout << std::fixed << std::setprecision(2);
    double total = 0;
    for (const Shape* s : shapes) {
        std::cout << s->name() << ' ' << s->area() << '\n';
        total += s->area();
    }
    std::cout << "total " << total << '\n';

    for (Shape* s : shapes) delete s;
    return 0;
}
```

## Complexity

- Time: O(n)
- Space: O(n)

## Interview follow-ups

- How are vtables and vptrs laid out? What does `sizeof` of a class with one virtual function and no data return on a 64-bit machine? (8: the vptr.)
- What happens if `~Shape` is not virtual and you `delete` a `Circle` through a `Shape*`?
- Can a constructor be virtual? What happens if a base constructor calls a virtual function? (It calls the base version: the derived part doesn't exist yet.)
- What is the run-time cost of a virtual call, and why does it matter in a hot trading loop? (Indirect branch, blocks inlining.) Alternatives: CRTP / static polymorphism, `std::variant` + `std::visit`, `final` to let the compiler devirtualise.
- Rewrite ownership with `std::vector<std::unique_ptr<Shape>>` so no manual `delete` is needed.
