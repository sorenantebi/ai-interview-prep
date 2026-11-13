# Learn: Row, Column and Overall Aggregates

## The idea

- The task: squeeze a 2D table of numbers down to four summaries, using one NumPy call per summary.
- A **reduction** boils many numbers down to fewer: a sum, a mean, a maximum.
- An array of shape `(n, d)` has `n` rows and `d` columns.
- The **axis** says which direction to reduce in.
  - `axis=0` runs down the rows, so it walks through each column.
  - `axis=1` runs across the columns, so it walks through each row.
- The rule to remember: **the axis you name is the one that disappears.**
  - `axis=1` removes the `d` dimension, leaving one value per row, shape `(n,)`.
  - `axis=0` removes the `n` dimension, leaving one value per column, shape `(d,)`.
  - No axis removes everything, leaving a single number.
- **`argmax`** is a cousin of `max`: instead of the largest value, it returns the *position* (index) of the largest value.
- Where it shows up in ML and data work:
  - per-feature means when normalising a dataset,
  - per-sample sums in a loss,
  - `argmax` to turn class scores into predicted labels.

## Work it by hand

Example 1: `x = [[1, 2, 3], [4, 5, 6]]`, shape `(2, 3)`.

| Step | What we do | Result | Shape |
|---|---|---|---|
| 1 | Add each row: 1+2+3 and 4+5+6 | `[6, 15]` | `(2,)` |
| 2 | Average each column: (1+4)/2, (2+5)/2, (3+6)/2 | `[2.5, 3.5, 4.5]` | `(3,)` |
| 3 | Largest of all six entries | `6` | single number |
| 4 | Per column, which row holds the bigger value? Column 0: 1 vs 4, row 1. Column 1: 2 vs 5, row 1. Column 2: 3 vs 6, row 1. | `[1, 1, 1]` | `(3,)` |

- Final answer: `([6, 15], [2.5, 3.5, 4.5], 6, [1, 1, 1])`, which matches the expected output.
- Steps 1 and 2 give different shapes, `(2,)` and `(3,)`.
  - If your shape is the wrong one, you used the wrong axis.

## Tools you'll need

### `a.sum(axis=...)`

- Adds up entries; the named axis collapses.
- No axis adds everything.
- Works as a method (`a.sum(...)`) or a function (`np.sum(a, ...)`).

```python
import numpy as np
a = np.array([[1, 0, 2], [3, 1, 1]])
print(a.sum(axis=0))  # [4 1 3]
print(a.sum(axis=1))  # [3 5]
print(a.sum())        # 8
print(a.sum(axis=1).shape)  # (2,)
```

### `a.mean(axis=...)`

- Same idea as `sum`, but divides by how many entries were collapsed.
- The result is always a float.

```python
import numpy as np
a = np.array([[2.0, 10.0], [4.0, 20.0], [6.0, 30.0]])
print(a.mean(axis=0))  # [ 4. 20.]
print(a.mean(axis=1))  # [ 6. 12. 18.]
print(a.mean(axis=0).shape)  # (2,)
```

### `a.max(axis=...)`

- Returns the largest value.
- Without an axis it looks at the whole array and gives one number.

```python
import numpy as np
a = np.array([[5, -1], [2, 8], [7, 0]])
print(a.max())        # 8
print(a.max(axis=0))  # [7 8]
print(a.max(axis=1))  # [5 8 7]
```

### `a.argmax(axis=...)`

- Returns the *index* of the largest value along the named axis.
- If the maximum appears several times, the first index wins.
- Without an axis, it indexes into the flattened array, which is not what you want per column.

```python
import numpy as np
a = np.array([[5, -1], [2, 8], [7, 0]])
print(a.argmax(axis=0))  # [2 1]
print(a.argmax(axis=1))  # [0 1 0]
print(np.array([4, 9, 9]).argmax())  # 1
```

## Common mistakes

- **Swapping the axes.** "Row sums" means one number per row, so the columns collapse: `axis=1`.
  - Check your output shape against `(n,)` or `(d,)` before moving on.
- **Reading `axis=0` as "along rows".** It means "collapse the row dimension", giving one result per column.
  - Use the "named axis disappears" rule instead of memorising words.
- **Calling `argmax` without an axis.** That returns one index into the flattened array, not one row index per column.
  - Pass `axis=0` for per-column answers.
- **Mixing up `max` and `argmax`.** `max` returns values, `argmax` returns positions.
  - You need `max` for output 3 and `argmax` for output 4.
- **Writing loops.** They work but are slow and unnecessary here.
  - Each output is a single reduction call.

## Hints

### Hint 1

- You need four separate reductions on the same array.
- Each differs only in which axis it collapses, or whether it collapses everything.
- Return the four results together as a tuple, in the order the problem lists them.

### Hint 2

- Row sums: `sum`, result shape `(n,)`.
- Column means: `mean`, result shape `(d,)`.
- Overall maximum: `max`, result is a single number.
- Column argmax: `argmax`, result shape `(d,)` of integers.
- Only the axis argument changes between them.

### Hint 3

- The axis you name is the one that vanishes.
  - Per-row results need the column dimension to vanish, so use axis 1.
  - Per-column results need the row dimension to vanish, so use axis 0.
- The overall maximum takes no axis at all.
- For ties, do nothing extra: `argmax` already returns the first index.
