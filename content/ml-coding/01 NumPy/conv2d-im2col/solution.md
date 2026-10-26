---
topic: "NumPy"
difficulty: Hard
---
# Conv2D with im2col - Solution

## Intuition

Every output pixel is a dot product between one `kh × kw` patch of the image and the kernel. If you lay all the patches out as rows of a matrix (the "im2col" matrix, shape `(oh·ow, kh·kw)`), the whole convolution becomes a single matrix-vector product with the flattened kernel — which is how deep-learning libraries turn convolutions into fast matmuls.

## Approach

1. Output size: `oh = H - kh + 1`, `ow = W - kw + 1`.
2. Row indices: `rows[i, u] = i + u` (shape `(oh, kh)`); column indices: `cols[j, v] = j + v` (shape `(ow, kw)`), both by broadcasting two `arange`s.
3. Fancy-index the image with `rows[:, None, :, None]` and `cols[None, :, None, :]`; broadcasting gives `patches[i, j, u, v] = image[i + u, j + v]`, shape `(oh, ow, kh, kw)`.
4. Reshape to the im2col matrix `(oh·ow, kh·kw)`, multiply by `kernel.reshape(-1)` with `@`, and reshape back to `(oh, ow)`.

## Code

```python
import numpy as np

def conv2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    H, W = image.shape
    kh, kw = kernel.shape
    oh, ow = H - kh + 1, W - kw + 1
    rows = np.arange(oh)[:, None] + np.arange(kh)[None, :]  # (oh, kh): image rows each output row touches
    cols = np.arange(ow)[:, None] + np.arange(kw)[None, :]  # (ow, kw)
    patches = image[rows[:, None, :, None], cols[None, :, None, :]]  # (oh, ow, kh, kw)
    cols_matrix = patches.reshape(oh * ow, kh * kw)  # im2col: one row per output pixel
    return (cols_matrix @ kernel.reshape(-1)).reshape(oh, ow)
```

## Complexity

- **Time:** `O(H'·W'·kh·kw)`
- **Space:** `O(oh·ow·kh·kw)` — the im2col matrix holds every patch.
