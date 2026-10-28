---
topic: "C++ Basics"
difficulty: Easy
---
# Counting Live Objects With Static Members - Solution

## Intuition

A non-static data member exists once per object; a `static` data member exists **once per class**, shared by all objects (like a global, but scoped to the class and subject to access control). The constructor and destructor of every `Order` update the same two counters. A `static` member function has no `this`, so it can only touch static members, and it's called through the class name.

## Approach

1. `static inline int nextId_ = 0, alive_ = 0;` (C++17 `inline` lets you define them in the class; pre-C++17 you'd write `int Order::nextId_ = 0;` in one `.cpp` file).
2. Constructor: `id_ = ++nextId_; ++alive_;` Destructor: `--alive_;`.
3. `destroy k`: find the pointer with `id() == k`, `delete` it, erase it from the vector.
4. After the loop, `delete` everything left and print the stats again: `alive` must be 0.

## Code

```cpp
#include <iostream>
#include <string>
#include <vector>

class Order {
public:
    Order() : id_(++nextId_) { ++alive_; }
    ~Order() { --alive_; }
    int id() const { return id_; }
    static int alive() { return alive_; }
    static int created() { return nextId_; }

private:
    int id_;
    static inline int nextId_ = 0;
    static inline int alive_ = 0;
};

void stats() { std::cout << "alive " << Order::alive() << " created " << Order::created() << '\n'; }

int main() {
    std::vector<Order*> orders;
    std::string cmd;
    while (std::cin >> cmd) {
        if (cmd == "create") {
            orders.push_back(new Order());
            std::cout << "created " << orders.back()->id() << '\n';
        } else if (cmd == "destroy") {
            int id;
            std::cin >> id;
            bool found = false;
            for (std::size_t i = 0; i < orders.size(); ++i) {
                if (orders[i]->id() == id) {
                    delete orders[i];
                    orders.erase(orders.begin() + i);
                    found = true;
                    break;
                }
            }
            if (found) std::cout << "destroyed " << id << '\n';
            else std::cout << "no order " << id << '\n';
        } else if (cmd == "stats") {
            stats();
        }
    }
    for (Order* o : orders) delete o;
    orders.clear();
    stats();
    return 0;
}
```

## Complexity

- Time: O(live orders) per `destroy`, O(1) otherwise.
- Space: O(live orders)

## Interview follow-ups

- Why does a static member need a definition outside the class before C++17, and what linker error do you get without it?
- What's the "static initialisation order fiasco", and how does a function-local `static` (Meyers singleton) avoid it? Is that initialisation thread-safe? (Yes, since C++11.)
- Is `++alive_` safe if orders are created from several threads? (No: make it `std::atomic<int>`.)
- What do the other meanings of `static` mean: a `static` local variable, a `static` free function / global (internal linkage)?
- Copying an `Order` with the default copy constructor breaks the counts. Why, and how do you fix it?
