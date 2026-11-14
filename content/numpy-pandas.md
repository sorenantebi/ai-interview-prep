# NumPy & pandas basics

One card per topic: the calls you reach for in ML coding rounds, each with a runnable example (the comment under a print is what it prints). Edit this file under Files.

## NumPy: create arrays

- **From a list:** `np.array([1, 2, 3])`; nested lists make 2-D arrays.
- **Filled:** `np.zeros(shape)`, `np.ones(shape)`, `np.full(shape, value)`, `np.eye(n)` (identity).
- **Ranges:** `np.arange(start, stop, step)` (stop excluded), `np.linspace(start, stop, num)` (stop included).
- **Same shape as another array:** `np.zeros_like(a)`, `np.ones_like(a)`.
- **dtype:** pass `dtype=float` / `int` / `bool`, or convert with `a.astype(float)`.

```python
import numpy as np

print(np.array([[1, 2], [3, 4]]))  # [[1 2]
                                   #  [3 4]]
print(np.zeros((2, 3)))            # [[0. 0. 0.]
                                   #  [0. 0. 0.]]
print(np.arange(0, 10, 3))         # [0 3 6 9]
print(np.linspace(0, 1, 5))        # [0.   0.25 0.5  0.75 1.  ]
print(np.full(3, 7))               # [7 7 7]
```

## NumPy: shape, dtype & attributes

- **`a.shape`**: tuple of sizes per axis, e.g. `(rows, cols)`.
- **`a.ndim`**: number of axes. **`a.size`**: total number of elements.
- **`a.dtype`**: element type (`int64`, `float64`, `bool`, ...). Integer division traps: `/` always gives floats, `//` floors.
- **`len(a)`** is the size of the first axis only.

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape, a.ndim, a.size)  # (2, 3) 2 6
print(a.dtype)                  # int64
print(a / 2)                    # [[0.5 1.  1.5]
                                #  [2.  2.5 3. ]]
