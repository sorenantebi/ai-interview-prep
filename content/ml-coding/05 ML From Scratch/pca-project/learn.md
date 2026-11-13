# Learn: PCA Projection

## The idea

- The task: find the directions in which the data varies most, then describe each row by its position along the top `k` of them.
- It shows up in feature pipelines (shrinking 50 columns to 5), in plotting high-dimensional data in 2D, and in denoising.
- **Principal component**: a unit-length direction in feature space.
  - The first one is where the data is most spread out.
  - The second is the most spread-out direction at a right angle to the first, and so on.
- **Centering**: subtract each column's mean, so every column averages 0.
- **Covariance matrix**: a `d x d` table where entry `(i, j)` says how much columns `i` and `j` vary together.
  - The diagonal holds each column's variance.
  - For centered data `Xc` it is `Xc.T @ Xc / (n - 1)`.
- **Eigenvector / eigenvalue**: for a covariance matrix, an eigenvector is a direction and its eigenvalue is the variance along it.
  - A big eigenvalue means an important direction.
- **Projection**: the dot product of a row with a unit direction.
  - It gives one number per row: how far along that direction the row sits.
- **Sign ambiguity**: if `v` is an eigenvector, so is `-v`, which is why the problem fixes a sign rule.
- **SVD** (singular value decomposition): a factorisation `Xc = U S Vᵀ`.
  - The rows of `Vᵀ` are the covariance eigenvectors, already sorted from most to least variance.
  - It is an alternative to building the covariance matrix yourself.

## Work it by hand

`X = [[1, 2], [3, 3], [5, 7]]`, `k = 1`, so `n = 3`, `d = 2`.

1. **Column means**: column 0 is `(1+3+5)/3 = 3`, column 1 is `(2+3+7)/3 = 4`.
2. **Center** (shape `(3, 2)`): `[[-2, -2], [0, -1], [2, 3]]`.
3. **Covariance** (divide by `n - 1 = 2`):
   - variance of column 0: `(4+0+4)/2 = 4`
   - variance of column 1: `(4+1+9)/2 = 7`
   - covariance between the columns: `(4+0+6)/2 = 5`
   - the matrix is `[[4, 5], [5, 7]]`, shape `(2, 2)`.
4. **Eigenvalues**: they solve `l^2 - 11l + 3 = 0` (trace 11, determinant `28 - 25 = 3`).
   - `l = (11 ± sqrt(109)) / 2`, about `10.720` and `0.280`.
   - The first is far bigger, so it is the top component.
5. **Eigenvector for 10.720**: `(4 - 10.720) x + 5 y = 0` gives `y = 1.344 x`.
   - Divide `(1, 1.344)` by its length `sqrt(1 + 1.806) = 1.675`.
   - Result: `(0.59694, 0.80229)`.
6. **Sign check**: the largest absolute entry is `0.80229`, already positive, so keep it.
7. **Project** each centered row onto it (dot product), giving shape `(3, 1)`:
   - `-2*0.59694 + -2*0.80229 = -2.79845`
   - `0*0.59694 + -1*0.80229 = -0.80229`
   - `2*0.59694 + 3*0.80229 = 3.60074`

Output: `[[-2.79845], [-0.80229], [3.60074]]`.

## Tools you'll need

### `a.mean(axis=0)` and broadcasting
- `axis=0` averages down the rows, giving one mean per column.
- Subtracting that length-`d` vector from an `(n, d)` array works row by row (**broadcasting**) and creates a new array.

```python
import numpy as np
a = np.array([[1.0, 10.0], [3.0, 20.0]])
m = a.mean(axis=0)
print(m, m.shape)  # [ 2. 15.] (2,)
print(a - m)
# [[-1. -5.]
#  [ 1.  5.]]
```

### `np.linalg.svd(A, full_matrices=False)`
- Returns `(U, S, Vt)`.
  - `S` holds the singular values, largest first.
  - The rows of `Vt` are the directions.
- With `full_matrices=False` and `A` of shape `(n, d)`, `n >= d`, `Vt` has shape `(d, d)`.
- Relation to variance: the variance along row `j` of `Vt` is `S[j]**2 / (n - 1)`.

