# Learn: Linear Regression (Normal Equation)

## The idea

- The task: find the straight line (or plane, with more features) that fits your data best, in one step with no training loop.
- **Sum of squared errors**: for each sample, take prediction minus truth, square it, and add them all up.
  - Squaring makes every error positive and punishes big misses more than small ones.
  - The "best" weights are the ones that make this sum smallest.
- A prediction is `intercept + w1*x1 + w2*x2 + ...`.
- **Intercept (bias)**: the prediction when every feature is 0.
  - To treat it like any other weight, put a column of ones in front of `X`.
  - Call the new matrix `A`. Then all predictions are `A @ w`, and `w[0]` multiplies the ones, so it is the intercept.
- **Normal equation**: the closed-form condition for the best `w`, `AᵀA w = Aᵀy`.
  - Intuition: at the best `w`, the leftover error is perpendicular to every column of `A`.
  - Solving it jumps straight to the minimum, where gradient descent would take many small steps.
- Where it shows up: a quick baseline model, a sanity check for iterative training, and the core of many stats libraries.
- **Singular case**: with duplicate columns or fewer samples than weights, many `w` fit equally well.
  - `AᵀA` then has no inverse, so inverting it directly breaks.
  - A least-squares solver or the **pseudo-inverse** picks the answer with the smallest length `||w||`.

## Work it by hand

Example 1: `X = [[1], [2], [3]]`, `y = [3, 5, 7]`.

1. Shapes: `X` is `(3, 1)`, `y` is `(3,)`.
2. Put ones in front. `A` is `(3, 2)`:

```text
A = [[1, 1],
     [1, 2],
     [1, 3]]
```

3. Compute `AᵀA`, shape `(2, 2)`. Each entry is a dot product of two columns of `A`:

```text
AᵀA = [[1+1+1, 1+2+3],   = [[3,  6],
       [1+2+3, 1+4+9]]      [6, 14]]
```

4. Compute `Aᵀy`, shape `(2,)`:

```text
Aᵀy = [3+5+7, 1*3+2*5+3*7] = [15, 34]
```

5. Solve `[[3, 6], [6, 14]] w = [15, 34]`:
   - Equation 1: `3*w0 + 6*w1 = 15`, so `w0 + 2*w1 = 5`.
   - Equation 2: `6*w0 + 14*w1 = 34`.
   - Subtract 6 times the simplified equation 1 (`6*w0 + 12*w1 = 30`): `2*w1 = 4`, so `w1 = 2`.
   - Then `w0 = 5 - 4 = 1`.
6. Result: `w = [1, 2]`, which matches `[1.00000,2.00000]`.
   - Check: `1 + 2*1 = 3`, `1 + 2*2 = 5`, `1 + 2*3 = 7`. Every error is zero.

## Tools you'll need

### np.ones(shape)

- Makes an array filled with 1.0.
- Pass a tuple for a 2-D shape. A plain number gives a 1-D array.

```python
import numpy as np
c = np.ones((4, 1))
print(c.shape)  # (4, 1)
print(c.ravel())  # [1. 1. 1. 1.]
print(np.ones(4).shape)  # (4,)
```

### np.hstack([a, b])

- Glues 2-D arrays side by side. They must have the same number of rows.
- The order in the list is the order of the columns.
- `np.concatenate([a, b], axis=1)` does the same thing.

```python
import numpy as np
left = np.zeros((2, 1))
right = np.array([[5, 6], [7, 8]])
out = np.hstack([left, right])
print(out.shape)  # (2, 3)
print(out)
# [[0. 5. 6.]
#  [0. 7. 8.]]
```

### np.linalg.lstsq(A, b, rcond=None)

- Finds `w` that minimises `||A w - b||²`.
- It returns a tuple of four things: the solution, the residuals, the rank, and the singular values. The solution is the first item.
- When many solutions tie, it returns the one with the smallest norm.
- Pass `rcond=None` to use the modern cut-off and avoid a warning.

```python
import numpy as np
A = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
b = np.array([1.0, 2.0, 3.0])
result = np.linalg.lstsq(A, b, rcond=None)
print(len(result))  # 4
print(result[0].round(3))  # [1. 2.]
print(result[2])  # 2
```

### np.linalg.pinv(A)

- The pseudo-inverse. `pinv(A) @ b` gives the same minimum-norm answer as `lstsq`.
- It is a good alternative if you prefer a matrix formula.

```python
import numpy as np
A = np.array([[1.0, 1.0], [2.0, 2.0]])  # duplicate columns
b = np.array([2.0, 4.0])
print((np.linalg.pinv(A) @ b).round(3))  # [1. 1.]
```

### A.T and @

- `A.T` is the transpose (rows become columns).
- `@` is matrix multiplication. A `(2, 3)` times a `(3,)` gives `(2,)`.

```python
import numpy as np
M = np.array([[1, 2, 3], [4, 5, 6]])
print(M.T.shape)  # (3, 2)
print(M @ np.array([1, 0, 1]))  # [ 4 10]
```

## Common mistakes

- **Forgetting the intercept column.** Without the ones, the line is forced through the origin.
  - Check that your result has `d + 1` entries.
- **Putting the ones column at the end.** The problem says `w[0]` is the intercept, so the ones go in front.
- **Inverting `AᵀA` directly.** It crashes or gives garbage with duplicate columns or fewer samples than weights.
  - Use `lstsq` or `pinv` instead.
- **Forgetting that `lstsq` returns a tuple.** You want only the first item, not the whole tuple.
- **Wrong shape for the ones column.** A 1-D `np.ones(n)` will not stack next to a 2-D `X`.
  - Use shape `(n, 1)`.

## Hints

### Hint 1
- Build `A` by putting a column of ones in front of `X`.
- Ask a least-squares solver for the weights that make `A @ w` as close to `y` as possible.
- Return those weights.

### Hint 2
- Make the ones column with `np.ones`, shape `(n, 1)`.
- Join it to `X` with `np.hstack`, giving `A` with shape `(n, d + 1)`.
- Call `np.linalg.lstsq` on `A` and `y`. It returns a tuple.
- The first item of the tuple is `w`, with shape `(d + 1,)`.

### Hint 3
- The number of rows in the ones column is the first entry of `X.shape`.
- List the ones column first in the stack, so the first weight becomes the intercept.
- The solver already handles the singular case and returns the smallest-norm answer, so you never form `AᵀA` yourself.
- Pick out the first element of what the solver returns and return it.
