---
topic: "C++ Basics"
difficulty: Easy
---
# Compile It Yourself - Solution

## Intuition

Building a C++ program is two steps:

1. **Compile** (`-c`): each `.cpp` file becomes an object file (`.o`) of machine code. Calls to functions in other files are left as unresolved references.
2. **Link**: the object files and libraries are joined into one program, and those references are filled in.

`-o` only names the output of a step; without it you get `main.o` from step 1 and `a.out` (`a.exe` on Windows) from step 2.

## Approach

```
g++ -c main.cpp -o main.o
g++ main.o -o trader
```

Why it matters: in a project with many files, changing one `.cpp` file means recompiling only that file and then linking again. And the errors differ: "was not declared" comes from compiling, "undefined reference" (or "undefined symbols") comes from linking, when something was declared but its definition was never linked in.

## Solution

```cpp
// compile: g++ -c main.cpp -o main.o
// compile: g++ main.o -o trader
#include <fstream>
#include <iostream>
#include <string>

int main(int, char** argv) {
    // What your compile steps produced: the program's file name, and whether main.o was made first.
    std::string name = argv[0];
    name = name.substr(name.find_last_of("/\\") + 1);
    if (name.size() > 4 && name.substr(name.size() - 4) == ".exe") name.resize(name.size() - 4);
    std::cout << "binary " << name << "\n";
    std::cout << "object file " << (std::ifstream("main.o") ? "main.o" : "none") << "\n";

    for (int qty; std::cin >> qty;) std::cout << qty << " -> " << qty / 100 << " lots\n";
    return 0;
}
```