print(a // 2)                   # [[0 1 1]
                                #  [2 2 3]]
```

## NumPy: indexing & slicing

- **1-D:** `a[i]`, `a[-1]` (last), `a[start:stop:step]`, `a[::-1]` (reversed).
- **2-D:** `a[row, col]`, a whole row `a[r]` or `a[r, :]`, a whole column `a[:, c]`.
- **Slices are views:** changing `a[1:3]` changes `a`. Use `.copy()` when you need a separate array.
- **Fancy indexing:** an index array picks those positions: `a[[0, 2]]`; it returns a copy.

```python
import numpy as np

a = np.arange(12).reshape(3, 4)
print(a[1, 2])      # 6
print(a[:, 0])      # [0 4 8]
print(a[-1, ::-1])  # [11 10  9  8]
print(a[:2, 1:3])   # [[1 2]
                    #  [5 6]]
print(a[[0, 2]])    # [[ 0  1  2  3]
                    #  [ 8  9 10 11]]
```

## NumPy: boolean masks & np.where

- **A comparison** like `a > 3` gives a boolean array of the same shape.
- **Filter:** `a[a > 3]` keeps the matching elements (result is 1-D).
- **Combine conditions** with `&` (and), `|` (or), `~` (not), and wrap each in brackets: `(a > 1) & (a < 5)`.
- **`np.where(cond, x, y)`**: element-wise "if cond then x else y"; `x` and `y` can be scalars.
- **Count / test:** `mask.sum()` counts `True`s; `mask.any()`, `mask.all()`.

```python
import numpy as np

a = np.array([4, -1, 7, 0, 2])
print(a > 1)                     # [ True False  True False  True]
print(a[(a > 0) & (a % 2 == 0)]) # [4 2]
print(np.where(a < 0, 0, a))     # [4 0 7 0 2]
print((a > 1).sum())             # 3
```

## NumPy: arithmetic & broadcasting

- **Element-wise:** `+ - * / ** %` work entry by entry on same-shaped arrays, and with a scalar on every entry.
- **Broadcasting:** shapes are compared from the right; each axis must be equal or 1. A `(3, 1)` column and a `(1, 4)` row give `(3, 4)`.
- **Add an axis:** `a[:, None]` (or `a.reshape(-1, 1)`) turns shape `(n,)` into a column `(n, 1)`.
- **Matrix product:** `A @ B` (not `*`, which is element-wise).
- **Maths:** `np.sqrt`, `np.exp`, `np.log`, `np.abs`, `np.round(a, 2)`, `np.pi`.

```python
import numpy as np

a = np.array([1, 2, 3])
print(a * 10 + 1)        # [11 21 31]
print(a[:, None] * a)    # [[1 2 3]
                         #  [2 4 6]
                         #  [3 6 9]]
A = np.array([[1, 2], [3, 4]])
print(A @ A)             # [[ 7 10]
                         #  [15 22]]
print(np.round(np.sqrt(a), 2))  # [1.   1.41 1.73]
```

## NumPy: aggregates & axis

- **Reductions:** `sum`, `mean`, `min`, `max`, `std`, `prod`, `argmin`, `argmax` (index of the min/max).
- **`axis=0`** collapses the rows (one result per column); **`axis=1`** collapses the columns (one result per row).
- **`keepdims=True`** keeps the reduced axis as size 1, so the result broadcasts back, e.g. `a / a.sum(axis=1, keepdims=True)`.
- **Running totals:** `np.cumsum(a)`.

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.sum())                 # 21
print(a.sum(axis=0))           # [5 7 9]
print(a.mean(axis=1))          # [2. 5.]
print(a.argmax(axis=1))        # [2 2]
print(a.sum(axis=1, keepdims=True).shape)  # (2, 1)
```

## NumPy: reshape, transpose, join & split

- **`a.reshape(r, c)`**: same data, new shape; `-1` means "work it out": `a.reshape(-1, 2)`.
- **`a.T`**: transpose. **`a.flatten()`**: a 1-D copy.
- **Join:** `np.concatenate([a, b], axis=0)` along an existing axis; `np.vstack` (as rows), `np.hstack` (side by side); `np.stack` adds a new axis.
- **Split:** `np.split(a, 2)` into equal parts.

```python
import numpy as np

a = np.arange(6)
print(a.reshape(2, -1))       # [[0 1 2]
                              #  [3 4 5]]
print(a.reshape(2, 3).T.shape)  # (3, 2)
b = np.array([[1, 2]])
print(np.vstack([b, b * 10])) # [[ 1  2]
                              #  [10 20]]
print(np.hstack([b, b]))      # [[1 2 1 2]]
```

## NumPy: sort, unique & random

- **`np.sort(a)`** returns a sorted copy; **`np.argsort(a)`** returns the indices that would sort it (reverse with `[::-1]`).
- **`np.unique(a, return_counts=True)`**: the distinct values and how often each appears.
- **Random:** `rng = np.random.default_rng(0)` (seeded, so the same every run), then `rng.integers(low, high, size)` (high excluded), `rng.random(size)`, `rng.normal(mean, std, size)`, `rng.choice(a, size)`, `rng.permutation(a)`.

```python
import numpy as np

a = np.array([30, 10, 20, 10])
print(np.sort(a))                # [10 10 20 30]
print(np.argsort(a)[::-1])       # [0 2 3 1]
vals, counts = np.unique(a, return_counts=True)
print(vals, counts)              # [10 20 30] [2 1 1]
rng = np.random.default_rng(0)
print(rng.integers(1, 7, size=5).shape)  # (5,)
```

## pandas: Series & DataFrame

- **Series:** one labelled column: values plus an **index** (the labels). `pd.Series({"a": 1, "b": 2})` uses the keys as the index.
- **DataFrame:** a table of columns sharing one index. `pd.DataFrame({"col": [...], ...})` builds it from a dict of columns.
- **Index:** `df.set_index("name")` makes a column the row labels; `df.reset_index()` turns them back into a column.
- **Convert:** `s.tolist()`, `s.to_dict()`, `df.to_numpy()`.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ann", "Ben", "Cy"], "age": [31, 25, 40]})
print(df.shape)           # (3, 2)
print(df.columns.tolist())  # ['name', 'age']
s = df.set_index("name")["age"]
print(s.to_dict())        # {'Ann': 31, 'Ben': 25, 'Cy': 40}
```

## pandas: load & inspect

- **Read a file:** `pd.read_csv("file.csv")`; `index_col="id"` uses a column as the index; `pd.read_csv(io.StringIO(text))` reads CSV text.
- **Look:** `df.head(n)`, `df.tail(n)`, `df.shape`, `df.dtypes`, `df.info()`.
- **Summaries:** `df.describe()` (count, mean, std, min, quartiles, max per number column), `s.value_counts()`, `s.nunique()`.

```python
import io
import pandas as pd

text = "id,city,temp\n1,Bonn,12\n2,Köln,15\n3,Bonn,9\n"
df = pd.read_csv(io.StringIO(text), index_col="id")
print(df.shape)                        # (3, 2)
print(df["city"].value_counts().to_dict())  # {'Bonn': 2, 'Köln': 1}
print(df["temp"].describe()["mean"])   # 12.0
```

## pandas: select rows & columns

- **Columns:** `df["col"]` (a Series), `df[["a", "b"]]` (a DataFrame).
- **`df.loc[rows, cols]`**: by **label**; label slices include the end: `df.loc["a":"c"]`.
- **`df.iloc[rows, cols]`**: by **position**, like Python slices (end excluded): `df.iloc[:2, -2:]`.
- **One value:** `df.loc[label, "col"]` or `df.at[label, "col"]`.

```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]}, index=["a", "b", "c"])
print(df.loc["b", "y"])                 # 5
print(df.loc["a":"b", ["x", "z"]].values.tolist())  # [[1, 7], [2, 8]]
print(df.iloc[:2, -2:].values.tolist())  # [[4, 7], [5, 8]]
print(df["x"].tolist())                 # [1, 2, 3]
```

## pandas: filter rows

- **Boolean mask:** `df[df["age"] > 30]` keeps the rows where the condition is `True`.
- **Several conditions:** `&`, `|`, `~` with each condition in brackets (`and` / `or` raise an error).
- **Membership:** `df["city"].isin(["Bonn", "Köln"])`. **Text:** `df["name"].str.contains("an")`.
- **`df.query("age > 30 and city == 'Bonn'")`** is the same filter written as a string.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ann", "Ben", "Cy", "Dana"], "age": [31, 25, 40, 35], "city": ["Bonn", "Köln", "Bonn", "Ulm"]})
print(df[df["age"] > 30]["name"].tolist())                             # ['Ann', 'Cy', 'Dana']
print(df[(df["age"] > 30) & (df["city"] == "Bonn")]["name"].tolist())  # ['Ann', 'Cy']
print(df[df["city"].isin(["Köln", "Ulm"])]["name"].tolist())           # ['Ben', 'Dana']
```

