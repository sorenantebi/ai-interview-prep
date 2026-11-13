# Learn: Top-K per Row

## The idea

- **The task:** for each row of a score table, find *where* the `k` biggest values sit.
  - You return column indices, not the values themselves.
  - Indices are listed from the biggest value to the smallest.
- **Tie rule:** if two values are equal, the lower column index comes first.
- **Where it shows up:**
  - Top-k accuracy in an evaluation report: "is the right class among the 5 highest-scoring predictions?"
  - Recommenders and retrieval systems: pick the best items per user or query.
- **Axis:** the direction NumPy works along.
  - `axis=1` means within each row (across columns).
  - `axis=0` means within each column (down rows).
- **argsort:** returns the indices that would sort an array, not the sorted values.
- **Stable sort:** a sort that keeps items with equal keys in their original order.
  - This is how you get the tie rule for free.
- **Slicing:** taking a range of rows or columns, such as the first `k` columns.

## Work it by hand

Example 1: `x = [[0.1, 0.9, 0.5], [3.0, 3.0, 1.0]]`, `k = 2`. Shape of `x` is `(2, 3)`.

1. Handle each row on its own. Row 0 is `[0.1, 0.9, 0.5]`, row 1 is `[3.0, 3.0, 1.0]`.
2. Row 0, largest to smallest: 0.9 (col 1), 0.5 (col 2), 0.1 (col 0). Order of columns: `[1, 2, 0]`.
3. Row 1: the two 3.0s tie, so the lower column comes first: col 0, then col 1. Then 1.0 (col 2). Order: `[0, 1, 2]`.
4. Full ordering, shape `(2, 3)`:

```text
[[1, 2, 0],
 [0, 1, 2]]
```

5. Keep only the first `k = 2` columns, shape `(2, 2)`:

```text
[[1, 2],
 [0, 1]]
```

6. This matches the expected output `[[1,2],[0,1]]`.

## Tools you'll need

### np.argsort(a, axis=-1, kind=None)

- Returns the *indices* that would sort the array, smallest value first.
- `axis=1` sorts each row separately; the output has the same shape as the input.
- `kind="stable"` guarantees equal values keep their original order.

```python
import numpy as np

a = np.array([[30, 10, 20], [5, 5, 1]])
print(np.argsort(a, axis=1))  # [[1 2 0]
                              #  [2 0 1]]
print(np.argsort(a, axis=1, kind="stable").shape)  # (2, 3)
```

### Negation to flip the order

- `argsort` goes ascending, so to get "largest first", sort the negated values.
- The biggest number becomes the smallest after the sign flip.
- `-v` makes a new array; the original is untouched.

```python
import numpy as np

v = np.array([4, 9, 1])
print(-v)  # [-4 -9 -1]
print(np.argsort(v))   # [2 0 1]
print(np.argsort(-v))  # [1 0 2]
```

### Slicing columns: `a[:, :k]`

- The first `:` means all rows; `:k` means columns `0` up to (not including) `k`.
- The result has `k` columns.

```python
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m[:, :2])  # [[0 1]
                 #  [4 5]
                 #  [8 9]]
print(m[:, :2].shape)  # (3, 2)
```

### Fancy indexing (optional, for checking your work)

- Passing index arrays picks out elements.
- With `np.arange(n)[:, None]` as the row index and an `(n, k)` array of column indices, you get an `(n, k)` array of values.
- Handy for looking at the values your indices point to.

```python
import numpy as np

m = np.array([[7, 8, 9], [1, 2, 3]])
cols = np.array([[2, 0], [1, 1]])
rows = np.arange(2)[:, None]
print(m[rows, cols])  # [[9 7]
                      #  [2 2]]
```

## Common mistakes

- **Wrong axis.**
  - `axis=0` sorts down columns and gives a wrong answer.
  - Be explicit with `axis=1`.
- **Sorting ascending.**
  - Plain `argsort` puts the smallest first, so the answer is reversed.
  - Negate the values first.
- **Reversing with `[::-1]` to get descending order.**
  - This breaks the tie rule: equal values end up with the *higher* index first.
  - Negate instead.
- **Forgetting the stable sort.**
  - The default sort doesn't guarantee ties stay in index order.
  - Pass `kind="stable"`.
- **Returning values instead of indices.**
  - `np.sort` gives values; the task wants column indices, which `argsort` gives.

## Hints

### Hint 1
- Put every row's column indices in order from largest value to smallest.
- Keep only the first `k` of them.
- Equal values must stay in their original column order.

### Hint 2
- Make the values negative, so ascending order becomes largest-first.
- Use `np.argsort` along `axis=1` with a stable sort: shape `(n, d)`.
- Slice columns to get shape `(n, k)`.

### Hint 3
- A stable sort leaves equal keys in their original left-to-right order, so ties keep the lower column index first.
- Sorting the negated array ascending puts the largest original values first.
- So: argsort the negated array along each row with `kind="stable"`, then take all rows and the first `k` columns of the result.
