---
topic: "NumPy"
difficulty: Hard
---
# Conv2D with im2col

**Topic:** NumPy · **Difficulty:** Hard

## Problem

Implement a single-channel 2-D "valid" convolution as deep-learning libraries define it (cross-correlation, so the kernel is **not** flipped). For an image of shape `(H, W)` and a kernel of shape `(kh, kw)`, return the array of shape `(H - kh + 1, W - kw + 1)` with

`out[i, j] = Σ_{u, v} image[i + u, j + v] * kernel[u, v]`.

Use the im2col trick and build it yourself: with index arrays (fancy indexing), gather a matrix with one row per output pixel holding its `kh·kw` patch values, then compute the whole convolution as **one matrix product** with the flattened kernel. No Python loops.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: image = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], kernel = [[1.0, 0.0], [0.0, -1.0]]
Output: [[-4.00000,-4.00000],[-4.00000,-4.00000]]
```

**Example 2**
```text
Input: image = [[1.0, 2.0, 3.0, 4.0]], kernel = [[1.0, 1.0, 1.0]]
Output: [[6.00000,9.00000]]
```

## Constraints

- `1 <= kh <= H <= 2000`
- `1 <= kw <= W <= 2000`
