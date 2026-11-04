---
topic: "Pandas Basics"
difficulty: Easy
---
# Fix the Column Types

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

A small shop table was loaded from a CSV file, so every column came in with the wrong data type. Write `fix_dtypes(df)`, which receives a `pd.DataFrame` with the columns `item`, `price`, `member` and `count`, and returns a new DataFrame in which:

- `price` (strings such as `"1.50"`) is converted to numbers (`float64`). Strings that are not numbers, such as `"n/a"`, become `NaN`.
- `member` (the strings `"yes"` / `"no"`) is converted to `bool` (`"yes"` becomes `True`, `"no"` becomes `False`).
- `count` (`int64`) is converted to `float64`.
- `item` is left unchanged.

The column order and the index must stay the same, and the input DataFrame must not be modified.

Calls to practise: `pd.to_numeric` (look at its `errors` argument), `Series.map` with a dict, `Series.astype`. The whole solution fits in 1-3 lines.

## Examples

**Example 1**
```text
Input: df = {"item": ["pen", "ink", "pad"], "price": ["1.50", "2.00", "10.25"], "member": ["yes", "no", "yes"], "count": [3, 0, 12]}
Output: {"item":["pen","ink","pad"],"price":[1.50000,2.00000,10.25000],"member":[true,false,true],"count":[3.00000,0.00000,12.00000]}
```

**Example 2**
```text
Input: df = {"item": ["cap", "hat"], "price": ["n/a", "7.00"], "member": ["no", "no"], "count": [5, 1]}
Output: {"item":["cap","hat"],"price":[null,7.00000],"member":[false,false],"count":[5.00000,1.00000]}
Explanation: "n/a" is not a number, so it becomes NaN (null).
```

## Constraints

- `1 <= len(df) <= 10^3`
- `member` only contains `"yes"` and `"no"`.
- Every `price` string either contains a decimal point (e.g. `"2.00"`) or is not a number at all.
