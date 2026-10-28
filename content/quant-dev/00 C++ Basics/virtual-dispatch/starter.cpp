#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

const double PI = 3.14159265358979;

class Shape {
public:
    virtual ~Shape() {}
    // TODO: pure virtual area() and name()
};

// TODO: Circle, Rect, Square (derives from Rect)

int main() {
    int n;
    std::cin >> n;
    std::vector<Shape*> shapes;
    // TODO: read each line, push_back(new ...), print "<name> <area>" and "total <sum>", delete all
    return 0;
}
