---
topic: "C++ Basics"
difficulty: Medium
---
# Object Slicing

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) that demonstrates object slicing:

```cpp
class Base {
public:
    explicit Base(int value);
    virtual ~Base() = default;
    virtual std::string describe() const;   // "Base(<value>)"
protected:
    int value_;
};

class Derived : public Base {
public:
    Derived(int value, int bonus);
    std::string describe() const override;  // "Derived(<value>,<bonus>)"
private:
    int bonus_;
};

std::string byValue(Base b);           // returns b.describe()
std::string byRef(const Base& b);      // returns b.describe()
std::string byPtr(const Base* b);      // returns b->describe()
```

The program reads `n`, then `n` lines that are either `B <value>` or `D <value> <bonus>`. For each line, construct that object on the stack and print

```text
value: <byValue(obj)> | ref: <byRef(obj)> | ptr: <byPtr(&obj)>
```

## Examples

**Example 1**
```text
Input:
2
B 3
D 5 7
Output:
value: Base(3) | ref: Base(3) | ptr: Base(3)
value: Base(5) | ref: Derived(5,7) | ptr: Derived(5,7)
```

**Example 2**
```text
Input:
1
D 1 2
Output:
value: Base(1) | ref: Derived(1,2) | ptr: Derived(1,2)
```

## Constraints

- `1 <= n <= 100`, all numbers fit in `int`.
- `byValue` must really take `Base` by value (that's the point).
