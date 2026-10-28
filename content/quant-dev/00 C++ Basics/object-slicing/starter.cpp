#include <iostream>
#include <string>

class Base {
public:
    explicit Base(int value) : value_(value) {}
    virtual ~Base() = default;
    // TODO: virtual describe() returning "Base(<value>)"
protected:
    int value_;
};

// TODO: class Derived : public Base with bonus_ and describe() returning "Derived(<value>,<bonus>)"

// TODO: byValue(Base), byRef(const Base&), byPtr(const Base*)

int main() {
    int n;
    std::cin >> n;
    // TODO: for each line build a Base or Derived and print the three results
    return 0;
}
