---
topic: "Pandas Basics"
difficulty: Easy
---
# Load a CSV Table with an Index Column

**Topic:** Pandas Basics · **Difficulty:** Easy

## Problem

Write a function `load_table(text, index_col)` that receives the contents of a CSV file as a string `text` (first line is the header) and the name of one of its columns, `index_col`. It must return a `pd.DataFrame` that:

1. is parsed from `text`, with the column `index_col` used as the row index (not kept as a normal column), and
2. contains only the rows that have no missing values in any of the remaining columns.

The row order of the input is preserved.

Calls to practise: `pd.read_csv` on an `io.StringIO(text)` object with its `index_col` argument, and `DataFrame.dropna`.

Don't write Python loops over the rows or parse the text by hand.

## Examples

**Example 1**
```text
Input: text = "item,price,stock\napple,1.5,10\npear,2.0,4\nplum,0.8,25\n", index_col = "item"
Output: {"price":{"apple":1.50000,"pear":2.00000,"plum":0.80000},"stock":{"apple":10,"pear":4,"plum":25}}
Explanation: "item" becomes the index, so only price and stock remain as columns.
```

**Example 2**
```text
Input: text = "id,temp,humidity\ns1,20.5,40\ns2,,55\ns3,19.0,\ns4,21.5,38\n", index_col = "id"
Output: {"temp":{"s1":20.50000,"s4":21.50000},"humidity":{"s1":40.00000,"s4":38.00000}}
Explanation: s2 has no temp and s3 has no humidity, so both rows are dropped.
```

**Example 3**
```text
Input: text = "k,v\na,1\n", index_col = "k"
Output: {"v":{"a":1}}
```

## Constraints

- `text` is valid CSV with a header line and at least one data row.
- `index_col` is the name of one of the header columns.
- Missing values are empty fields.
- At most `10^4` rows.
