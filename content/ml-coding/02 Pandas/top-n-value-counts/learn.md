# Learn: Top N Value Counts

## The idea

- The task: count how often each label appears, then keep only the `n` most common ones.
- The answer is a Series: the labels are the index, the counts are the values.
- **Series**: a pandas column, a list of values where each value has a label.
- **Index**: the labels attached to a Series' values.
- Where it shows up:
  - Checking class balance before training a model.
  - Finding the top categories for a feature pipeline.
  - Listing the most frequent errors in an evaluation report.
- **Missing values** (`None` / `NaN`) mean "no label here". They are not counted.
- **Tie-break**: labels with equal counts need a fixed order, so the output is always the same.
  - Here that order is alphabetical.

## Work it by hand

Take `s = ["cat", "dog", "cat", "bird", "dog", "cat"]` and `n = 2`.

1. Count each label:

   | label | count |
   |-------|-------|
   | cat   | 3     |
   | dog   | 2     |
   | bird  | 1     |

2. Sort by count from highest to lowest, and by label A to Z when counts are equal.
   - There are no ties here, so the order stays the same.
3. Keep the first `n = 2` rows: `cat 3` and `dog 2`.
4. Result: index `["cat", "dog"]`, values `[3, 2]`, which is `{"cat": 3, "dog": 2}`.

- In Example 2, `a` and `b` both have count 2, so `a` goes first.
  - The `null` is skipped, giving the order `a`, `b`, `c`.

## Tools you'll need

### `Series.value_counts()`

- Counts each distinct value and returns a Series: label as index, count as value.
- It skips missing values by default (`dropna=True`).
- It sorts by count, but the order among tied counts is not alphabetical. Don't rely on it.

```python
import pandas as pd

t = pd.Series(["red", "blue", "red", None, "red", "blue"])
vc = t.value_counts()
print(vc.to_dict())        # {'red': 3, 'blue': 2}
print(vc.index.tolist())   # ['red', 'blue']
print(vc.values.tolist())  # [3, 2]
```

### `DataFrame.sort_values(by, ascending)`

- Sorts rows by one or more columns.
- Pass a list to `by` to sort on several keys.
- Pass a list to `ascending` with one True/False per key, in the same order.
- The second key only matters when the first key ties.

```python
import pandas as pd

df = pd.DataFrame({"name": ["b", "a", "c"], "score": [5, 5, 9]})
out = df.sort_values(["score", "name"], ascending=[False, True])
print(out["name"].tolist())  # ['c', 'a', 'b']
```

### `.head(n)`

- Returns the first `n` rows (or items).
- If there are fewer than `n`, you just get all of them, with no error.

```python
import pandas as pd

q = pd.Series([4, 3, 2, 1])
print(q.head(2).tolist())  # [4, 3]
print(len(q.head(10)))     # 4
```

### Building a Series with a custom index

- `pd.Series(values, index=labels)` makes a Series whose index is the labels you give it.
- Plain lists or arrays avoid carrying over an old index.

```python
import pandas as pd

r = pd.Series([7, 8], index=["u", "v"])
print(r.to_dict())  # {'u': 7, 'v': 8}
print(r["v"])       # 8
```

### Building a DataFrame from columns

- `pd.DataFrame({"col": values, ...})` turns equal-length lists into a table.
- This is handy when you need to sort by two keys.

```python
import pandas as pd

d = pd.DataFrame({"fruit": ["fig", "kiwi"], "qty": [2, 6]})
print(d.shape)             # (2, 2)
print(d.columns.tolist())  # ['fruit', 'qty']
```

## Common mistakes

- **Trusting `value_counts` for tie order.**
  - Its order among equal counts is not alphabetical.
  - Add an explicit second sort key on the label.
- **Counting missing values.**
  - Don't pass `dropna=False`.
  - The default already ignores `None`/`NaN`.
- **Sorting both keys the same way.**
  - Counts go descending, labels go ascending.
  - Use `ascending=[False, True]`, matching the order of the `by` list.
- **Leaking the old index.**
  - After sorting a DataFrame, its row numbers are shuffled.
  - Build the final Series from the label column as the index, not from those row numbers.
- **Over-worrying about `n`.**
  - If `n` exceeds the number of distinct labels, `head(n)` just returns everything.
  - An empty input should give an empty result, so you rarely need a special case.

## Hints

### Hint 1
- Count the labels first.
- Order the counts so bigger ones come first and ties go alphabetically.
- Cut the result down to `n` entries.
- Return it as a Series with the labels as the index.

### Hint 2
- Counting: `value_counts()` gives a Series (label index, count values), with missing values already dropped.
- Sorting on two keys is easiest on a DataFrame with a label column and a count column.
  - Use `sort_values` with a list for `by` and a list for `ascending`.
- Cutting to `n`: `head(n)` keeps at most `n` rows.
- Return: a new Series built from the count column, with the label column as its index.

### Hint 3
- The tricky step is the sort: sort by `count` descending first, then break ties by `label` ascending.
  - So `by` is `["count", "label"]` and `ascending` is `[False, True]`.
- After `head(n)`, take the `label` column as the new index and the `count` column as the values.
- Use their raw values (not the old row numbers) so the index really is the labels.
