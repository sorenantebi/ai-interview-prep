#include <iostream>
#include <string>
#include <vector>

class Order {
public:
    Order() : id_(0) { /* TODO */ }
    ~Order() { /* TODO */ }
    int id() const { return id_; }
    // TODO: static alive() and created()
private:
    int id_;
    // TODO: static int nextId_, alive_ (and define them outside the class, or make them inline)
};

int main() {
    std::vector<Order*> orders;
    std::string cmd;
    while (std::cin >> cmd) {
        // TODO: create / destroy <id> / stats
    }
    // TODO: delete the remaining orders and print the final stats line
    return 0;
}
