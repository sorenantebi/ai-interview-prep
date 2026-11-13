# Learn: Stable Softmax

## The idea

- **Task:** turn each row of raw scores into probabilities that are positive and add up to 1.
- **Where it shows up:** it is the last step of almost every classifier, and it sits inside the cross-entropy loss used in training.
- **Logits:** the raw scores a model outputs, one per class for each example.
  - They can be any real number, so they are not probabilities yet.
- **Softmax:** exponentiate each score, then divide by the sum of those exponentials.
  - Bigger logits get bigger probabilities.
- **The catch:** `exp` grows extremely fast.
  - `np.exp(1000.0)` is too big for a float and becomes `inf`.
  - Then `inf / inf` gives `nan`.
- **The trick:** subtracting the same number from every score in a row does not change the softmax.
  - The extra factor appears in the top and bottom of the fraction and cancels.
- **Best number to subtract:** the row's maximum.
  - The biggest exponent becomes `exp(0) = 1`, so nothing overflows.
- **Per row:** each row is its own example, so the max and the sum are computed per row.
- **Broadcasting:** NumPy's rule for combining arrays of different shapes.
  - A `(n, 1)` column is stretched across the `k` columns of an `(n, k)` array automatically.

## Work it by hand

Start with `x = [[1.0, 2.0, 3.0]]`, shape `(1, 3)`.

| Step | Result | Shape |
|---|---|---|
| 1. Row max | `[[3.0]]` | `(1, 1)` |
| 2. Subtract max | `[[-2, -1, 0]]` | `(1, 3)` |
| 3. Exponentiate | `[[0.13534, 0.36788, 1.0]]` | `(1, 3)` |
| 4. Row sum | `[[1.50321]]` | `(1, 1)` |
| 5. Divide | `[[0.09003, 0.24473, 0.66524]]` | `(1, 3)` |

- **Check step 5:**
  - `0.13534 / 1.50321 = 0.09003`
  - `0.36788 / 1.50321 = 0.24473`
  - `1.0 / 1.50321 = 0.66524`
- The three values add up to 1 and match the expected output `[[0.09003, 0.24473, 0.66524]]`.

## Tools you'll need

### `arr.max(axis=1, keepdims=True)`

- Returns the maximum along an axis.
  - `axis=1` means "across the columns", so you get one value per row.
- `keepdims=True` keeps that axis with size 1.
  - The result stays 2-D and can broadcast against the original array.

```python
import numpy as np

a = np.array([[1, 5, 2], [7, 0, 3]])
print(a.max(axis=1))  # [5 7]
print(a.max(axis=1).shape)  # (2,)
print(a.max(axis=1, keepdims=True).shape)  # (2, 1)
```

### `arr.sum(axis=..., keepdims=...)`

- Works like `max`, but adds the values up.
- `axis=0` collapses the rows, giving one value per column.
- `axis=1` collapses the columns, giving one value per row.

```python
import numpy as np

d = np.array([[2, 4, 6], [1, 1, 1]])
print(d.sum(axis=1))  # [12  3]
print(d.sum(axis=0))  # [3 5 7]
print(d.sum(axis=1, keepdims=True).shape)  # (2, 1)
```

### Broadcasting with `-` and `/`

- Combining an `(n, k)` array with an `(n, 1)` array repeats the column across all `k` columns.
  - This subtracts or divides each row by its own number, with no loop.
- If the second array had shape `(n,)`, NumPy would line it up with the columns instead.
  - That either fails or gives a wrong answer.

```python
import numpy as np

b = np.array([[10, 20, 30], [40, 50, 60]])
c = np.array([[1], [2]])
print((b - c).shape)  # (2, 3)
print((b - c)[1])  # [38 48 58]
```

### `np.exp(a)`

- Computes `e**a` for every element and keeps the shape.
- Large positive inputs overflow to `inf`.
- Large negative inputs become `0.0`, which is harmless here.

```python
import numpy as np

print(np.exp(np.array([0.0, 1.0])))  # [1.         2.71828183]
print(np.exp(-1000.0))  # 0.0
print(np.exp(1000.0))  # inf
```

- The last line also prints an overflow warning to stderr.
  - That is the problem you are avoiding.

## Common mistakes

- **Wrong axis:** each row is one example, so reduce over `axis=1`.
  - With `axis=0` you would normalize columns, and the rows would not sum to 1.
- **Forgetting `keepdims=True`:** a max of shape `(n,)` lines up with the columns, not the rows.
  - Keep the shape `(n, 1)`.
- **Skipping the max subtraction:** it works on `[1, 2, 3]`, then returns `nan` for `1000.0`.
  - Test with the large values from Example 2.
- **Using a global max:** `x.max()` with no axis uses one number for the whole array.
  - A row with very small scores could underflow to all zeros, giving `0 / 0`. Use one max per row.
- **Modifying the input in place:** `x -= ...` changes the caller's array.
  - It also fails if `x` holds integers. Create a new array instead.

## Hints

### Hint 1
- Make each row safe by subtracting that row's largest score from every entry in it.
- Exponentiate the result.
- Divide each row by its own total.

### Hint 2
- Take the max along `axis=1` with `keepdims=True`, giving shape `(n, 1)`. Subtract it from `x` to get shape `(n, k)`.
- Apply `np.exp`, which keeps shape `(n, k)`.
- Sum along `axis=1` with `keepdims=True`, giving shape `(n, 1)`.
- Divide the `(n, k)` array by that column.

### Hint 3
- For row `i`, let `m_i` be its maximum. The shifted value is `x[i, j] - m_i`, and its exponential is `e[i, j]`.
- The answer is `e[i, j]` divided by the sum of `e[i, :]`.
- Both `m_i` and that sum must stay as columns of shape `(n, 1)`.
  - Then broadcasting applies each row's number to that row only.
- Each output row then sums to 1.
