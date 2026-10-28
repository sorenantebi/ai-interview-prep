---
topic: "Containers & Allocators"
difficulty: Easy
---
# Matrix with a Row Proxy - Solution

## Intuition

`m[r][c]` is two calls: `m.operator[](r)` and then `operator[](c)` on whatever the first one returned. If the first returns a lightweight object holding "pointer to the start of row `r`, and the row length", the second call can check `c` and return a reference into the matrix's storage. Because it returns a real `double&`, reads, writes and `+=` all work. A separate `ConstRow` holding a `const double*` keeps `const Matrix` read-only.

## Approach

1. Store `rows_`, `cols_` and a `std::vector<double> data_(rows * cols)` (zero-initialized, copyable for free).
2. `Row` holds `double* p` and `size_t n`. `operator[](c)` throws if `c >= n`, else returns `p[c]`.
3. `ConstRow` is the same with `const double*`.
4. `Matrix::operator[](r)`: throw if `r >= rows_`, else return a proxy pointing at `data_.data() + r * cols_`.

## Code

```cpp
#include <cstddef>
#include <stdexcept>
#include <vector>

class Matrix {
public:
    class Row {
    public:
        double& operator[](std::size_t c) {
            if (c >= n_) throw std::out_of_range("Matrix column index");
            return p_[c];
        }

    private:
        friend class Matrix;
        Row(double* p, std::size_t n) : p_(p), n_(n) {}
        double* p_;
        std::size_t n_;
    };

    class ConstRow {
    public:
        const double& operator[](std::size_t c) const {
            if (c >= n_) throw std::out_of_range("Matrix column index");
            return p_[c];
        }

    private:
        friend class Matrix;
        ConstRow(const double* p, std::size_t n) : p_(p), n_(n) {}
        const double* p_;
        std::size_t n_;
    };

    Matrix(std::size_t rows, std::size_t cols) : rows_(rows), cols_(cols), data_(rows * cols, 0.0) {}

    std::size_t rows() const noexcept { return rows_; }
    std::size_t cols() const noexcept { return cols_; }

    Row operator[](std::size_t r) {
        check_row(r);
        return Row(data_.data() + r * cols_, cols_);
    }
    ConstRow operator[](std::size_t r) const {
        check_row(r);
        return ConstRow(data_.data() + r * cols_, cols_);
    }

private:
    void check_row(std::size_t r) const {
        if (r >= rows_) throw std::out_of_range("Matrix row index");
    }

    std::size_t rows_, cols_;
    std::vector<double> data_;
};
```

## Complexity

- Time: O(1) per element access (two comparisons and pointer arithmetic; the proxy is optimized away).
- Space: `rows * cols` doubles in one block.

## Interview follow-ups

- C++23 allows `m[r, c]` with a multi-argument `operator[]`. What does that remove, and what does `std::mdspan` add?
- Why is iterating `for r, for c` much faster than `for c, for r` on a row-major matrix?
- What goes wrong if a `Row` proxy outlives the matrix, or survives a resize? How does `std::vector<bool>::reference` have the same issue?
- Implement matrix multiplication and make it cache-friendly (loop order i-k-j, blocking).
- Remove the bounds checks in release builds without changing call sites.
