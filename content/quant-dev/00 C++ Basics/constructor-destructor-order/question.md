---
topic: "C++ Basics"
difficulty: Medium
---
# Constructor and Destructor Order

**Topic:** C++ Basics · **Difficulty:** Medium

## Problem

Write a complete program (including `main`) whose output traces object lifetimes. Every constructor prints `<Class> <id>` and every destructor prints `~<Class> <id>`, each on its own line:

```cpp
struct Vehicle { /* base class */ };
struct Engine  { /* member */ };
struct Radio   { /* member */ };
struct Car : Vehicle {
    Engine engine;   // declared first
    Radio radio;     // declared second
    Car(int id);     // write the initialiser list as  : Vehicle(id), radio(id), engine(id)
};
```

Every class stores the `id` it was given. `main` reads `n` and then runs:

```cpp
std::cout << "-- begin\n";
{
    Car first(1);
    for (int i = 2; i <= n; ++i) {
        Car temp(i);
    }
}
std::cout << "-- end\n";
```

Predict the output before you run it: base before members, members in **declaration** order (not initialiser-list order), destruction in exactly the reverse order, and a loop-local object destroyed at the end of each iteration.

## Examples

**Example 1**
```text
Input:
1
Output:
-- begin
Vehicle 1
Engine 1
Radio 1
Car 1
~Car 1
~Radio 1
~Engine 1
~Vehicle 1
-- end
```

**Example 2**
```text
Input:
2
Output:
-- begin
Vehicle 1
Engine 1
Radio 1
Car 1
Vehicle 2
Engine 2
Radio 2
Car 2
~Car 2
~Radio 2
~Engine 2
~Vehicle 2
~Car 1
~Radio 1
~Engine 1
~Vehicle 1
-- end
```

## Constraints

- `1 <= n <= 20`
- No virtual functions needed; don't print from anywhere else.
