# Learn: Replace Outliers

## The idea

- **Outlier**: a value far from the rest of its column. Here "far" means more than 3 standard deviations from the column mean.
- **Standard deviation (std)**: how spread out a column is.
  - Small std means values cluster tightly.
  - Large std means they are scattered.
- **Population std** (`ddof=0`): divides by `n`, not `n - 1`. This is NumPy's default.
- **Median**: the middle value after sorting. One huge value can't drag it around, which makes it a safe replacement.
- The task: for each column, find the outliers and swap them for that column's median.
- Where it shows up: feature pipelines, where you clean data before training or before computing statistics that outliers would distort.
- "Each column separately" means each statistic is one number per column, so a `(n, d)` array gives `d` means, `d` stds and `d` medians.
- **Broadcasting**: NumPy stretches a shape `(d,)` vector across all `n` rows of a `(n, d)` array, so you can compare the whole array against the `d` numbers at once.
- **Mask**: a boolean array that is `True` where a condition holds.

## Work it by hand

Example 1 has `n = 11` rows and `d = 2` columns.

1. Column 0 is ten `1.0`s and one `100.0`.
   - mean = (10 × 1 + 100) / 11 = 10.0
   - deviations: ten values of `-9`, one value of `+90`
   - variance = (10 × 81 + 8100) / 11 = 8910 / 11 = 810
   - std = sqrt(810) ≈ 28.46, so 3 × std ≈ 85.38
   - sorted, the 6th of 11 values is `1.0`, so the median is `1.0`
2. Column 1 is `5.0` six times and `6.0` five times.
   - mean = 60 / 11 ≈ 5.4545
   - std ≈ 0.498, so 3 × std ≈ 1.49
   - median (6th of 11 sorted values) = `5.0`
3. Collect the statistics. Each has shape `(2,)`.

| Statistic | Column 0 | Column 1 |
|---|---|---|
| mean | 10.0 | 5.4545 |
| 3 × std | 85.38 | 1.49 |
| median | 1.0 | 5.0 |

4. Apply the test `|v - mean| > 3 * std`.
   - Column 0: each `1.0` gives `9`, which is not above 85.38. The `100.0` gives `90`, which is above 85.38, so it is an outlier.
   - Column 1: every deviation is at most about 0.55, below 1.49, so there are no outliers.
   - The mask has shape `(11, 2)`, with a single `True` at row 10, column 0.
5. Replace that one entry with the column 0 median, `1.0`.
   - The last row goes from `[100.0, 5.0]` to `[1.0, 5.0]`.
   - Every other row is unchanged, which matches the expected output.

## Tools you'll need

### `arr.mean(axis=0)` and `arr.std(axis=0)`

- `axis=0` collapses the rows, giving one value per column.
- `std` uses `ddof=0` by default, which is what the problem wants.
- `keepdims=True` keeps the reduced axis with length 1.

```python
import numpy as np
c = np.array([[1., 10.], [3., 10.]])
print(c.mean(axis=0))  # [ 2. 10.]
print(c.std(axis=0))   # [1. 0.]
print(c.mean(axis=0).shape, c.mean(axis=0, keepdims=True).shape)  # (2,) (1, 2)
```

### `np.median(arr, axis=0)`

- Returns the middle value of each column.
- With an even count, it averages the two middle values.

```python
import numpy as np
m = np.array([[1., 9.], [7., 3.], [4., 5.]])
print(np.median(m, axis=0))          # [4. 5.]
print(np.median([1., 2., 3., 10.]))  # 2.5
```

### Broadcasting arithmetic

- Subtracting a shape `(d,)` vector from a `(n, d)` array subtracts it from every row.
- The trailing dimensions must match.

```python
import numpy as np
m = np.array([[1., 2., 3.], [4., 5., 6.]])
v = np.array([1., 2., 3.])
print((m - v).shape)  # (2, 3)
print(m - v)
# [[0. 0. 0.]
#  [3. 3. 3.]]
```

### `np.abs` and comparisons

- `np.abs` works element by element.
- Comparing an array with a number or a broadcastable array gives a boolean mask.

```python
import numpy as np
v = np.array([-2., 1., 5.])
print(np.abs(v) > 1.5)  # [ True False  True]
```

### `np.where(cond, a, b)`

- Builds a new array: `a` where `cond` is `True`, `b` elsewhere.
- All three arguments broadcast, so `a` can be a per-column vector.
- The inputs are not modified.

```python
import numpy as np
arr = np.array([[1., 2.], [3., 4.]])
mask = np.array([[True, False], [False, True]])
fill = np.array([10., 20.])
print(np.where(mask, fill, arr))
# [[10.  2.]
#  [ 3. 20.]]
```

## Common mistakes

- **Wrong axis.** `axis=1` gives one statistic per row. You need `axis=0`.
- **Sample std instead of population std.** `ddof=1` shifts the threshold slightly. Keep the default `ddof=0`.
- **Computing statistics after replacing.** Mean, std and median must all come from the original column, outliers included. Compute them first, then replace.
- **Modifying `x` in place.** `x[mask] = ...` changes the caller's array. Build a new array instead.
- **Constant columns.**
  - Std is `0` and all deviations are `0`.
  - Since `0 > 0` is `False`, nothing is flagged.
  - Use strict `>`, not `>=`, or the whole column would be flagged.

## Hints

### Hint 1
- Compute three per-column statistics from the original data: mean, std and median.
- Use them to mark which entries are outliers.
- Build a new array that takes the median at those spots and the original value everywhere else.

### Hint 2
- Mean, std and median are reductions along `axis=0`. Each has shape `(d,)`.
- Subtracting the mean broadcasts to shape `(n, d)`.
- Comparing the absolute deviation with the threshold gives a boolean mask of shape `(n, d)`.
- `np.where` then chooses between the median vector and `x`, giving shape `(n, d)`.

### Hint 3
- For every entry, take its distance from its own column's mean, in absolute value.
- Compare that distance with three times its own column's std.
- If the distance is strictly larger, the entry is an outlier, and the mask is `True` there.
- Pass the mask, the median vector and `x` to `np.where`.
- Make sure the result is a float array.
