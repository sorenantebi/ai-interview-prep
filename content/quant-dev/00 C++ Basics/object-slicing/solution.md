---
topic: "C++ Basics"
difficulty: Medium
---
# Object Slicing - Solution

## Intuition

Passing a `Derived` to a parameter of type `Base` (by value) copy-constructs a brand-new `Base` from the `Base` part of the argument; the `Derived` part (`bonus_`) and its dynamic type are **sliced off**. The copy's vptr points to `Base`'s vtable, so `describe()` calls `Base::describe`. A reference or pointer, on the other hand, refers to the original object, so the virtual call dispatches to `Derived::describe`. For a plain `Base` all three agree.

## Approach

1. Implement both `describe`s with `std::to_string`.
2. Write the three free functions; their bodies are identical, only the parameter type differs.
3. In the loop, branch on the letter, build a `Base` or `Derived` on the stack, and print via a helper that takes `const Base&`, which itself doesn't slice.

## Code

```cpp
#include <iostream>
#include <string>

class Base {
public:
    explicit Base(int value) : value_(value) {}
    virtual ~Base() = default;
    virtual std::string describe() const { return "Base(" + std::to_string(value_) + ")"; }
protected:
    int value_;
};

class Derived : public Base {
public:
    Derived(int value, int bonus) : Base(value), bonus_(bonus) {}
    std::string describe() const override {
        return "Derived(" + std::to_string(value_) + "," + std::to_string(bonus_) + ")";
    }
private:
    int bonus_;
};

std::string byValue(Base b) { return b.describe(); }
std::string byRef(const Base& b) { return b.describe(); }
std::string byPtr(const Base* b) { return b->describe(); }

void report(const Base& obj) {
    std::cout << "value: " << byValue(obj) << " | ref: " << byRef(obj) << " | ptr: " << byPtr(&obj) << '\n';
}

int main() {
    int n;
    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        char kind;
        int value;
        std::cin >> kind >> value;
        if (kind == 'D') {
            int bonus;
            std::cin >> bonus;
            Derived d(value, bonus);
            report(d);
        } else {
            Base b(value);
            report(b);
        }
    }
    return 0;
}
```

## Complexity

- Time: O(n)
- Space: O(1) per object.

## Interview follow-ups

- Where else does slicing bite? (`std::vector<Base>` holding derived objects, `catch (std::exception e)` instead of `catch (const std::exception& e)`, assigning `Base b = d;`.)
- How do you prevent it? (Pass by reference/pointer; make base classes abstract or delete/protect their copy operations.)
- What does slicing do with the assignment `Base& r = d1; r = d2;`? (Calls `Base::operator=`: only the base part of `d1` changes, a "partial assignment".)
- How would you copy a polymorphic object correctly? (A virtual `clone()` returning `std::unique_ptr<Base>`.)
