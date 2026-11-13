# Learn: Rank Within Group

## The idea

- **The task:** for each employee, find where their salary stands among people in their own department, with `1` as the highest.
- **Ties share a rank.** Salaries 9, 9, 7 give ranks 1, 1, 2.
  - The next rank follows immediately, with no gap.
- **Dense rank:** the name for this tie rule.
- **groupby:** splits a table into pieces by the value of a column (here `dept`), does something to each piece separately, and puts the results back in the original row positions.
- **Where it shows up:**
  - Feature pipelines: "top-3 products per category".
  - Evaluation reports: "best model run per dataset".
  - Ranking features for recommenders.
- Ranking must happen inside each department, never across the whole table.
- The result must line up with the original rows, so order and index stay unchanged.

## Work it by hand

Example 1:

```text
dept:   eng, eng, ops, eng
name:   a,   b,   c,   d
salary: 100, 120, 90,  100
```

1. Split the rows by department.

   | dept | rows (name: salary)    |
   |------|------------------------|
   | eng  | a: 100, b: 120, d: 100 |
   | ops  | c: 90                  |

2. In `eng`, list the distinct salaries from high to low: 120, 100.
   - b (120) gets rank 1.
   - a (100) and d (100) tie, so both get rank 2.
3. In `ops`, there is only 90, so c gets rank 1.
4. Put the ranks back in the original row order (a, b, c, d): `2, 1, 1, 2`.
5. Attach them as a new last column. The result:

```text
dept:   eng, eng, ops, eng
name:   a,   b,   c,   d
salary: 100, 120, 90,  100
rank:   2,   1,   1,   2
```

- This matches the expected output.

## Tools you'll need

### df.copy()

- Returns a new DataFrame with its own data.
- Changing the copy leaves the original alone, which the problem requires.

```python
import pandas as pd

a = pd.DataFrame({"x": [1, 2]})
b = a.copy()
b["x"] = 99
print(a["x"].tolist())  # [1, 2]
```

### df.groupby(col)

- Splits the table into groups by the values in `col`.
- On its own it shows nothing. Pick a column from it and apply an operation, which then runs once per group.

```python
import pandas as pd

d = pd.DataFrame({"team": ["r", "b", "r"], "pts": [5, 8, 7]})
print(d.groupby("team")["pts"].max())
# team
# b    8
# r    7
# Name: pts, dtype: int64
```

### Series.rank(method=, ascending=)

- Gives each value its rank. Ranks come back as floats.
- `ascending=True` (default) gives rank 1 to the smallest value. Use `ascending=False` for the largest.
- `method` decides how ties are handled:
  - `"average"` (default): tied values get the mean of their positions.
  - `"min"`: ties get the lowest position, leaving gaps afterwards.
  - `"first"`: ties are broken by order of appearance.
  - `"dense"`: ties share a rank, with no gaps.

```python
import pandas as pd

s = pd.Series([30, 10, 30, 20])
print(s.rank(ascending=False).tolist())                  # [1.5, 4.0, 1.5, 3.0]
print(s.rank(method="min", ascending=False).tolist())    # [1.0, 4.0, 1.0, 3.0]
print(s.rank(method="dense", ascending=False).tolist())  # [1.0, 3.0, 1.0, 2.0]
```

### rank() after groupby

- Calling `.rank()` on a grouped column ranks inside each group.
- The result keeps the original index, so it lines up row by row.

```python
import pandas as pd

d = pd.DataFrame({"g": ["u", "v", "u", "v"], "s": [1, 5, 3, 5]})
print(d.groupby("g")["s"].rank(method="min").tolist())  # [1.0, 1.0, 2.0, 1.0]
```

### Series.astype(int)

- Converts values to another type.
- `rank` returns floats like `1.0`, but the problem wants integers.

```python
import pandas as pd

r = pd.Series([1.0, 2.0])
print(r.astype(int).tolist())  # [1, 2]
print(r.astype(int).dtype)     # int64
```

### Adding a column: df["new"] = values

- Assigning to a new column name appends it at the end.
- Pandas matches by index, so a Series with the same index lands in the right rows.

```python
import pandas as pd

d = pd.DataFrame({"a": [1, 2]})
d["b"] = pd.Series([7, 8])
print(d.columns.tolist())  # ['a', 'b']
```

## Common mistakes

- **Ranking the whole column.** `df["salary"].rank()` ignores departments.
  - Always go through `groupby("dept")`.
- **Wrong direction.** The default is ascending, so the lowest salary gets rank 1.
  - Pass `ascending=False`.
- **Wrong tie method.** The default `"average"` gives values like `1.5`, and `"min"` leaves gaps (1, 1, 3).
  - Pick the method that gives 1, 1, 2.
- **Float ranks.** `rank` returns floats.
  - Convert to `int` so the column holds integers.
- **Modifying the input.** Assigning a column directly on `df` changes the caller's data.
  - Copy first.

## Hints

### Hint 1

- Make a copy of the table.
- For each department separately, compute the dense rank of salary, highest first.
- Convert the ranks to integers.
- Store them in a new column called `rank`.
- Return the copy.

### Hint 2

- Call `copy()` first: you get a new DataFrame.
- Group by `dept`, select the `salary` column, and call `rank` with a tie method: you get a float Series with one value per original row and the same index.
- Finish with `astype(int)`: same shape, integer dtype.
- Assign the result to the `rank` column of the copy.

### Hint 3

- The tricky part is choosing the arguments for `rank`.
- You want the highest salary to be 1, so set `ascending` to `False`.
- You want ties to share a rank and the next salary to follow with no gap, so set `method` to `"dense"`.
- Because `rank` is called on the grouped column, counting restarts at 1 in every department.
