# Learn: Confusion Matrix

## The idea

- **Confusion matrix:** a table of counts that shows *how* a classifier is right and wrong, not just how often.
  - Each row is a true class.
  - Each column is a predicted class.
  - Cell `[i, j]` = number of samples that really were class `i` but were predicted as `j`.
- Correct predictions land on the **diagonal** (`i == j`).
  - Everything off the diagonal is a mistake.
  - Its position tells you which two classes get mixed up.
- Where it shows up: almost every classification evaluation report.
  - It is the starting point for precision, recall and F1.
- The task is really a counting job: every sample adds exactly 1 to exactly one cell.
  - The cell is picked by its `(true label, predicted label)` pair.
- The table always has `num_classes` rows and columns.
  - A class that never appears keeps an all-zero row and column.
- **Histogram:** counts of how often each value occurs. Here the "value" is a pair, so it is a 2-D histogram.
- **Fancy indexing:** using integer arrays as an index to pick many array cells at once.

## Work it by hand

Example 1: `y_true = [0, 1, 2, 1]`, `y_pred = [0, 2, 2, 1]`, `num_classes = 3`.

1. Start with a 3×3 table of zeros.
2. Go through the samples one at a time:

| Sample | true | pred | Pair | Cell that gets +1 |
|---|---|---|---|---|
| 0 | 0 | 0 | (0, 0) | row 0, col 0 |
| 1 | 1 | 2 | (1, 2) | row 1, col 2 |
| 2 | 2 | 2 | (2, 2) | row 2, col 2 |
| 3 | 1 | 1 | (1, 1) | row 1, col 1 |

3. The final table:

```text
        pred 0  pred 1  pred 2
true 0     1       0       0
true 1     0       1       1
true 2     0       0       1
```

4. As a list: `[[1,0,0],[0,1,1],[0,0,1]]`, which matches the expected output.
5. Sanity check: all cells add up to 4, the number of samples.

## Tools you'll need

### np.zeros(shape, dtype=int)

- Makes an array filled with zeros.
- The default dtype is float, so ask for an integer type; the problem needs integer counts.

```python
import numpy as np

a = np.zeros((2, 4), dtype=int)
print(a.shape)  # (2, 4)
print(a.dtype)  # int64
```

### Indexing with a pair of arrays

- Two integer arrays as an index pick one cell per position.
  - The first array gives the rows, the second gives the columns.
- The result is 1-D, with one value per position.

```python
import numpy as np

m = np.arange(12).reshape(3, 4)
rows = np.array([0, 2, 1])
cols = np.array([3, 0, 1])
print(m[rows, cols])  # [3 8 5]
```

- This reads cells `(0,3)`, `(2,0)` and `(1,1)`.

### Repeated indices and `+=`

- Careful when the same cell appears twice in the index.
- Plain `+=` with fancy indexing updates each distinct cell once, not once per occurrence.

```python
import numpy as np

c = np.zeros(3, dtype=int)
c[[1, 1, 2]] += 1
print(c)  # [0 1 1]
```

- Cell 1 was listed twice but only went up by 1.

### np.add.at(array, indices, value)

- The "unbuffered" version: it applies the update for every occurrence, so repeats add up.
- It changes the array in place and returns nothing.
- For a 2-D array, pass the indices as a tuple `(rows, cols)`.

```python
import numpy as np

c = np.zeros(3, dtype=int)
np.add.at(c, [1, 1, 2], 1)
print(c)  # [0 2 1]
```

### A plain loop with zip (alternative)

- `for a, b in zip(x, y):` walks through two arrays together.
- It is slower than NumPy tools, but with `n <= 10^5` it is still fine.

```python
import numpy as np

t = np.array([0, 1])
p = np.array([1, 1])
for a, b in zip(t, p):
    print(a, b)
# 0 1
# 1 1
```

## Common mistakes

- **Swapping rows and columns.** Rows are *true* labels, columns are *predicted* labels.
  - Check with Example 2: the two true-1 samples predicted as 0 must land in row 1, column 0.
- **Using `cm[t, p] += 1` with arrays.** Repeated pairs count only once.
  - Use `np.add.at`, or a loop.
- **Sizing the matrix from the data.** `max(y_true) + 1` can be too small when the top classes are missing.
  - Always use `num_classes`.
- **Float output.** `np.zeros(...)` without `dtype=int` gives floats such as `1.0`.
  - Ask for an integer dtype.
- **Mixing up the pair order.** `(true, pred)` is not `(pred, true)`; the result would be the transpose.

## Hints

### Hint 1
- Make an empty square table with one row and one column per class.
- Go through the samples.
- For each one, find the cell named by its true label and predicted label, and add 1 there.
- Return the table.

### Hint 2
- Create the table with `np.zeros`, two sides of `num_classes`, integer dtype.
- Count either with one unbuffered add that takes `(y_true, y_pred)` as the index pair, or with a loop over `zip(y_true, y_pred)`.
- The result keeps shape `(num_classes, num_classes)`.

### Hint 3
- The key is the index: `y_true` picks the row of each sample, `y_pred` picks the column.
- Use the unbuffered add with the value 1, so each occurrence of a repeated pair adds 1.
- In Example 2 the pair (1, 0) appears twice, so cell `[1][0]` must end up as 2.