```python
import numpy as np
A = np.array([[3.0, 0.0], [0.0, 2.0], [0.0, 0.0]])
U, S, Vt = np.linalg.svd(A, full_matrices=False)
print(S)         # [3. 2.]
print(U.shape)   # (3, 2)
print(Vt.shape)  # (2, 2)
```

### `np.cov(M, rowvar=False)` and `np.linalg.eigh(S)`
- This is the other route: build the covariance matrix, then decompose it.
- `np.cov` treats rows as variables by default, so pass `rowvar=False` when columns are features.
  - It centers the data and divides by `n - 1`.
- `eigh` is for symmetric matrices and returns `(values, vectors)`.
  - Values come in **ascending** order.
  - Eigenvectors are the **columns** of `vectors`.

```python
import numpy as np
M = np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]])
print(np.cov(M, rowvar=False))
# [[1. 2.]
#  [2. 4.]]
vals, vecs = np.linalg.eigh(np.diag([3.0, 1.0]))
print(vals)  # [1. 3.]
```

### `np.argsort(v)`
- Returns the indices that would sort `v`, smallest first.
- Negate `v` to get largest first.
- Use the result to reorder values and matching columns together, e.g. `vecs[:, order]`.

```python
import numpy as np
v = np.array([0.5, 2.0, 1.0])
print(np.argsort(-v))  # [1 2 0]
```

### `np.abs(v).argmax()`
- `argmax` gives the index of the largest value, and on ties the **first** one.
- Apply it to absolute values to find the biggest-magnitude entry, then check the sign of the original entry at that index.

```python
import numpy as np
v = np.array([0.3, -0.9, 0.9])
i = np.abs(v).argmax()
print(i, v[i])  # 1 -0.9
```

### `@` (matrix product) and shapes
- `(n, d) @ (d, k)` gives `(n, k)`; each output entry is a row dotted with a column.
- `M[:k]` keeps the first `k` rows and `M[:, :k]` the first `k` columns.
- `.T` transposes.

```python
import numpy as np
A = np.ones((3, 2))
B = np.array([[1.0], [2.0]])
print((A @ B).shape)  # (3, 1)
print(A @ B)
# [[3.]
#  [3.]
#  [3.]]
```

## Common mistakes

- **Mixing up rows and columns.** `eigh` returns eigenvectors as columns, but `svd` returns them as rows of `Vt`.
  - Check which one you have before slicing.
- **Wrong order with `eigh`.** It sorts ascending, but you want the largest variance first.
  - Reorder values and vectors together.
- **Wrong `axis` or `rowvar`.** Means are per column (`axis=0`).
  - With `np.cov`, forget `rowvar=False` and you get an `n x n` matrix.
- **Projecting the raw data.** Project the *centered* data, not `X`.
- **Wrong sign rule.** Look at the entry with the largest *absolute* value and flip the whole component if that entry is negative.
  - Don't flip by the sum or by the first entry.
- **Changing `X` in place.** Build a new centered array instead of using `-=` on the input.

## Hints

### Hint 1
- Center the data by subtracting each column's mean.
- Get the principal directions of the centered data, sorted from most to least variance.
- Keep the first `k` directions.
- Fix each direction's sign.
- Multiply the centered data by those directions.

### Hint 2
- Centering: subtract `X.mean(axis=0)`; shape stays `(n, d)`.
- Directions: `np.linalg.svd(..., full_matrices=False)` gives `Vt` of shape `(d, d)`, rows sorted by variance.
  - With `eigh` instead, use `np.argsort` on the negated values and take columns.
- Keep the first `k` directions: `(k, d)` from `Vt`.
- Sign fix: use `np.abs(...).argmax()` per direction, keeping shape `(k, d)`.
- Project: centered data `(n, d)` times the transposed directions `(d, k)` gives `(n, k)`.

### Hint 3
- For each kept direction (one row of the `(k, d)` matrix), find the position of its entry with the largest absolute value.
- If the entry at that position is negative, multiply the whole direction by -1.
- Do this for every direction before projecting.
- Column `j` of the output is the centered data times direction `j`.
  - That is one matrix product with the `(d, k)` transpose of your directions.
