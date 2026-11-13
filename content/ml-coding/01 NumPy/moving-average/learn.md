# Learn: Moving Average

## The idea

- **Moving average** (also "rolling mean"): slide a window of `k` values along the array and take the mean at each position.
  - For `[1, 2, 3, 4, 5]` with `k = 2`, you average `(1, 2)`, `(2, 3)`, `(3, 4)`, `(4, 5)`.
  - Each step moves the window one place to the right.
- The output has `n - k + 1` values, one per window position.
- It shows up whenever noisy data needs smoothing: training-loss curves, sensor streams, daily metrics in an evaluation report, rolling features in a pipeline.
- The slow way recomputes a sum of `k` numbers for every window, which costs `O(n * k)`.
- **Cumulative sum** (or prefix sum): an array where each entry is the total of everything up to that point.
  - Any window sum is the difference of two entries, so all windows come from one subtraction.
- **Vectorised**: NumPy works on whole arrays at once, with no Python loop.
- **Slicing**: `a[m:]` and `a[:-m]` give shifted views of the same array, which line up for element-wise arithmetic.

## Work it by hand

Take `x = [1.0, 2.0, 3.0, 4.0, 5.0]`, `k = 2`. The output must have `n - k + 1 = 4` values.

1. Build running totals with a `0` in front: `c = [0, 1, 3, 6, 10, 15]` (length 6, one longer than `x`).
2. A window sum is the total up to its end minus the total before its start.
   - Window 0 covers `x[0:2]`: `c[2] - c[0] = 3 - 0 = 3`.
3. Do all windows at once with two slices of `c`:
   - End totals, `c` from index `k` on: `[3, 6, 10, 15]`.
   - Start totals, `c` without its last `k` entries: `[0, 1, 3, 6]`.
4. Subtract element by element: `[3, 5, 7, 9]`. These are the window sums.
5. Divide by `k = 2`: `[1.5, 2.5, 3.5, 4.5]`.

Expected output: `[1.50000, 2.50000, 3.50000, 4.50000]`.

| window | start total | end total | sum | mean |
|---|---|---|---|---|
| `x[0:2]` | 0 | 3 | 3 | 1.5 |
| `x[1:3]` | 1 | 6 | 5 | 2.5 |
| `x[2:4]` | 3 | 10 | 7 | 3.5 |
| `x[3:5]` | 6 | 15 | 9 | 4.5 |

## Tools you'll need

### np.cumsum(a, dtype=None)

- Returns the running total of a 1-D array; the result has the same length as the input.
- Pass `dtype=float` so the totals are floats even if the input is ints.

```python
import numpy as np

a = np.array([2, 5, 1, 4])
print(np.cumsum(a))  # [ 2  7  8 12]
print(np.cumsum(a, dtype=float))  # [ 2.  7.  8. 12.]
```

### np.concatenate([a, b])

- Joins arrays end to end; pass the arrays in a list.
- For 1-D arrays the lengths add up, so it can put a leading value in front of an array.

```python
import numpy as np

a = np.array([7.0, 8.0])
b = np.concatenate([[0.0], a])
print(b)  # [0. 7. 8.]
print(b.shape)  # (3,)
```

### Slicing: `a[m:]` and `a[:-m]`

- `a[m:]` drops the first `m` items; `a[:-m]` drops the last `m` items.
- Both have length `len(a) - m`, so they can be subtracted element by element.

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a[3:])  # [40 50]
print(a[:-3])  # [10 20]
print(a[3:] - a[:-3])  # [30 30]
```

- Careful: `a[:-0]` is an empty array, not the whole array. Here `k >= 1`, so it is safe.

### Element-wise arithmetic and division

- Operators like `-` and `/` work on whole arrays of equal shape.
- `/` with a plain number divides every element; in Python 3 it always gives floats.

```python
import numpy as np

s = np.array([6.0, 9.0, 12.0])
print(s / 3)  # [2. 3. 4.]
print(s - np.array([1.0, 1.0, 2.0]))  # [5. 8. 10.]
```

## Common mistakes

- **Forgetting the leading zero.** Without it, the first window has no start total and the output is one element short.
  - The prefix array must have length `n + 1`.
- **Off-by-one in the slices.** End totals start at index `k`; start totals stop `k` before the end.
  - Check that the output length is `n - k + 1`.
- **Integer inputs.** A plain cumsum on ints stays int, so ask for floats before dividing.
- **Using a Python loop or banned helpers.** A loop over windows is too slow at `n = 10^6`.
  - `np.convolve` and `sliding_window_view` are rejected by the tests.
- **Changing the input.** Don't write into `x` (for example with `x += ...`); build new arrays instead.

## Hints

### Hint 1
- Build an array of running totals that starts with a `0`.
- Each window sum is one running total minus an earlier one, exactly `k` positions apart.
- Take all those differences at once.
- Divide by `k`.

### Hint 2
- Use `np.cumsum` on `x` to get running totals (length `n`).
- Use `np.concatenate` to put a `0` in front (length `n + 1`).
- Take two slices of that array, each of length `n - k + 1`, and subtract them.
- Divide the result by `k`.

### Hint 3
- Call the prefix array `c`, with `c[0] = 0` and `c[j]` equal to the sum of the first `j` values of `x`.
- The sum of `x[i : i + k]` is `c[i + k] - c[i]`.
- For all `i` from `0` to `n - k`, the first terms are the slice of `c` starting at index `k`.
- The second terms are the slice of `c` that stops `k` places before the end.
- Subtract the second from the first, then divide by `k`.
