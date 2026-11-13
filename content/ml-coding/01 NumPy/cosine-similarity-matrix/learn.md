# Learn: Cosine Similarity Matrix

## The idea

- The task: for every row of `a` and every row of `b`, measure how much the two vectors point the same way, and collect all the answers in an `(n, m)` table.
- **Cosine similarity** compares direction and ignores length.
  - `1` means same direction.
  - `0` means at right angles.
  - `-1` means opposite directions.
- The formula is `a·b / (|a| · |b|)`.
- **Dot product** (`a·b`): multiply matching entries, then add them up.
- **Norm** (`|a|`): the length of a vector, the square root of the sum of its squares.
- It shows up in ML and data work in several places:
  - comparing text or image embeddings
  - nearest-neighbour search
  - recommendation systems
  - retrieval evaluation reports
- **Broadcasting**: NumPy stretches size-1 axes so arrays of different shapes can be combined. A column of shape `(n, 1)` divides an `(n, d)` array row by row.
- **Matrix product** (`@`): computes the dot product of every row of one array with every column of another, in one step.
- Think about what the formula becomes when both vectors already have length 1.

## Work it by hand

Example 1: `a = [[1, 0], [1, 1]]`, `b = [[2, 0], [0, 3]]`.

1. **Lengths of the rows of a** (shape `(2, 1)` if you keep the column):
   - `[1, 0]` → `sqrt(1 + 0) = 1`
   - `[1, 1]` → `sqrt(1 + 1) = 1.41421`
2. **Lengths of the rows of b:**
   - `[2, 0]` → `2`
   - `[0, 3]` → `3`
3. **Divide each row by its length** (each row now has length 1):
   - a becomes `[[1, 0], [0.70711, 0.70711]]`
   - b becomes `[[1, 0], [0, 1]]`
4. **Dot every a-row with every b-row.** Entry `[i, j]` pairs row `i` of a with row `j` of b:

| | b row 0 `[1, 0]` | b row 1 `[0, 1]` |
|---|---|---|
| a row 0 `[1, 0]` | `1·1 + 0·0 = 1` | `1·0 + 0·1 = 0` |
| a row 1 `[0.70711, 0.70711]` | `0.70711` | `0.70711` |

```text
[[1.00000, 0.00000],
 [0.70711, 0.70711]]
```

- This matches the expected output.
- Step 4 is one matrix product: unit a times the transpose of unit b.

## Tools you'll need

### `a * a` and `np.sqrt`

- `*` multiplies element by element, so `x * x` squares every entry.
- `np.sqrt` takes the square root of every entry.

```python
import numpy as np
v = np.array([[3.0, 4.0], [1.0, 2.0]])
print((v * v).tolist())  # [[9.0, 16.0], [1.0, 4.0]]
print(np.sqrt(np.array([9.0, 16.0, 2.0])))  # [3.         4.         1.41421356]
```

### `arr.sum(axis=1, keepdims=True)`

- `axis=1` adds across columns, giving one value per row.
- `keepdims=True` keeps that axis with size 1, so the result is a column that broadcasts against the original.

```python
import numpy as np
x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(x.sum(axis=1).shape)                 # (2,)
print(x.sum(axis=1, keepdims=True).shape)  # (2, 1)
print(x.sum(axis=1, keepdims=True))
# [[ 6.]
#  [15.]]
```

### Broadcasting

- When shapes differ, NumPy stretches size-1 axes to match.
- An `(n, d)` array divided by an `(n, 1)` column divides each row by its own number.

```python
import numpy as np
x = np.array([[2.0, 4.0], [9.0, 3.0]])
scale = np.array([[2.0], [3.0]])
print((x / scale).tolist())  # [[1.0, 2.0], [3.0, 1.0]]
```

### `np.where(cond, a, b)`

- Picks from `a` where `cond` is true and from `b` elsewhere, element by element.
- Useful for swapping out unwanted values (like zeros) before a division.

```python
import numpy as np
v = np.array([0.0, 5.0, 0.0, 2.0])
print(np.where(v == 0, -1.0, v))  # [-1.  5. -1.  2.]
```

### `arr.T` and `@`

- `.T` swaps rows and columns: `(m, d)` becomes `(d, m)`.
- `@` is the matrix product: `(n, d) @ (d, m)` gives `(n, m)`.
- Entry `[i, j]` is row `i` of the left dotted with column `j` of the right.

```python
import numpy as np
p = np.array([[1, 2, 3], [4, 5, 6]])   # (2, 3)
q = np.array([[1, 0, 1]])              # (1, 3)
print(q.T.shape)           # (3, 1)
print((p @ q.T).tolist())  # [[4], [10]]
```

## Common mistakes

- **Wrong axis for the norm.**
  - You want one length per row, so sum over `axis=1`.
  - `axis=0` gives column lengths and the shapes won't line up.
- **Forgetting `keepdims=True`.**
  - A `(n,)` vector divided into an `(n, d)` array broadcasts along the wrong axis, or errors.
  - Keep the column shape `(n, 1)`.
- **Dividing by a zero norm.**
  - `0/0` gives `nan`, not `0.0`.
  - Fix the zero norms *before* dividing, so a zero row stays all zeros.
- **Forgetting to transpose `b`.**
  - `a @ b` fails unless `d` equals `m`.
  - You need `b` as `(d, m)`.
- **Changing the input in place.**
  - `a /= norms` modifies the caller's array.
  - Create new arrays instead.

## Hints

### Hint 1
- Turn each row of both arrays into a vector of length 1.
- Then every cosine similarity is a plain dot product, and all of them can be computed at once.
- Handle zero-length rows so they don't cause a division by zero.

### Hint 2
- Row lengths: square the array, sum over `axis=1` with `keepdims=True`, take the square root. The results have shapes `(n, 1)` and `(m, 1)`.
- Use `np.where` to replace zero lengths, then divide by broadcasting. The arrays keep shapes `(n, d)` and `(m, d)`.
- Finish with one matrix product of `(n, d)` and `(d, m)`, giving `(n, m)`.

### Hint 3
- A zero row has length 0, and dividing by 0 gives `nan`.
- If you divide that row by 1 instead, it stays all zeros, and its dot product with anything is `0.0`, which is what the problem asks for.
- So build "safe lengths": the length where it is nonzero, `1` where it is zero.
- Divide each array by its own safe lengths.
- Multiply the normalised `a` by the transpose of the normalised `b`.
