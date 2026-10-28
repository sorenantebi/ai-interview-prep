---
topic: "C++ Basics"
difficulty: Medium
---
# Virtual Dispatch Through Base Pointers

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) with a small class hierarchy:

```cpp
class Shape {
public:
    virtual ~Shape();                      // virtual: we delete through Shape*
    virtual double area() const = 0;       // pure virtual
    virtual const char* name() const = 0;
};
class Circle : public Shape { /* radius r:  area = pi * r * r */ };
class Rect   : public Shape { /* w x h:     area = w * h      */ };
class Square : public Rect  { /* side s: a Rect(s, s) that overrides only name() */ };
```

The program reads `n`, then `n` lines of the form `circle r`, `rect w h` or `square s`. Create each shape with `new` and keep **only** `Shape*` pointers (in a `std::vector<Shape*>` or a `new Shape*[n]`). Then, using only the base-class interface, print one line per shape and a final total:

```text
<name> <area>
total <sum of areas>
```

Areas are printed with exactly 2 decimals. Use `pi = 3.14159265358979`. Finally `delete` every shape through its `Shape*`.

## Examples

**Example 1**
```text
Input:
3
circle 1
rect 2 3
square 2
Output:
circle 3.14
rect 6.00
square 4.00
total 13.14
```

**Example 2**
```text
Input:
1
square 5
Output:
square 25.00
total 25.00
```

## Constraints

- `1 <= n <= 1000`, dimensions are positive and at most `1000`.
- No `switch` on a type tag after construction: `area()` and `name()` must dispatch virtually. Use `override` in the derived classes.