## pandas: add & change columns

- **New column:** `df["total"] = df["price"] * df["qty"]` (element-wise, aligned on the index).
- **Conditional:** `np.where(cond, a, b)`, or `s.map({"old": "new"})` / `s.apply(func)` for value by value.
- **Rename / drop:** `df.rename(columns={"a": "b"})`, `df.drop(columns=["c"])`.
- Methods return a new DataFrame; assign it back (`df = df.drop(...)`) instead of relying on `inplace=True`.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"price": [2.5, 10.0, 4.0], "qty": [4, 1, 0]})
df["total"] = df["price"] * df["qty"]
df["size"] = np.where(df["total"] >= 10, "big", "small")
print(df["total"].tolist())  # [10.0, 10.0, 0.0]
print(df["size"].tolist())   # ['big', 'big', 'small']
print(df.drop(columns=["qty"]).columns.tolist())  # ['price', 'total', 'size']
```

## pandas: missing data, types & cleaning

- **Find gaps:** `df.isna()` (True where missing), `df.isna().sum()` (missing per column).
- **Handle them:** `df.dropna()` (drop rows with any NaN; `subset=["col"]` for some columns), `df.fillna(value)` or `s.fillna(s.mean())`.
- **Types:** `s.astype(int)`, `pd.to_numeric(s, errors="coerce")` (bad values become NaN), `pd.to_datetime(s)`.
- **Text:** `s.str.strip()`, `.str.lower()`, `.str.replace("a", "b")`.
- **Duplicates:** `df.drop_duplicates()` (or `subset=["col"]`); clean text first so "Ann " and "ann" match.

```python
import pandas as pd

