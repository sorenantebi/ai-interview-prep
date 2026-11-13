# Learn: Min-Max Scale Columns

## The idea

- **Min-max scaling** squeezes every column into the range 0 to 1.
  - The smallest value in a column becomes `0`, the largest becomes `1`.
  - Everything else lands in between, in proportion.
- Each column is handled on its own, so house sizes and room counts both end up on the same 0 to 1 scale.
- It shows up in feature pipelines before training.
  - Models like k-nearest neighbours or gradient descent on linear models behave badly when one feature is in the millions and another is between 0 and 5.
  - Scaling puts them on equal footing.
- **Reduction**: an operation that collapses many numbers into one, such as `min`, `max` or `sum`.
  - With `axis=0` it collapses the rows, so you get one result per column.
- **Broadcasting**: NumPy stretches the smaller array to fit when shapes differ.
  - A shape `(d,)` array combined with a shape `(n, d)` array is applied to every row.
- **Span**: `max - min` of a column, the width of its range.
- A **constant column** has span `0`, so the formula would compute `0 / 0`.
  - The task says such a column must become all `0.0`.

## Work it by hand

Example 1: `x = [[1, 10], [3, 10], [2, 10]]`, shape `(3, 2)`.

1. Column minimums (down the rows): `[1, 10]`, shape `(2,)`.
2. Column maximums: `[3, 10]`, shape `(2,)`.
3. Spans (max minus min): `[2, 0]`, shape `(2,)`.
   - The second column is constant, so its span is zero. That is the danger spot.
4. Subtract the minimums from every row (broadcasting), shape `(3, 2)`:

| row | x - min |
|---|---|
| 0 | `[0, 0]` |
| 1 | `[2, 0]` |
| 2 | `[1, 0]` |

5. Divide by the spans.
   - First column: divide by `2`, giving `0, 1, 0.5`.
   - Second column: every numerator is already `0`, so the answer must be `0`.
   - Dividing by any nonzero number gives `0`; dividing by `0` gives `nan`.
6. Result: `[[0, 0], [1, 0], [0.5, 0]]`, which matches the expected output.

## Tools you'll need

### arr.min(axis=0) and arr.max(axis=0)

- Reduce along the rows, giving one value per column.
- `axis=1` would give one value per row instead.
- The reduced axis disappears, so a `(n, d)` input gives shape `(d,)`.

```python
import numpy as np

a = np.array([[4.0, 9.0, 1.0],
              [6.0, 2.0, 5.0]])
print(a.min(axis=0))  # [4. 2. 1.]
print(a.max(axis=1))  # [9. 6.]
print(a.min(axis=0).shape)  # (3,)
```

### Broadcasting

- Shapes are compared from the right; a dimension of size 1 (or a missing one) is stretched.
- A `(d,)` array lines up with the last axis of `(n, d)`, so it is applied to every row.

```python
import numpy as np

a = np.array([[10.0, 20.0, 30.0],
              [40.0, 50.0, 60.0]])
b = np.array([1.0, 2.0, 3.0])
print((a - b).shape)  # (2, 3)
print(a / b)
# [[10. 10. 10.]
#  [40. 25. 20.]]
```

### np.where(cond, a, b)

- Builds an array element by element: where `cond` is True take from `a`, otherwise from `b`.
- Handy for swapping out only the bad entries.

```python
import numpy as np

v = np.array([3.0, 0.0, 7.0, 0.0])
print(np.where(v == 0, -1.0, v))  # [ 3. -1.  7. -1.]
```

### Division by zero

- Dividing a float array by `0.0` does not raise an error.
  - `0/0` gives `nan`, and `x/0` gives `inf`, plus a warning.
- So zero spans must be replaced before dividing.

```python
import numpy as np

print(np.array([0.0, 5.0]) / np.array([0.0, 0.0]))  # [nan inf]
```

## Common mistakes

- **Wrong axis.**
  - `axis=0` gives per-column results; `axis=1` scales each row, a different task.
  - Check that your min has shape `(d,)`.
- **Dividing by zero.**
  - Constant columns give `0/0 = nan`.
  - Fix the spans before the division, not after.
- **Patching the output instead of the divisor.**
  - Swapping zero spans for a harmless nonzero number is simpler than hunting for `nan` afterwards.
- **Changing the input.**
  - Avoid `x -= ...` or other in-place operations.
  - The task wants a new array, and the caller's `x` should stay untouched.
- **Integer arrays.**
  - Here the input is float, so `/` is fine.
  - With int data, check the dtype before assuming the result is float.

## Hints

### Hint 1
- Find the smallest and largest value of each column.
- Work out how wide each column's range is.
- Make sure a range of zero cannot cause a division by zero.
- Subtract the minimum from every value, then divide by the range, for all columns at once.

### Hint 2
- Use `min(axis=0)` and `max(axis=0)`, each giving shape `(d,)`.
- Subtract them to get the spans, also shape `(d,)`.
- Use `np.where` to replace zero spans with a harmless number, still shape `(d,)`.
- Broadcasting lets `(n, d)` combine with `(d,)` in both the subtraction and the division, giving `(n, d)`.

### Hint 3
- For a constant column, the numerator `v - min` is `0` for every row.
- So any nonzero divisor gives `0`, which is what the task wants.
- Pick the divisor per column as: the span if it is not zero, otherwise `1`.
- Each output value is then `(v - min_j) / divisor_j`, computed for the whole array in one expression.
