// compile: g++ main.cpp
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
