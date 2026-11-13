# Learn: Precision, Recall and F1

## The idea

- The task: compare predicted labels to true labels and turn the comparison into three scores.
- A **binary classifier** says `1` (positive) or `0` (negative) for each item.
- Accuracy alone can hide problems.
  - If only 1% of emails are spam, a model that never flags anything is 99% accurate and useless.
- Precision, recall and F1 give a fairer picture. They appear in almost every classifier evaluation report, especially when one class is rare.
- Everything starts from three counts:
  - **True positive (TP):** predicted 1, truth is 1. A correct alarm.
  - **False positive (FP):** predicted 1, truth is 0. A false alarm.
  - **False negative (FN):** predicted 0, truth is 1. A missed case.
- **Precision** asks: "Of everything I flagged, how much was really positive?"
- **Recall** asks: "Of everything that was really positive, how much did I find?"
- **F1** is the harmonic mean of precision and recall.
  - It is high only when both are high, so one good number can't hide a bad one.
- **Guard:** when a denominator would be 0, the ratio is undefined.
  - This problem says to return `0.0` in that case.

## Work it by hand

Example 1: `y_true = [1, 0, 1, 1, 0]`, `y_pred = [1, 1, 0, 1, 0]`.

1. Compare position by position:

| i | true | pred | outcome |
|---|------|------|---------|
| 0 | 1 | 1 | TP |
| 1 | 0 | 1 | FP |
| 2 | 1 | 0 | FN |
| 3 | 1 | 1 | TP |
| 4 | 0 | 0 | true negative (not used) |

2. Counts: TP = 2, FP = 1, FN = 1.
3. Precision = TP / (TP + FP) = 2 / 3 = 0.66667.
4. Recall = TP / (TP + FN) = 2 / 3 = 0.66667.
5. F1 = 2 · 0.66667 · 0.66667 / (0.66667 + 0.66667) = 0.88889 / 1.33333 = 0.66667.
6. Output: `[0.66667, 0.66667, 0.66667]`.

The guard, Example 2: `y_true = [0, 0, 1]`, `y_pred = [0, 0, 0]`.

1. TP = 0, FP = 0, FN = 1.
2. Precision: the denominator is 0, so it is `0.0`.
3. Recall: 0 / 1 = `0.0`.
4. `precision + recall` is 0, so F1 is `0.0`.

## Tools you'll need

### Comparison on arrays: `a == 1`

- Comparing a NumPy array to a number gives a boolean array of the same shape.
- You get one True/False per element.

```python
import numpy as np
a = np.array([2, 1, 1, 0])
print(a == 1)  # [False  True  True False]
print((a == 1).shape)  # (4,)
```

### Combining masks with `&`

- `&` is the element-wise "and" for boolean arrays.
- Use it instead of the word `and`, which fails on arrays.
- Wrap each comparison in parentheses, because `&` binds more tightly than `==`.

```python
import numpy as np
x = np.array([1, 1, 0, 0])
y = np.array([1, 0, 1, 0])
print((x == 1) & (y == 0))  # [False  True False False]
```

### `np.sum(mask)`

- Summing a boolean array counts the Trues, since True is 1 and False is 0.
- The result is a NumPy integer. `int(...)` turns it into a plain Python int.

```python
import numpy as np
m = np.array([True, False, True, True])
print(np.sum(m))  # 3
print(int(m.sum()))  # 3
```

### Conditional expression: `a / b if b else 0.0`

- Python's one-line `if` picks a value.
- A denominator of 0 counts as false, so the guard needs no explicit comparison.
- Only the chosen branch is evaluated, so the division by zero never happens.

```python
total = 0
print(5 / total if total else 0.0)  # 0.0
total = 4
print(5 / total if total else 0.0)  # 1.25
```

### Returning a list of floats

- Build the result as a plain list.
- `/` always gives a float, so mixing in NumPy integers is fine.

```python
a, b = 3, 4
print([a / b, b / a])  # [0.75, 1.3333333333333333]
```

## Common mistakes

- **Guarding the wrong thing.** Check the denominator (`tp + fp`), not `tp`.
  - TP can be 0 while the denominator is not. The division then gives a legitimate `0.0`.
- **Using `and` instead of `&` on arrays.** Python's `and` raises an error for arrays with more than one element.
  - Use `&` with parentheses around each comparison.
- **Forgetting the F1 guard.** Both precision and recall can be 0, making `precision + recall` zero.
  - Check it before dividing.
- **Mixing up FP and FN.** FP: predicted 1, truth 0. FN: predicted 0, truth 1.
  - Say each aloud as "predicted ..., truth ...".
- **Rounding early.** Keep full precision in intermediate values.
  - Return plain floats, not strings or rounded values.

## Hints

### Hint 1
- Count three things by comparing the two label arrays: correct alarms, false alarms and misses.
- Turn the counts into precision and recall, checking each time that the denominator isn't 0.
- Combine precision and recall into F1 with the same kind of check.
- Return the three values in order.

### Hint 2
- Build one boolean mask per count by comparing `y_pred` and `y_true` to 0 or 1 and joining the two comparisons with `&`. Each mask has shape `(n,)`.
- Sum each mask to get a single integer count.
- Use a one-line `x / y if y else 0.0` for precision and recall.
- Use the same pattern for F1. The result is a list of 3 floats.

### Hint 3
- TP: positions where pred is 1 and true is 1. FP: pred is 1 and true is 0. FN: pred is 0 and true is 1.
- Precision is TP divided by (TP + FP). Recall is TP divided by (TP + FN). Each is 0.0 if its denominator is 0.
- F1 is 2 times precision times recall, divided by (precision + recall). It is 0.0 if that sum is 0.
- Return the values in the order precision, recall, F1.
