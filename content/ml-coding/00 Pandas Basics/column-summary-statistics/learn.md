# Learn: Column Summary Statistics

## The idea

- **The task**: shrink one column of a table down to four numbers: mean, min, max and sum.
- You return those four numbers together as one labelled `Series`, in a fixed order.
- **Where it shows up**: checking a feature before training, spotting odd ranges in an evaluation report, sanity-checking a new dataset.
- **DataFrame**: a table with named columns.
- **Series**: one column of values, plus an *index* (a label for each value) and an optional *name*.
- **Aggregation**: turning many values into one, such as a sum.
- **NaN**: "not a number", pandas' marker for a missing value.
  - Pandas skips it by default, so the mean of `[1, NaN, 3]` is 2, not NaN.

## Work it by hand

Example 1: column `"a"` holds `[1, 2, 3, 4]`. Column `"b"` is ignored.

| Step | What we do | Result |
|---|---|---|
| 1 | Pick column `"a"` | `[1, 2, 3, 4]` (4 values) |
| 2 | mean = (1+2+3+4) / 4 = 10 / 4 | 2.5 |
| 3 | min = smallest value | 1 |
| 4 | max = largest value | 4 |
| 5 | sum = 1+2+3+4 | 10 |
| 6 | Line them up as mean, min, max, sum, using those words as labels | 4 labelled values |

- The final Series looks like this:

```text
mean    2.5
min     1.0
max     4.0
sum    10.0
Name: a, dtype: float64
```

- This matches the expected output (2.5, 1, 4, 10).
- The name `a` is the column name.

## Tools you'll need

### df[col]

- Square brackets with a column name give you that column as a Series.
- The Series remembers the column name.

```python
import pandas as pd

df = pd.DataFrame({"height": [1.5, 1.8], "age": [30, 40]})
s = df["height"]
print(s.name)  # height
print(s.tolist())  # [1.5, 1.8]
```

### Series.agg([...])

- `agg` (short for aggregate) takes a list of function names as strings, such as `"median"` or `"std"`.
- It applies each one to the Series and returns a new Series.
  - Its index holds the names, in the order you gave them.
  - The result keeps the original column's name.

```python
import pandas as pd

s = pd.Series([4, 8, 6], name="score")
out = s.agg(["max", "median"])
print(out.tolist())  # [8.0, 6.0]
print(list(out.index))  # ['max', 'median']
print(out.name)  # score
```

### Skipping NaN

- `mean`, `sum`, `min` and `max` ignore NaN by default (`skipna=True`).
- You don't need to clean the data first.

```python
import numpy as np
import pandas as pd

s = pd.Series([10.0, np.nan, 20.0])
print(s.mean())  # 15.0
print(s.sum())  # 30.0
```

### Series.describe()

- `describe()` is a related tool that returns a fixed summary: count, mean, std, min, quartiles and max.
- You can't choose which statistics appear or their order, and it has no `sum`.

```python
import pandas as pd

s = pd.Series([2, 4, 6])
print(list(s.describe().index))
# ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
```

## Common mistakes

- **Using `describe()` as the answer.**
  - It gives the wrong labels, extra rows and no `sum`.
  - Use `agg` with your own list.
- **Wrong order in the list.**
  - The index follows the order you pass.
  - Write it as mean, min, max, sum.
- **Misspelling a name.**
  - Aggregation names are strings and must match exactly, such as `"mean"`, not `"average"`.
- **Selecting with double brackets.**
  - `df[[col]]` returns a DataFrame, not a Series.
  - The result then has a different shape and no `name == col`. Use `df[col]`.
- **Dropping NaN by hand or looping.**
  - Pandas already skips NaN, and loops are slower and unnecessary.

## Hints

### Hint 1

- Take out the one column you need from the table.
- Ask pandas for four statistics on it at once.
- List them in the required order.

### Hint 2

- Step 1: column selection with square brackets gives a Series.
- Step 2: the Series method `agg` takes a list of statistic names and returns a Series indexed by those names.
- The result is a Series of length 4.

### Hint 3

- Give `agg` a list of four strings: `"mean"`, `"min"`, `"max"`, `"sum"`, in that order.
- The index of the result follows your list.
- The column name carries over on its own.
- Return what `agg` gives you. Nothing else is needed.
