#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Position {
    std::string symbol;
    int qty;
    double price;
};

class Portfolio {
public:
    void add(const Position& p) { /* TODO */ }
    // TODO: find(...) const, value() const, size() const
private:
    std::vector<Position> positions_;
};

void report(const Portfolio& pf, const std::string& symbol) {
    // TODO: print "<symbol> <qty> @ <price> = <notional>" or "<symbol> not found"
}

int main() {
    // TODO: read n positions, q queries, print "positions <size> value <value>"
    return 0;
}
