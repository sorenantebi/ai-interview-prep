# Learn: Ridge Regression (Closed Form)

## The idea

- **Linear regression** fits a straight line (or flat plane) through data: `prediction = w[0] + w[1]·x1 + w[2]·x2 + ...`.
  - `w[0]` is the **intercept**: the prediction when every feature is 0.
  - `w[1:]` are the **slopes**: how much the prediction moves per unit of each feature.
- **Ridge regression** adds one twist: besides making errors small, it also keeps the slopes small.
  - Big slopes often mean the model is chasing noise.
  - A small penalty makes the fit steadier.
- It shows up as a baseline model, and as the standard fix when features are strongly correlated or there are more features than rows.
- **Penalty**: `alpha · (sum of squared slopes)`.
  - A larger `alpha` pulls the slopes harder towards 0.
  - The intercept is left out, because it only sets the overall level of predictions, not how wiggly the model is.
- **Closed form**: a formula gives the answer directly, so no training loop is needed.
  - Set the gradient of the loss to zero and you get a linear system `M w = b`.
  - `M = AᵀA + alpha·D` and `b = Aᵀy`.
- **`A`**: `X` with a column of ones in front. That column is what makes `w[0]` an intercept.
- **`D`**: the identity matrix with its first diagonal entry set to 0. That zero leaves the intercept unpenalised.
- **Linear system**: a set of equations like `3·w0 + 6·w1 = 15`. "Solving" means finding the `w` that satisfies all of them.

## Work it by hand

Example 1: `X = [[1],[2],[3]]`, `y = [3,5,7]`, `alpha = 1`.

1. Put ones in front. `A` has shape `(3, 2)`: rows `[1,1]`, `[1,2]`, `[1,3]`.
2. Compute `AᵀA`, shape `(2, 2)`:
   - top-left: 1+1+1 = 3
   - off-diagonal: 1+2+3 = 6
   - bottom-right: 1+4+9 = 14
   - so `AᵀA = [[3, 6], [6, 14]]`
3. Compute `Aᵀy`, shape `(2,)`: `[3+5+7, 1·3+2·5+3·7] = [15, 34]`.
4. Build the penalty `alpha·D = [[0, 0], [0, 1]]` and add it to `AᵀA`:
   - `M = [[3, 6], [6, 15]]`
   - only the bottom-right entry changed
5. Solve `M w = [15, 34]`, which is two equations:
   - `3·w0 + 6·w1 = 15`, so `w0 = 5 - 2·w1`
   - `6·w0 + 15·w1 = 34`; substituting gives `30 - 12·w1 + 15·w1 = 34`, so `3·w1 = 4` and `w1 = 1.33333`
   - then `w0 = 5 - 8/3 = 2.33333`
6. Result: `[2.33333, 1.33333]`, matching the expected output.
   - Without the penalty the answer would be exactly `[1, 2]`, so the slope was shrunk from 2 to 1.33.

## Tools you'll need

### np.hstack([a, b])

- Glues arrays side by side (along columns). The row counts must match.
- `np.ones((rows, 1))` makes a 2-D column of ones, which is how you add an intercept column.

```python
import numpy as np
b = np.array([[4., 7.], [5., 8.], [6., 9.]])
out = np.hstack([np.ones((3, 1)), b])
print(out.shape)  # (3, 3)
print(out)
# [[1. 4. 7.]
#  [1. 5. 8.]
#  [1. 6. 9.]]
```

### np.eye(k)

- The `k × k` identity matrix: 1s on the diagonal, 0s elsewhere.
- Multiply by a number to scale the diagonal.
- Overwrite a single entry with `M[i, j] = value`.

```python
import numpy as np
M = 5 * np.eye(3)
M[2, 2] = 0.0
print(M)
# [[5. 0. 0.]
#  [0. 5. 0.]
#  [0. 0. 0.]]
```

### `.T` and `@`

- `.T` transposes: rows become columns.
- `@` is matrix multiplication.
- A `(3, 2)` matrix transposed is `(2, 3)`, so `M.T @ M` is `(2, 2)`.
- `M.T @ v` with a 1-D `v` gives a 1-D result.

```python
import numpy as np
M = np.array([[1, 2], [3, 4], [5, 6]])
v = np.array([1, 1, 1])
print((M.T @ M).shape)  # (2, 2)
print(M.T @ M)
# [[35 44]
#  [44 56]]
print(M.T @ v)  # [ 9 12]
```

### np.linalg.solve(M, b)

- Solves `M x = b` for `x`. `M` must be square; `b` can be 1-D.
- Faster and more accurate than `inv(M) @ b`, so avoid the explicit inverse.

```python
import numpy as np
M = np.array([[2., 1.], [1., 3.]])
b = np.array([5., 10.])
x = np.linalg.solve(M, b)
print(np.round(x, 6))  # [1. 3.]
```

## Common mistakes

- **Penalising the intercept.** Adding `alpha` to the whole diagonal changes the answer for Example 1. Make sure the top-left entry gets no penalty.
- **Putting the ones column at the end.** The output must have the intercept first, so the ones column goes in front.
- **Wrong sizes.** `D` must be `(d+1) × (d+1)`, not `d × d`. Take the size from `A`'s columns.
- **Computing an explicit inverse.** `np.linalg.inv(M) @ b` works on easy cases but is slower and less stable. Use `np.linalg.solve`.
- **Shape slips in `Aᵀy`.** Keep `y` 1-D `(n,)`. Reshaping it to `(n, 1)` makes the result 2-D, but the output should be 1-D.

## Hints

### Hint 1

- Add a column of ones to the front of `X`.
- Compute the two ingredients of the normal equations: the matrix `AᵀA` and the vector `Aᵀy`.
- Build a penalty matrix that is `alpha` on the diagonal, except at the intercept's position.
- Add the penalty to `AᵀA`.
- Solve the linear system for `w`.

### Hint 2

- `np.hstack` with `np.ones((n, 1))` gives `A` of shape `(n, d+1)`.
- `A.T @ A` is `(d+1, d+1)` and `A.T @ y` is `(d+1,)`.
- `np.eye` of size `d+1`, scaled by `alpha`, gives the penalty matrix.
- `np.linalg.solve` finishes the job and returns shape `(d+1,)`.

### Hint 3

- The penalty matrix is `alpha` times the identity, except its first diagonal entry (row 0, column 0) is set to 0.
- Add it to `AᵀA` to get `M`.
- The answer is the `w` that satisfies `M w = Aᵀy`.
- Check with Example 1: `M = [[3, 6], [6, 15]]` and `Aᵀy = [15, 34]`.
