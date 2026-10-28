---
topic: "C++ Basics"
difficulty: Medium
---
# Constructor and Destructor Order - Solution

## Intuition

Construction builds an object from the inside out: first the base class subobjects, then the data members **in the order they are declared in the class**, and only then the constructor body. The order you write in the initialiser list is ignored (compilers warn with `-Wreorder`). Destruction runs in exactly the reverse order: destructor body, members in reverse declaration order, then bases. Automatic (stack) objects are destroyed when their scope ends, in reverse order of construction, so the loop's `temp` dies at the end of every iteration while `first` lives until the closing brace of the outer block.

## Approach

1. Give each of `Vehicle`, `Engine`, `Radio` an `int id`, a constructor that prints `Name id` and a destructor that prints `~Name id`.
2. `Car(int id) : Vehicle(id), radio(id), engine(id)` prints `Car id` in its body; `~Car` prints `~Car id`.
3. `main` is the block from the statement.

For one `Car`: `Vehicle, Engine, Radio, Car`, then `~Car, ~Radio, ~Engine, ~Vehicle`.

## Code

```cpp
#include <iostream>

struct Vehicle {
    int id;
    Vehicle(int i) : id(i) { std::cout << "Vehicle " << id << '\n'; }
    ~Vehicle() { std::cout << "~Vehicle " << id << '\n'; }
};

struct Engine {
    int id;
    Engine(int i) : id(i) { std::cout << "Engine " << id << '\n'; }
    ~Engine() { std::cout << "~Engine " << id << '\n'; }
};

struct Radio {
    int id;
    Radio(int i) : id(i) { std::cout << "Radio " << id << '\n'; }
    ~Radio() { std::cout << "~Radio " << id << '\n'; }
};

struct Car : Vehicle {
    Engine engine;
    Radio radio;
    // Deliberately "wrong" order: members are still built engine first, then radio.
    Car(int i) : Vehicle(i), radio(i), engine(i) { std::cout << "Car " << id << '\n'; }
    ~Car() { std::cout << "~Car " << id << '\n'; }
};

int main() {
    int n;
    std::cin >> n;
    std::cout << "-- begin\n";
    {
        Car first(1);
        for (int i = 2; i <= n; ++i) {
            Car temp(i);
        }
    }
    std::cout << "-- end\n";
    return 0;
}
```

## Complexity

- Time: O(n)
- Space: O(1) (at most two `Car`s alive at once).

## Interview follow-ups

- Why does initialiser-list order not matter, and what bug do you get if `radio`'s initialiser reads `engine` but `radio` is declared first?
- If `Engine`'s constructor throws, which destructors run? (Only fully constructed subobjects: `~Vehicle`. `~Car` does not run.)
- Why should a destructor never throw? (During stack unwinding a second exception calls `std::terminate`; destructors are `noexcept` by default.)
- When are a global, a function-local `static`, and a temporary (`Car(5);` on its own line) constructed and destroyed?
- What changes if you `new Car(1)` and never `delete` it?
