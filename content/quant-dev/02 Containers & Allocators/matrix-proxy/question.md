---
topic: "Containers & Allocators"
difficulty: Easy
---
# Matrix with a Row Proxy

**Topic:** Containers & Allocators · **Difficulty:** Easy

## Problem

Covariance matrices, correlation grids and risk ladders are 2-D tables of doubles. For speed they should live in one contiguous row-major block (`rows * cols` doubles, no `vector<vector<double>>`). Users still want to write `m[r][c]`. C++ has no two-argument `operator[]` before C++23, so the usual trick is the **proxy class** idiom: `m[r]` returns a small `Row` object that remembers where row `r` starts, and `Row::operator[](c)` returns the element. Here both levels also check their bounds.

Implement `Matrix`:

```cpp
class Matrix {
public:
    class Row {                                  // returned by Matrix::operator[] (non-const)
    public:
        double& operator[](std::size_t c);       // throws std::out_of_range if c >= cols
    };
    class ConstRow {                             // returned by Matrix::operator[] const
    public:
        const double& operator[](std::size_t c) const;  // throws std::out_of_range if c >= cols
    };

    Matrix(std::size_t rows, std::size_t cols);  // all elements 0.0
    std::size_t rows() const noexcept;
    std::size_t cols() const noexcept;
    Row operator[](std::size_t r);               // throws std::out_of_range if r >= rows
    ConstRow operator[](std::size_t r) const;    // throws std::out_of_range if r >= rows
};
```

Elements are stored contiguously in row-major order: `&m[r][c] == &m[0][0] + r * cols + c`.

## Examples

**Example 1**
```cpp
Matrix m(2, 3);
m[1][2] = 4.5;
m[1][2] += 0.5;
m[1][2];         // 5.0
m[0][0];         // 0.0
m.rows();        // 2
m.cols();        // 3
```

**Example 2**
```cpp
const Matrix& cm = m;
cm[1][2];        // 5.0 (read-only access through ConstRow)
m[2][0];         // throws std::out_of_range: row 2 doesn't exist
m[0][3];         // throws std::out_of_range: column 3 doesn't exist
```

## Constraints

- `0 <= rows, cols <= 2000`.
- Indexing is O(1) and allocates nothing; the proxy is just a pointer and a length.
- `Matrix` is copyable (a copy is independent of the original).
