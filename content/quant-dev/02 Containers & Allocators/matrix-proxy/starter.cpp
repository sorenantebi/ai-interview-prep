#include <cstddef>
#include <stdexcept>
#include <vector>

class Matrix {
public:
    class Row {
    public:
        double& operator[](std::size_t c) { throw std::logic_error("not implemented"); }
    };
    class ConstRow {
    public:
        const double& operator[](std::size_t c) const { throw std::logic_error("not implemented"); }
    };

    Matrix(std::size_t rows, std::size_t cols) {}
    std::size_t rows() const noexcept { return 0; }
    std::size_t cols() const noexcept { return 0; }
    Row operator[](std::size_t r) { return Row(); }
    ConstRow operator[](std::size_t r) const { return ConstRow(); }
};
