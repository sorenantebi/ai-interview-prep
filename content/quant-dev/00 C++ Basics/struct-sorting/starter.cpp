#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Trade {
    std::string symbol;
    double price;
    int qty;
    double notional() const { return 0; /* TODO */ }
};

bool bySymbol(const Trade& a, const Trade& b) {
    // TODO: symbol asc, then price desc, then qty asc
    return false;
}

bool byNotional(const Trade& a, const Trade& b) {
    // TODO: notional desc, then symbol asc
    return false;
}

int main() {
    std::string mode;
    int n;
    std::cin >> mode >> n;
    // TODO: read the trades, std::sort with the right comparator, print them and the total
    return 0;
}
