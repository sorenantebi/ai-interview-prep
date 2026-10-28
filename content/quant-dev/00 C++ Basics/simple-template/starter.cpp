#include <iostream>
#include <string>

// TODO: template maxOf and swapValues

template <typename T, int Capacity>
class Stack {
public:
    // TODO: push, pop, top, size, empty, ...
private:
    T data_[Capacity];
    int size_ = 0;
};

template <typename T>
void run() {
    // TODO: Stack<T, 4> s; read commands until end of input
}

int main() {
    std::string type;
    std::cin >> type;
    if (type == "int") run<int>();
    else run<std::string>();
    return 0;
}