s = pd.Series([" Ann", "ann ", "Ben", None])
clean = s.str.strip().str.lower()
print(clean.isna().sum())                     # 1
print(clean.dropna().drop_duplicates().tolist())  # ['ann', 'ben']
n = pd.to_numeric(pd.Series(["3", "x", "5"]), errors="coerce")
print(n.fillna(0).tolist())                   # [3.0, 0.0, 5.0]
```

## pandas: sort & rank

- **`df.sort_values("col")`**; `ascending=False` for largest first; a list of columns sorts by the first, then ties by the next.
- **`df.sort_index()`** sorts by the row labels.
- **Top n:** `df.nlargest(n, "col")`, `df.nsmallest(n, "col")`.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ann", "Ben", "Cy"], "score": [80, 95, 80]})
print(df.sort_values("score", ascending=False)["name"].tolist())  # ['Ben', 'Ann', 'Cy']
print(df.sort_values(["score", "name"], ascending=[False, False])["name"].tolist())  # ['Ben', 'Cy', 'Ann']
print(df.nlargest(1, "score")["name"].tolist())  # ['Ben']
```

## pandas: groupby & aggregate

- **Split → apply → combine:** `df.groupby("key")["col"].mean()` gives one row per key.
- **Several stats:** `.agg(["mean", "count"])`, or named: `.agg(avg=("col", "mean"), n=("col", "count"))`.
- **Back to columns:** add `.reset_index()`; `as_index=False` does the same up front.
- **Per-row group value:** `df.groupby("key")["col"].transform("mean")` keeps the original number of rows.

```python
import pandas as pd

df = pd.DataFrame({"team": ["a", "b", "a", "b", "a"], "pts": [3, 5, 1, 7, 2]})
print(df.groupby("team")["pts"].sum().to_dict())  # {'a': 6, 'b': 12}
out = df.groupby("team").agg(avg=("pts", "mean"), n=("pts", "count")).reset_index()
print(out.values.tolist())                        # [['a', 2.0, 3], ['b', 6.0, 2]]
print(df.groupby("team")["pts"].transform("max").tolist())  # [3, 7, 3, 7, 3]
```

## pandas: merge & concat

- **`pd.merge(left, right, on="key", how="inner")`**: SQL-style join; `how` is `inner` (keys in both), `left`, `right` or `outer`.
- **Different key names:** `left_on="id", right_on="user_id"`.
- **`pd.concat([df1, df2])`** stacks rows (`ignore_index=True` renumbers); `axis=1` puts them side by side.

```python
import pandas as pd

users = pd.DataFrame({"id": [1, 2, 3], "name": ["Ann", "Ben", "Cy"]})
orders = pd.DataFrame({"id": [1, 1, 3], "amount": [10, 5, 7]})
print(pd.merge(users, orders, on="id")["name"].tolist())              # ['Ann', 'Ann', 'Cy']
print(pd.merge(users, orders, on="id", how="left")["amount"].isna().sum())  # 1
print(len(pd.concat([users, users], ignore_index=True)))              # 6
```
