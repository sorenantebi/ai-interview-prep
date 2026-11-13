# Learn: Select Rows and Columns with .loc

## The idea

- The task: from a big table, build a smaller table with only the rows and columns you want, in the order you want.
- **DataFrame**: a pandas table with labelled rows and labelled columns.
- **Index**: the row labels of a DataFrame.
  - By default they are 0, 1, 2, ...
  - You can turn any column, such as a name, into the index.
- **Label-based selection**: asking for rows and columns by their labels (`"Cara"`, `"score"`), not by position ("third row").
- **`.loc`**: the pandas tool for label-based selection.
  - Give it a **list** of labels per axis and you always get a DataFrame back.
  - A single label shrinks the result to a Series or a single value.
- Where it shows up:
  - picking the feature columns for a model,
  - pulling certain customers for an evaluation report,
  - reordering columns before an export.

## Work it by hand

Example 1: `names = ["Cara", "Anna"]`, `columns = ["score", "age"]`.

1. **Start**: 4 rows, 4 columns, default index 0 to 3.

| | name | age | city | score |
|---|---|---|---|---|
| 0 | Anna | 34 | Bonn | 88.5 |
| 1 | Ben | 28 | Koeln | 92.0 |
| 2 | Cara | 45 | Essen | 79.5 |
| 3 | Dev | 39 | Ulm | 85.0 |

2. **Make `name` the index.**
   - `name` leaves the data columns and becomes the row labels.
   - Shape is now (4, 3): columns `age`, `city`, `score`.

| name | age | city | score |
|---|---|---|---|
| Anna | 34 | Bonn | 88.5 |
| Ben | 28 | Koeln | 92.0 |
| Cara | 45 | Essen | 79.5 |
| Dev | 39 | Ulm | 85.0 |

3. **Pick rows** in the order `["Cara", "Anna"]`.
   - Cara comes first, then Anna.
   - Ben and Dev are gone.
4. **Pick columns** in the order `["score", "age"]`.
   - `city` is dropped and `score` now comes before `age`.
   - Shape is (2, 2).

| name | score | age |
|---|---|---|
| Cara | 79.5 | 45 |
| Anna | 88.5 | 34 |

5. **Result**: `{"name":["Cara","Anna"],"score":[79.5,88.5],"age":[45,34]}`, which matches the expected output.

## Tools you'll need

### df.set_index("col")

- Turns the column `col` into the row index.
- Returns a **new** DataFrame; the original is unchanged.

```python
import pandas as pd

d = pd.DataFrame({"fruit": ["kiwi", "plum"], "price": [3, 5]})
e = d.set_index("fruit")
print(list(e.index))    # ['kiwi', 'plum']
print(list(e.columns))  # ['price']
print(list(d.columns))  # ['fruit', 'price']
```

### df.loc[row_labels, column_labels]

- Selects by label: rows first, columns second.
- With lists, the result follows the order of your lists and is always a DataFrame.

```python
import pandas as pd

t = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]},
                 index=["x", "y", "z"])
r = t.loc[["z", "x"], ["c", "a"]]
print(r.shape)  # (2, 2)
print(r.values.tolist())  # [[9, 7], [3, 1]]
```

### List vs. single label

- A single label drops a dimension.
- A one-element list keeps it.

```python
import pandas as pd

t = pd.DataFrame({"a": [1, 2], "b": [3, 4]}, index=["x", "y"])
print(type(t.loc["x", "a"]).__name__)      # int64
print(type(t.loc["x", ["a"]]).__name__)    # Series
print(type(t.loc[["x"], ["a"]]).__name__)  # DataFrame
```

### Repeated labels

- If a label appears twice in the row list, `.loc` returns that row twice.
- This works as long as the index itself has unique labels.

```python
import pandas as pd

t = pd.DataFrame({"a": [10, 20]}, index=["x", "y"])
print(t.loc[["y", "y", "x"], ["a"]]["a"].tolist())  # [20, 20, 10]
```

## Common mistakes

- **Forgetting `set_index`.**
  - Without it the index is 0, 1, 2, ..., so looking up `"Cara"` raises a `KeyError`.
  - Set the index first.
- **Swapping the arguments.**
  - Rows come first, columns second.
  - Putting the column list first fails or selects the wrong thing.
- **Passing a single string.**
  - `"Ben"` or `"city"` instead of a list can give a Series or a scalar.
  - Keep both arguments as lists.
- **Expecting `name` to stay a column.**
  - After `set_index`, `name` is the index, so don't list it in `columns`.
- **Looping over rows.**
  - It is slower and unnecessary.
  - One `.loc` call handles the order and the repeats.

## Hints

### Hint 1
- Move the `name` column into the index, so you can look rows up by name.
- Select the wanted rows and columns in one step, using the two lists you were given.
- Return the result.

### Hint 2
- Use `set_index` on `"name"`; for the example the frame has shape (4, 3), indexed by name.
- Use `.loc` with the row list first and the column list second.
- The result has shape `(len(names), len(columns))`.

### Hint 3
- `.loc` takes two arguments separated by a comma inside square brackets.
- The first is your `names` list (row labels), the second is your `columns` list (column labels).
- Apply it to the frame you got back from `set_index`, and return that directly.
- The order of both lists and any repeated names are kept automatically.
