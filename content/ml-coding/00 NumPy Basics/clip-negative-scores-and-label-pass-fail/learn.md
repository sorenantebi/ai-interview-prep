# Learn: Clip Negative Scores and Label Pass/Fail

## The idea

- The task has two steps on one array of scores.
  - First, **clean** it: replace every negative score with `0`.
  - Second, **label** it: compare each cleaned score to the pass mark and write `'pass'` or `'fail'`.
- Labels must come from the cleaned scores, not the raw ones.
- This shows up in two places in ML and data work.
  - A feature pipeline cleans impossible values before training.
  - An evaluation report turns numeric scores into readable labels.
- Working on the whole array at once is much faster than a Python `for` loop.
- **Boolean mask**: an array of `True`/`False` values, one per element, made by a comparison like `a < 0`.
- **Elementwise**: the operation is applied to each entry on its own, so the output has the same shape as the input.
- **Threshold**: the pass mark. A score at or above it passes.
- **Scalar**: a single value (like `0.0`) rather than an array.

## Work it by hand

Use Example 1: `scores = [-5.0, 55.5, 80.0]`, `threshold = 60.0`.

1. Find the negatives by checking `score < 0` for each entry. The mask has shape `(3,)`.

| index | score | score < 0 |
|---|---|---|
| 0 | -5.0 | True |
| 1 | 55.5 | False |
| 2 | 80.0 | False |

2. Build `clean`: where the mask is `True` use `0.0`, otherwise keep the score.
   - `clean = [0.0, 55.5, 80.0]`, shape `(3,)`.
3. Compare the cleaned scores to `60.0` with `>=`.

| index | clean | clean >= 60.0 | label |
|---|---|---|---|
| 0 | 0.0 | False | fail |
| 1 | 55.5 | False | fail |
| 2 | 80.0 | True | pass |

4. Turn the label array into a plain Python list: `['fail', 'fail', 'pass']`.
5. Return both pieces as a tuple: `([0.0, 55.5, 80.0], ['fail', 'fail', 'pass'])`.
   - This matches the expected output.

## Tools you'll need

### Comparison operators on arrays

- `a < 0` or `a >= 5` compares every element and returns a boolean array of the same shape.
- No loop is needed.

```python
import numpy as np

a = np.array([3.0, -1.0, 7.5, 5.0])
mask = a >= 5
print(mask)  # [False False  True  True]
print(mask.shape)  # (4,)
```

### np.where(cond, a, b)

- Builds a new array elementwise: where `cond` is `True` it takes the value from `a`, otherwise from `b`.
- `a` and `b` can be arrays or scalars. A scalar is repeated for every position.
- They can also be strings, which gives a string array.
- The original array is not changed.

```python
import numpy as np

x = np.array([10, -4, 3, -8])
print(np.where(x > 5, 100, x))  # [100  -4   3  -8]
print(np.where(x > 0, 'pos', 'nonpos'))  # ['pos' 'nonpos' 'pos' 'nonpos']
print(x)  # [10 -4  3 -8]
```

### .tolist()

- Converts a NumPy array into a normal Python list.
- For a string array you get plain Python `str` values.

```python
import numpy as np

w = np.array(['yes', 'no', 'yes'])
out = w.tolist()
print(out)  # ['yes', 'no', 'yes']
print(type(out))  # <class 'list'>
```

### Returning a tuple

- Separating values with a comma in `return` packs them into a tuple.
- The caller can unpack them into separate names.

```python
def two_things():
    return 1, [2, 3]

a, b = two_things()
print(a, b)  # 1 [2, 3]
```

## Common mistakes

- **Using `>` instead of `>=`.**
  - A score equal to the threshold must pass (Example 2).
  - Use `>=`.
- **Labelling the raw scores.**
  - Labels come from the cleaned array.
  - In Example 3, `-3.0` becomes `0.0`, which meets a threshold of `0.0`, so it passes.
- **Returning a NumPy array for labels.**
  - The problem asks for a Python `list[str]`.
  - Convert with `.tolist()`.
- **Changing the input in place.**
  - Build a new array instead of assigning into `scores`.
  - The caller may still need the original data.
- **Mixing up the `np.where` argument order.**
  - It is condition, value if true, value if false.
  - Swapping the values flips your results.

## Hints

### Hint 1
- Make a mask of the negative scores.
- Use it to build a cleaned array where those entries are zero.
- Compare the cleaned array to the threshold and turn each result into a word.
- Convert the words to a plain list.
- Return both pieces.

### Hint 2
- Cleaning: use `np.where` with the condition "score is negative". The result has shape `(n,)`.
- Labelling: use `np.where` again, with a condition on the cleaned array and two strings as values. The result is a string array of shape `(n,)`.
- Convert the string array with `.tolist()` to get a list of length `n`.

### Hint 3
- First `np.where`: where the score is below 0, give `0.0`; otherwise keep the score.
- Second `np.where`: where the cleaned score is greater than or equal to the threshold, give `'pass'`; otherwise `'fail'`.
- The second comparison must use the cleaned array, not the original.
- Return the cleaned array and the list together as a tuple.
