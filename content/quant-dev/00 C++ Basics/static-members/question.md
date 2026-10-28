---
topic: "C++ Basics"
difficulty: Easy
---
# Counting Live Objects With Static Members

**Topic:** C++ Basics · **Difficulty:** Easy

## Problem

Write a complete program (including `main`) with a class `Order` that uses **static** data members to hand out ids and to count how many orders exist:

```cpp
class Order {
public:
    Order();                        // id_ = ++nextId_; ++alive_
    ~Order();                       // --alive_
    int id() const;
    static int alive();             // orders currently alive
    static int created();           // orders ever created (== last id handed out)
private:
    int id_;
    static int nextId_;
    static int alive_;
};
```

The program reads commands, one per line, until end of input:

- `create` - `new` an `Order`, print `created <id>`
- `destroy <id>` - `delete` that order and print `destroyed <id>`, or print `no order <id>` if it doesn't exist (anymore)
- `stats` - print `alive <alive> created <created>`

At the end, delete every remaining order and print a final `stats` line. Keep the live orders as `Order*` in a `std::vector`.

## Examples

**Example 1**
```text
Input:
create
create
stats
destroy 1
stats
Output:
created 1
created 2
alive 2 created 2
destroyed 1
alive 1 created 2
alive 0 created 2
```

**Example 2**
```text
Input:
stats
destroy 5
Output:
alive 0 created 0
no order 5
alive 0 created 0
```

## Constraints

- At most `1000` commands.
- `alive()` and `created()` must be `static` member functions, called as `Order::alive()` (no object needed).
