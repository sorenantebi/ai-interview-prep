# Learn: Scores Above a Threshold

## The idea

- The task: keep only the entries whose number is **strictly greater** than a cutoff.
  - The labels must survive as the index.
  - The original order must not change.
- This "filter rows by a condition" step shows up everywhere in data work.
  - Dropping low-confidence predictions.
  - Removing outliers in a feature pipeline.
  - Listing the models that beat a baseline in an evaluation report.
- **Series**: pandas' one-dimensional labelled column, i.e. a list of values plus a label for each value.
- **Index**: the labels of a Series. Building a Series from a dict makes the keys the index.
- **Boolean mask**: a Series of `True`/`False` values, one per entry.
  - Using it to select entries keeps the `True` ones and drops the `False` ones.
- **Strictly greater**: a value equal to the threshold is dropped.

## Work it by hand

Example 1: `scores = {"a": 1.0, "b": 3.5, "c": 2.0, "d": 5.0}`, `threshold = 2.0`.

1. Build the Series. Its shape is `(4,)`.

| index | value |
|---|---|
| a | 1.0 |
| b | 3.5 |
| c | 2.0 |
| d | 5.0 |

2. Compare each value with `2.0`. The mask has the same index and shape `(4,)`.

| index | value > 2.0 |
|---|---|
| a | False (1.0 is below 2.0) |
| b | True |
| c | False (2.0 equals 2.0, not strictly above) |
| d | True |

3. Keep only the `True` rows, in their original order: `b` and `d`. Shape is `(2,)`.
4. Result: `b` is `3.5` and `d` is `5.0`, which is `{"b":3.50000,"d":5.00000}`.

## Tools you'll need

### pd.Series(dict)

- Builds a Series from a dict.
- Keys become the index, values become the data, and the dict's order is kept.

```python
import pandas as pd

s = pd.Series({"x": 7.0, "y": 1.5, "z": 4.0})
print(s.index.tolist())  # ['x', 'y', 'z']
print(s.shape)  # (3,)
print(s["y"])  # 1.5
```

### Comparison operators on a Series (`>`, `>=`)

- Comparing a Series with one number checks every entry and returns a boolean Series with the same index.
  - No loop is needed.
- `>` is strictly greater; `>=` also accepts equality.

```python
import pandas as pd

s = pd.Series({"p": 10.0, "q": 20.0, "r": 30.0})
print((s > 20.0).tolist())   # [False, False, True]
print((s >= 20.0).tolist())  # [False, True, True]
```

### .loc[...]

- `.loc` selects by **label**.
  - Give it a label, a list of labels, or a boolean mask with the same index.
- With a mask, it returns only the entries where the mask is `True`, and keeps their labels.

```python
import pandas as pd

s = pd.Series({"u": 1.0, "v": 8.0, "w": 3.0})
print(s.loc["v"])  # 8.0
print(s.loc[["u", "w"]].tolist())  # [1.0, 3.0]
mask = pd.Series({"u": True, "v": False, "w": True})
print(s.loc[mask].index.tolist())  # ['u', 'w']
```

### Empty results

- If the mask is all `False`, selecting gives an empty Series.
  - It is not an error, so no special case is needed.

```python
import pandas as pd

s = pd.Series({"k": 1.0, "m": 2.0})
empty = s.loc[s > 100.0]
print(len(empty))  # 0
print(empty.empty)  # True
```

## Common mistakes

- **Using `>=` instead of `>`.**
  - A value equal to the threshold must be dropped. Example 1's `"c"` checks this.
- **Using Python's `and`/`or` or a loop on a Series.**
  - Compare the whole Series at once.
  - If you ever combine masks, use `&` and `|` with parentheses.
- **Losing the labels.**
  - Don't convert to a list or NumPy array before filtering.
  - The result must keep the keys as its index.
- **Special-casing the empty result.**
  - Filtering already returns an empty Series when nothing matches.
  - Don't return `None` or `{}`.
- **Sorting the result.**
  - Don't call `sort_values`; boolean selection already preserves the original order.

## Hints

### Hint 1
- Turn the dict into a labelled column.
- Work out, for each entry, whether it is above the threshold.
- Keep only the entries where the answer is yes.

### Hint 2
- Build the Series with `pd.Series(...)`; it has length n.
- Compare it with the number to get a boolean Series of the same length and index.
- Select the matching entries with `.loc` and that boolean Series.

### Hint 3
- The comparison gives one True/False per label, and `True` means "strictly above".
- Pass that True/False Series into `.loc[...]` on the same Series you compared.
- Pandas matches by label and returns only the `True` rows, in their original order and with their labels.
- Return that result directly.
