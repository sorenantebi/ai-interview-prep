---
topic: "Pandas Basics"
difficulty: Easy
---
# Select Rows and Columns with .loc

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

You get a `pd.DataFrame` `df` with a `name` column (unique strings), a list `names` of index labels, and a list `columns` of column labels.

Make `name` the index, then return a new `pd.DataFrame` that contains only the rows listed in `names` and only the columns listed in `columns`. Rows must appear in the order of `names`, columns in the order of `columns`. The result is indexed by name. If a name appears twice in `names`, its row appears twice.

Calls to practise: `df.set_index("name")`, then label-based selection with `.loc[row_labels, column_labels]`, passing **lists** for both axes so the result is always a DataFrame (a single label would give you a Series or a scalar). The intended solution is one or two lines. Don't loop over the rows.

## Examples

**Example 1**
```text
Input: df = {"name": ["Anna", "Ben", "Cara", "Dev"], "age": [34, 28, 45, 39], "city": ["Bonn", "Koeln", "Essen", "Ulm"], "score": [88.5, 92.0, 79.5, 85.0]}, names = ["Cara", "Anna"], columns = ["score", "age"]
Output: {"name":["Cara","Anna"],"score":[79.50000,88.50000],"age":[45,34]}
Explanation: After `set_index("name")` the index is ["Anna", "Ben", "Cara", "Dev"]. The rows come back in the order Cara, Anna, and the columns in the order score, age.
```

**Example 2**
```text
Input: df = {"name": ["Anna", "Ben", "Cara", "Dev"], "age": [34, 28, 45, 39], "city": ["Bonn", "Koeln", "Essen", "Ulm"], "score": [88.5, 92.0, 79.5, 85.0]}, names = ["Ben"], columns = ["city"]
Output: {"name":["Ben"],"city":["Koeln"]}
Explanation: Same df and index as Example 1. A one-element list still gives a DataFrame (1 row, 1 column).
```

**Example 3**
```text
Input: df = {"name": ["Anna", "Ben", "Cara", "Dev"], "age": [34, 28, 45, 39], "city": ["Bonn", "Koeln", "Essen", "Ulm"], "score": [88.5, 92.0, 79.5, 85.0]}, names = ["Dev", "Dev"], columns = ["age"]
Output: {"name":["Dev","Dev"],"age":[39,39]}
Explanation: Same df and index as Example 1. The repeated name gives a repeated row (index ["Dev", "Dev"]).
```

## Constraints

- `1 <= len(df) <= 10^3`, the names are unique
- `1 <= len(names)`, `1 <= len(columns)`
- Every entry of `names` is in `df["name"]`, every entry of `columns` is in `df.columns`
