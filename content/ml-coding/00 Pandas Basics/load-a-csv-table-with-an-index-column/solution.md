---
topic: "Pandas Basics"
difficulty: Easy
---
# Load a CSV Table with an Index Column - Solution

## Intuition

`pd.read_csv` accepts any file-like object, so wrapping the string in `io.StringIO` lets us parse it without touching the disk. Its `index_col` argument turns a column into the index while reading, and empty fields are read as `NaN`, which `dropna` removes row-wise.

## Approach

1. Wrap `text` in `io.StringIO` and call `pd.read_csv(..., index_col=index_col)`.
2. Call `.dropna()` on the result to remove every row containing a `NaN`.
3. Return the frame.

## Code

```python
import io

import pandas as pd

def load_table(text: str, index_col: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text), index_col=index_col)
    return df.dropna()
```

## Complexity

Time and memory are linear in the size of the text.
