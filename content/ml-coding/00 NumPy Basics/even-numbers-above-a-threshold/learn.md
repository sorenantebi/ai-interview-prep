# Learn: Even Numbers Above a Threshold

## The idea

- The task: keep only the numbers that pass **two** tests at once, even and strictly greater than `k`.
  - **Strictly greater** means a value equal to `k` does not count.
  - The kept numbers stay in their original order.
- In NumPy you don't loop and check each number; you test the whole array in one go.
- Where it shows up: dropping outliers, keeping samples above a confidence score, selecting a subset for an evaluation report.
- **Boolean mask**: an array of `True`/`False` values, one per element, with the same shape as the original.
- **Boolean indexing**: writing `a[mask]` to keep only the positions where the mask is `True`.
- **Combining masks**: "A and B" keeps positions where both are `True`; "A or B" keeps positions where at least one is.
- **Remainder (modulo)**: `n % 2` is the remainder after dividing by 2. It is `0` for even numbers and `1` for odd ones.

## Work it by hand

Take `x = [1, 2, 3, 4, 5, 6, 7, 8]` and `k = 3`. Every mask has length 8.

1. **Even mask.** Compute `x % 2`, then check which are `0`.

| x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| x % 2 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| even? | F | T | F | T | F | T | F | T |

2. **Threshold mask.** Is each element greater than 3?

| x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| above 3? | F | F | F | T | T | T | T | T |

3. **Combine with "and".** Keep a position only if both rows are `T`.

| x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| both? | F | F | F | T | F | T | F | T |

4. **Select.** The `T` positions are 3, 5 and 7 (counting from 0), which hold `4, 6, 8`.
5. Result: `[4, 6, 8]`. The masks have length 8, the result has length 3.

## Tools you'll need

### `x % 2 == 0`

- `%` gives the remainder for every element at once.
- Comparing with `== 0` turns the remainders into a boolean array of the same shape.
- It also works for negative numbers in NumPy.

```python
import numpy as np

a = np.array([10, 7, -3, -8])
print(a % 2)         # [0 1 1 0]
print(a % 2 == 0)    # [ True False False  True]
```

### Comparisons (`>`, `>=`, `<`)

- Comparing an array with one number tests every element and returns a boolean array.
- `>` is strict; `>=` also accepts equality.

```python
import numpy as np

a = np.array([5, 9, 12, 9])
print(a > 9)     # [False False  True False]
print(a >= 9)    # [False  True  True  True]
```

### `&` and `|` (combining masks)

- `&` means "and" and `|` means "or", element by element.
- Python's `and` / `or` fail on arrays, so don't use them.
- Wrap each comparison in parentheses, because `&` binds more tightly than `>` or `==`.

```python
import numpy as np

a = np.array([2, 15, 8, 21])
print((a > 5) & (a < 20))   # [False  True  True False]
print((a < 5) | (a > 20))   # [ True False False  True]
```

### Boolean indexing `a[mask]`

- A boolean array of the same length inside square brackets keeps the elements where it is `True`, in order.
- The result is a new 1-D array, so the input is not changed.
- If nothing is `True`, you get an empty array.

```python
import numpy as np

a = np.array([30, 40, 50, 60])
mask = np.array([True, False, False, True])
print(a[mask])          # [30 60]
print(a[mask].shape)    # (2,)
```

```python
import numpy as np

a = np.array([1, 2, 3])
print(a[a > 10])    # []
```

## Common mistakes

- **Missing parentheses.** `x % 2 == 0 & x > k` is parsed in the wrong order and errors out or gives wrong results.
  - Put each comparison in its own parentheses.
- **Using `and` instead of `&`.** Python's `and` asks "is the whole array true?" and raises a `ValueError` for arrays with more than one element.
  - Use `&` for masks.
- **`>=` instead of `>`.** The problem says strictly greater, so an element equal to `k` must be dropped.
- **Testing for odd instead of even.** Even means remainder `0`; remainder `1` means odd.
- **Looping or building a list.** It works but is slow for 10^5 elements and misses the point of the drill.
  - Stay with masks.

## Hints

### Hint 1
- Make one yes/no test for "is even", covering all elements at once.
- Make another yes/no test for "is above `k`".
- Combine them so a position survives only if both tests say yes.
- Use that combined result to pick elements from `x`.

### Hint 2
- Use `%` with `== 0` for the even mask; it is a boolean array with the same shape as `x`.
- Use `>` against `k` for the threshold mask; same shape again.
- Join the two with `&`, each in parentheses, giving one more boolean array of that shape.
- Index `x` with it; the result is 1-D and no longer than `x`.

### Hint 3
- The combined mask reads: "the even test in parentheses, `&`, the greater-than-`k` test in parentheses".
- Store it in a variable.
- Put that variable inside square brackets after `x` and return the result.
- An empty result needs no special handling.
