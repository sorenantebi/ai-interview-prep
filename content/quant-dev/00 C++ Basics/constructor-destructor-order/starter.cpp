#include <iostream>

struct Vehicle {
    int id;
    // TODO: constructor prints "Vehicle <id>", destructor prints "~Vehicle <id>"
};

struct Engine {
    int id;
    // TODO
};

struct Radio {
    int id;
    // TODO
};

struct Car : Vehicle {
    Engine engine;
    Radio radio;
    // TODO: Car(int id) : Vehicle(id), radio(id), engine(id) { print "Car <id>" }, and ~Car
};

int main() {
    int n;
    std::cin >> n;
    std::cout << "-- begin\n";
    // TODO: the block from the problem statement
    std::cout << "-- end\n";
    return 0;
}
