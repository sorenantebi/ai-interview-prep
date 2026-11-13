# Learn: Left Join and Fill

## The idea

- The task: attach each customer's `name` and `country` to every order, and mark orders with an unknown customer as `"unknown"`.
- It shows up in feature pipelines (enriching event logs with user attributes) and in reports (unmatched rows must not vanish silently).
- **Join** (or **merge**): match rows of two tables on a shared column.
  - That shared column is the **key**; here it is `customer_id`.
- **Left join**: keep every row of the left table (`orders`), even when the right table has no match.
  - Unmatched rows get `NaN` in the new columns.
- **NaN**: pandas' marker for a missing value.
  - You replace these gaps with a default afterwards.
- Each `customer_id` appears at most once in `customers`, so no order gets duplicated by the join.

## Work it by hand

Example 1: `orders` has 3 rows, `customers` has 2 rows.

1. Look up each order's `customer_id` in `customers`.
   - Order 1: key 10 matches `ana`, `DE`.
   - Order 2: key 99 has no match, so `name` and `country` are `NaN`.
   - Order 3: key 10 matches `ana`, `DE`.
2. Customer 11 (`ben`) is never asked for.
   - A left join drops right-side rows that no order uses.
3. The joined table has 3 rows and 5 columns, in the order of `orders`:

| order_id | customer_id | amount | name | country |
|---|---|---|---|---|
| 1 | 10 | 5.0 | ana | DE |
| 2 | 99 | 7.5 | NaN | NaN |
| 3 | 10 | 2.0 | ana | DE |

4. Replace `NaN` in `name` and `country` with `"unknown"`:

| order_id | customer_id | amount | name | country |
|---|---|---|---|---|
| 1 | 10 | 5.0 | ana | DE |
| 2 | 99 | 7.5 | unknown | unknown |
| 3 | 10 | 2.0 | ana | DE |

5. This matches the expected output: `name` is `["ana","unknown","ana"]` and `country` is `["DE","unknown","DE"]`.

## Tools you'll need

### df.merge(other, on=..., how=...)

- Joins two DataFrames on a key column.
  - `on` names the shared column.
  - `how="left"` keeps all rows of the left frame, in their original order.
- The default is `how="inner"`, which drops unmatched rows, so always be explicit.
- Columns from `other` are appended after the left frame's columns.

```python
import pandas as pd

a = pd.DataFrame({"k": [1, 2, 3], "x": [10, 20, 30]})
b = pd.DataFrame({"k": [3, 1], "y": ["c", "a"]})
print(a.merge(b, on="k", how="left"))
#    k   x    y
# 0  1  10    a
# 1  2  20  NaN
# 2  3  30    c
print(a.merge(b, on="k", how="inner").shape)  # (2, 3)
```

### Series.fillna(value) / DataFrame.fillna(value)

- Replaces `NaN` with the given value and returns a new object.
- Works on one column, or on several selected columns at once.
- It does not change the original unless you assign the result back.

```python
import pandas as pd

df = pd.DataFrame({"p": ["a", None], "q": [None, "d"], "r": [1, 2]})
print(df["p"].fillna("?").tolist())  # ['a', '?']
print(df[["p", "q"]].fillna("none").values.tolist())  # [['a', 'none'], ['none', 'd']]
```

### Selecting and assigning several columns

- `df[["p", "q"]]` (a list inside the brackets) picks several columns and gives a DataFrame.
- You can assign to the same list of columns to write values back.

```python
import pandas as pd

df = pd.DataFrame({"p": [1, 2], "q": [3, 4], "r": [5, 6]})
df[["p", "q"]] = df[["p", "q"]] * 10
print(df.columns.tolist())  # ['p', 'q', 'r']
print(df["p"].tolist())  # [10, 20]
```

## Common mistakes

- **Using the default join type.**
  - `merge` without `how="left"` is an inner join, so unknown customers disappear.
  - Always pass `how="left"`.
- **Filling the whole frame.**
  - Filling every column could touch `order_id`, `customer_id` or `amount` too.
  - Only fill `name` and `country`.
- **Discarding the result of `fillna`.**
  - It returns a new object, so calling it alone changes nothing.
  - Assign the result back.
- **Wrong column order.**
  - The result must be `order_id, customer_id, amount, name, country`.
  - A left merge gives this naturally; don't reorder or add extra columns.
- **Empty inputs.**
  - With zero orders, you should still return a frame with the five columns.
  - Avoid steps that assume at least one row.

## Hints

### Hint 1
- Join the two tables so every order keeps its row and gains the customer's name and country.
- Then replace the missing values in those two new columns with the default text.

### Hint 2
- Use `merge` with key `customer_id` and a left join; the result has the same rows as `orders` and 5 columns.
- Then use `fillna` on just the `name` and `country` columns.

### Hint 3
- After the left merge, unmatched orders have `NaN` in `name` and `country`.
- Select those two columns together as a list and call `fillna` with the string `"unknown"`.
- Assign that result back to the same two columns of the merged frame.
- Return that frame.
