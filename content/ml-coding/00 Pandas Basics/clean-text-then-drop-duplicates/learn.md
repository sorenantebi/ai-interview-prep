# Learn: Clean Text, Then Drop Duplicates

## The idea

- The task: make messy text consistent, then remove rows that are exact repeats.
- `" Berlin"`, `"berlin "` and `"BERLIN"` mean one city, but a computer sees three different strings.
- This shows up in almost every feature pipeline: cleaning labels, merging data from several sources, and keeping the same example from appearing twice in a training set.
  - Duplicates can also leak from the training set into the test set and inflate your scores.
- **Normalising** (standardising) text: making spelling consistent, here by trimming whitespace and lowercasing.
- **Duplicate row**: a row whose values in every column match an earlier row.
- **DataFrame**: a table with named columns and a row label for each row.
- **Series**: one column of a DataFrame.
- **Index label**: the name of a row.
  - It stays attached to the row even when other rows are removed.
- Order matters: if you dedupe first, the messy spellings still look different and nothing is removed.

## Work it by hand

Example 1 input:

| index | city        | visitors |
|-------|-------------|----------|
| 0     | `" Berlin"` | 10       |
| 1     | `"berlin "` | 10       |
| 2     | `"Bonn"`    | 7        |

1. **Strip whitespace** from `city`: `"Berlin"`, `"berlin"`, `"Bonn"`.
2. **Lowercase** `city`: `"berlin"`, `"berlin"`, `"bonn"`.
3. The table is now:

| index | city       | visitors |
|-------|------------|----------|
| 0     | `"berlin"` | 10       |
| 1     | `"berlin"` | 10       |
| 2     | `"bonn"`   | 7        |

4. **Drop duplicates**: row 1 equals row 0 in all columns (`"berlin"`, 10), so it goes.
   - Row 2 differs, so it stays.
5. Result:

| index | city       | visitors |
|-------|------------|----------|
| 0     | `"berlin"` | 10       |
| 2     | `"bonn"`   | 7        |

- The index labels are 0 and 2; nothing renumbers them.
- This matches the expected output `{"city": ["berlin", "bonn"], "visitors": [10, 7]}`.
- Compare Example 2: both cities become `"ulm"`, but visitors 5 and 6 differ, so both rows stay.

## Tools you'll need

### `Series.str.strip()`

- The `.str` accessor applies a string method to every element of a text column, with no loop.
- `strip()` removes whitespace from both ends, not from the middle.

```python
import pandas as pd

s = pd.Series(["  cat", "dog  ", " a b "])
print(s.str.strip().tolist())  # ['cat', 'dog', 'a b']
```

### `Series.str.lower()`

- Converts every string to lowercase.
- It returns a new Series, so you can chain it after `strip()`.

```python
import pandas as pd

s = pd.Series(["Rose", "TULIP"])
print(s.str.lower().tolist())  # ['rose', 'tulip']
```

### `DataFrame.assign(col=values)`

- Returns a **new** DataFrame with a column added or replaced; the original is untouched.
- The column name is the keyword argument.
- Alternative: `out = df.copy()`, then `out["col"] = ...`.

```python
import pandas as pd

df = pd.DataFrame({"n": [1, 2]})
new = df.assign(n=df["n"] * 10)
print(df["n"].tolist())   # [1, 2]
print(new["n"].tolist())  # [10, 20]
```

### `DataFrame.drop_duplicates(keep="first")`

- Removes rows equal to an earlier row in **all** columns (unless you pass `subset=`).
- `keep="first"` (the default) keeps the first occurrence.
- Surviving rows keep their original index labels.

```python
import pandas as pd

df = pd.DataFrame({"a": ["x", "x", "y", "x"], "b": [1, 1, 1, 2]})
out = df.drop_duplicates(keep="first")
print(out.index.tolist())  # [0, 2, 3]
print(out["a"].tolist())   # ['x', 'y', 'x']
```

- Row 1 is dropped because it matches row 0.
- Row 3 stays because `b` differs.

## Common mistakes

- **Deduplicating before cleaning.** The messy strings are still different, so nothing is removed.
  - Clean first, then dedupe.
- **Modifying the input.** Writing `df["city"] = ...` directly changes the caller's DataFrame.
  - Use `assign`, or work on a `copy()`.
- **Forgetting `.str`.** `df["city"].strip()` fails.
  - String methods on a Series live under `.str`.
- **Resetting the index.** The problem wants the original labels (0 and 2 in Example 1).
  - Don't call `reset_index`.
- **Expecting `strip()` to clean the middle.** It only trims the ends, which is all this problem needs.

## Hints

### Hint 1

- Fix the text in the `"city"` column: trim the ends, then lowercase.
- Put the cleaned column into a new DataFrame so the original stays unchanged.
- Remove duplicate rows, keeping the first of each.

### Hint 2

- Clean the column with chained `.str.strip()` and `.str.lower()` on the `"city"` Series; the result is a Series of the same length.
- Use `assign` to get a new DataFrame with that column replaced; same rows, same columns.
- Call `drop_duplicates` on that DataFrame; same columns, fewer rows.

### Hint 3

- `assign` takes the column name as a keyword, so pass the cleaned Series under the name `city`.
- `drop_duplicates` compares all columns by default and keeps the first match.
  - You don't need `subset`, a loop, or `reset_index`.
- Return the result of `drop_duplicates`.
