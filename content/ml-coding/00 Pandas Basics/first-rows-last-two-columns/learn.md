# Learn: First Rows, Last Two Columns

## The idea

- A **DataFrame** is a table: rows run down, columns run across.
- The task: cut a rectangle out of the table, keeping the first `n` rows and the last two columns.
- You pick them by **position** (0, 1, 2, ...), not by name.
- Where it shows up in data work:
  - Peeking at a corner of a big table.
  - Splitting features from a label that sits in the last columns.
  - Trimming a frame before an evaluation report.
- **Index**: the row labels on the left (by default 0, 1, 2, ...).
- **Selecting by position**: means "the 3rd row", not "the row labelled 3".
- **Slice**: `a:b` means "from `a` up to, but not including, `b`".
- **Negative position**: counts from the end, so -1 is the last item.

## Work it by hand

Example 1: `n = 2`, and the table is:

| index | a | b | c |
|---|---|---|---|
| 0 | 1 | 4 | 7 |
| 1 | 2 | 5 | 8 |
| 2 | 3 | 6 | 9 |

1. **Rows.** The first 2 rows are positions 0 and 1.
   - Row 2 is dropped.
   - Shape goes from (3, 3) to (2, 3).
2. **Columns.** Count positions from the right: `c` is -1, `b` is -2, `a` is -3.
   - The last two columns are `b` and `c`.
   - Column `a` is dropped.
   - Shape is now (2, 2).
3. **Keep labels.** The index stays 0, 1 and the names stay `b`, `c`.
   - Nothing is renumbered or renamed.

Result:

| index | b | c |
|---|---|---|
| 0 | 4 | 7 |
| 1 | 5 | 8 |

- That is `{"b": [4, 5], "c": [7, 8]}`, the expected output.

## Tools you'll need

### df.iloc[rows, cols]

- **`iloc`** selects by integer position.
- Inside the brackets: a row selector, a comma, then a column selector.
- Each selector can be a number, a list, or a slice.
- It keeps the original index and column names.

```python
import pandas as pd

df = pd.DataFrame({"u": [10, 20, 30], "v": [1, 2, 3]}, index=["r1", "r2", "r3"])
print(df.iloc[1, 0])  # 20
print(df.iloc[[0, 2], [1]].shape)  # (2, 1)
print(df.iloc[[0, 2], [1]].index.tolist())  # ['r1', 'r3']
```

### Slices with `:`

- `a:b` runs from `a` up to but not including `b`.
- Leaving `a` out means "from the start".
- Leaving `b` out means "to the end".
- A bare `:` means "everything".

```python
import numpy as np

x = np.array([5, 6, 7, 8, 9])
print(x[:2])  # [5 6]
print(x[1:4])  # [6 7 8]
print(x[2:])  # [7 8 9]
```

### Negative positions

- A negative number counts from the end: -1 is the last item, -2 the second to last.
- A slice starting at a negative number and with no end runs to the last item.
- That works no matter how wide the table is.

```python
import numpy as np

x = np.array([5, 6, 7, 8, 9])
print(x[-1])  # 9
print(x[-3:])  # [7 8 9]
print(x[:-3])  # [5 6]
```

### Slice longer than the data

- A slice never raises an error if it asks for too much.
- It just returns what exists.
- Asking for zero rows gives an empty frame that still has its columns.

```python
import pandas as pd

df = pd.DataFrame({"p": [1, 2], "q": [3, 4]})
print(df.iloc[:10, :].shape)  # (2, 2)
print(df.iloc[:0, :].shape)  # (0, 2)
```

## Common mistakes

- **Using `.loc` for positions.**
  - `.loc` works with labels, and its slices include the end label.
  - Use `.iloc` so slices behave like normal Python slices.
- **Off-by-one on rows.**
  - `:n` gives exactly `n` rows (positions 0 to n-1).
  - Don't write `:n-1` or `:n+1`.
- **Hard-coding column names.**
  - The frame can have up to 100 columns with any names.
  - Count from the right with a negative slice instead.
- **Mixing up the comma.**
  - Rows come first, columns second.
  - Chaining two slices like `df.iloc[:n][-2:]` slices rows twice and gives the wrong thing.
- **Resetting the index.**
  - The task wants the original index kept.
  - Don't call `reset_index`, and don't rebuild the frame from scratch.

## Hints

### Hint 1

- You need one selection that makes two cuts at once.
- Cut 1: keep the first `n` rows.
- Cut 2: keep the last two columns.
- Both cuts are by position.
- The index and column names must come along unchanged.

### Hint 2

- Use `.iloc`, which takes a row selector and a column selector separated by a comma.
- Rows: a slice from the start. The result has at most `n` rows.
- Columns: a slice counted from the right end. The result has 2 columns.
- The final shape should be `(n, 2)`, or fewer rows if `n` is bigger than the frame.

### Hint 3

- For the rows, the slice "up to `n`" with the start left out gives positions 0 to n-1.
- For the columns, a slice that starts at position -2 and has no end runs from the second-to-last column to the last one.
- Put the row slice first, then a comma, then the column slice, all inside the `.iloc` brackets.
