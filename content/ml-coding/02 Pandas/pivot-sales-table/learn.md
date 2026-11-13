# Learn: Pivot a Sales Table

## The idea

- The task: turn a list of individual sales into a grid with one row per region and one column per month.
- Each cell holds the total `amount` for that region and month, or `0` if nothing was sold.
- This shape shows up in feature tables (one row per user, one column per category) and in evaluation reports (one row per model, one column per metric).
- **Long format**: one row per observation, with the region, month and amount written out in every row.
- **Wide format**: one row per entity, one column per category, one value per cell.
- **groupby**: collect all rows that share the same key, then combine them (here, add them up).
- **Pivot**: take the values of one column and spread them out as column headers.
- **Aggregation**: the rule for combining duplicates, such as sum or mean.
- Pairs that never occurred have no data, so they must be filled with `0`.

## Work it by hand

Input rows (long format):

| region | month   | amount |
|--------|---------|--------|
| east   | 2024-02 | 5.0    |
| west   | 2024-01 | 3.0    |
| east   | 2024-01 | 2.0    |
| east   | 2024-02 | 1.0    |

1. Group by (region, month) and sum the amounts:
   - (east, 2024-01) gives 2.0.
   - (east, 2024-02) gives 5.0 + 1.0 = 6.0.
   - (west, 2024-01) gives 3.0.
2. List the keys, sorted:
   - Regions: `east`, `west`.
   - Months: `2024-01`, `2024-02`.
   - The grid is 2 rows by 2 month columns.
3. Fill the grid:
   - east: 2.0 and 6.0.
   - west: 3.0 and missing (no sale in `2024-02`).
4. Replace the missing cell with `0`, so west becomes 3.0 and 0.0.
5. Make `region` an ordinary first column with index `0, 1`, and make sure the header has no extra label.
6. Final result, 2 rows by 3 columns:

```text
region: ["east", "west"]
2024-01: [2.0, 3.0]
2024-02: [6.0, 0.0]
```

## Tools you'll need

### df.pivot_table(index, columns, values, aggfunc, fill_value)

- Groups rows, aggregates them, and spreads one key across the columns.
- `index` gives the rows, `columns` gives the headers, `values` is the column to aggregate.
- `aggfunc` says how to combine duplicates (`"sum"`, `"mean"`, ...). The default is the mean.
- `fill_value` replaces combinations that never occurred (otherwise `NaN`).
- Rows and columns come out sorted by their keys.

```python
import pandas as pd

d = pd.DataFrame({"shop": ["a", "b", "a", "a"],
                  "day": ["mon", "mon", "tue", "tue"],
                  "qty": [1, 4, 2, 3]})
t = d.pivot_table(index="shop", columns="day", values="qty", aggfunc="sum", fill_value=0)
print(t.shape)  # (2, 2)
print(t.loc["a", "tue"])  # 5
print(t.loc["b", "tue"])  # 0
```

### df.reset_index()

- Moves the index back into a normal column and replaces it with `0..n-1`.
- After a pivot the row keys live in the index, so this brings them back as a column.

```python
import pandas as pd

t = pd.DataFrame({"x": [1, 2]}, index=pd.Index(["p", "q"], name="key"))
r = t.reset_index()
print(list(r.columns))  # ['key', 'x']
print(list(r.index))  # [0, 1]
```

### df.columns.name

- After a pivot, the column labels carry a name (the `columns=` key). It shows up as an extra header label.
- Setting it to `None` removes it.

```python
import pandas as pd

d = pd.DataFrame({"k": ["a", "b"], "c": ["u", "v"], "n": [1, 2]})
t = d.pivot_table(index="k", columns="c", values="n", aggfunc="sum")
print(t.columns.name)  # c
t.columns.name = None
print(t.columns.name)  # None
```

### df.groupby(...).sum() with unstack (alternative)

- `groupby` on two keys, then `.unstack()`, also pivots: the inner index level becomes the columns.
- Missing cells are `NaN` unless you pass `fill_value` to `unstack`.

```python
import pandas as pd

d = pd.DataFrame({"k": ["a", "a", "b"], "c": ["u", "v", "u"], "n": [1, 2, 3]})
w = d.groupby(["k", "c"])["n"].sum().unstack(fill_value=0)
print(w.shape)  # (2, 2)
print(w.loc["b", "v"])  # 0
```

## Common mistakes

- **Forgetting the fill value.** Missing combinations become `NaN`, not `0`. Pass `fill_value=0`.
- **Leaving `region` as the index.** The output needs `region` as the first column and a plain `0..n-1` index. Call `reset_index()`.
- **Keeping the columns' axis name.** The header would show `month` as an extra label. Set `columns.name = None`.
- **Relying on the default aggregation.** `pivot_table` averages by default, so duplicate rows give means instead of totals. Use `aggfunc="sum"`.
- **Using `pivot` instead of `pivot_table`.** `pivot` raises an error on duplicate (region, month) pairs and can't sum. Use `pivot_table`.

## Hints

### Hint 1
- Group the sales by region and month and add up the amounts.
- Spread the months across as columns, filling gaps with zero.
- Turn the region labels back into an ordinary first column.

### Hint 2
- One `pivot_table` call does the grouping, summing, spreading and zero-filling, and sorts rows and columns. The result is `regions × months` with `region` as the index.
- Clear the column-axis name so the header is just month strings.
- Use `reset_index()` so the shape becomes `regions × (1 + months)`.

### Hint 3
- In `pivot_table`, `index` is `"region"`, `columns` is `"month"`, and `values` is `"amount"`.
- Set the aggregation to sum and the fill value to 0.
- The pivoted result's column labels still carry the name `month`, so set that name to `None`.
- Last, reset the index so `region` becomes the first column and the index is `0..n-1`.
