#include <iostream>
#include <numeric>
#include <string>

class Fraction {
public:
    Fraction(long long num = 0, long long den = 1) : num_(num), den_(den) {
        // TODO: make den positive and divide both by their gcd
    }
    long long num() const { return num_; }
    long long den() const { return den_; }

private:
    long long num_, den_;
};

// TODO: operators + - * / == < and <<

int main() {
    int q;
    std::cin >> q;
    // TODO: read "a/b op c/d" lines and print the results
    return 0;
}
