# Learn: K-Fold Indices

## The idea

- **Cross-validation** checks how well a model works on data it has not seen before.
- You cut your samples into `k` groups called **folds**, then run `k` rounds.
  - In each round, one fold is the **validation set**, used to score the model.
  - The other `k - 1` folds together are the **training set**, used to fit the model.
  - Every sample is in validation exactly once.
- It shows up in model selection and evaluation reports, where the `k` scores are averaged.
- Here you only produce the indices, not the model.
- **Without shuffling** means each fold is a consecutive block in the original order.
- The tricky part is when `n` doesn't divide evenly by `k`.
  - **Integer division** (`n // k`) divides and rounds down, giving the base fold size.
  - The **remainder** (`n % k`) is what is left over.
  - The leftover is handed out one index each to the first `n % k` folds, so those folds are one bigger.
- The output is a list of `[train, val]` pairs, one per fold, with train first.

## Work it by hand

Example 1: `n = 5`, `k = 2`.

1. Base size: `5 // 2 = 2`. Remainder: `5 % 2 = 1`.
2. The first 1 fold gets an extra index, so the sizes are `[3, 2]`, which add up to 5.
3. All indices: `0 1 2 3 4`.
4. Fold 0 starts at 0 with size 3, so val is `[0, 1, 2]` and train is the rest, `[3, 4]`.
5. Fold 1 starts at 3 (where the last block ended) with size 2, so val is `[3, 4]` and train is `[0, 1, 2]`.

| fold | start | size | val | train |
|------|-------|------|-----------|-----------|
| 0 | 0 | 3 | `[0,1,2]` | `[3,4]` |
| 1 | 3 | 2 | `[3,4]` | `[0,1,2]` |

- Each result item is `[train, val]`, so the final answer is:

```text
[[[3,4],[0,1,2]],[[0,1,2],[3,4]]]
```

- This matches the expected output.

## Tools you'll need

### `//` and `%`
- `//` divides and rounds down; `%` gives the remainder.
- Together they split a total into equal parts plus a leftover.

```python
print(17 // 5)  # 3
print(17 % 5)   # 2
```

### `range(a, b)`
- Gives the integers from `a` up to but **not including** `b`, in increasing order.
- If `a >= b` it is empty. Wrap it in `list(...)` to get a real list.

```python
print(list(range(2, 6)))  # [2, 3, 4, 5]
print(list(range(4, 4)))  # []
```

### List concatenation with `+`
- Joins two lists into a new one, keeping order.
- Useful for gluing a "before" piece and an "after" piece.

```python
a = [10, 11]
b = [20, 21, 22]
print(a + b)  # [10, 11, 20, 21, 22]
```

### Conditional expression
- `x if cond else y` picks one of two values.
- It works inside a list comprehension, which is handy for building per-fold sizes.

```python
sizes = [4 + (1 if i < 2 else 0) for i in range(4)]
print(sizes)  # [5, 5, 4, 4]
```

### A running total
- Keep a variable that grows as you go, so each block starts where the last one ended.

```python
start = 0
for size in [2, 3, 1]:
    print(start, start + size)
    start += size
# 0 2
# 2 5
# 5 6
```

## Common mistakes

- **Forgetting the remainder.** Using `n // k` for every fold loses indices when `n % k > 0`; give the first `n % k` folds one extra.
- **Extras on the wrong folds.** They go to the *first* folds, not the last; for `n = 7`, `k = 3` the sizes are `[3, 2, 2]`.
- **Swapped pair order.** The output is `[train, val]`, not `[val, train]`.
- **Off-by-one at block edges.** `range` excludes its end, so a block ends at `start + size` (exclusive), and the "after" part of train begins at that same number.
- **Not advancing the start.** Move the running start forward after each fold, or every fold will validate on the first block.

## Hints

### Hint 1
- Work out the size of every fold: a base size, plus one extra for the first few.
- Go through the folds in order, remembering where each block starts.
- The validation set is the fold's block.
- The training set is all indices before the block, followed by all indices after it.

### Hint 2
- Use `n // k` and `n % k` to build a list of `k` sizes (a list of ints).
- Loop over the sizes with a running `start`.
- Build `val` from one `range` (a list of `size` ints).
- Build `train` from two `range`s joined with `+` (a list of `n - size` ints).
- Append `[train, val]`, then move `start` forward by the size.

### Hint 3
- For fold `i`, the size is `n // k`, plus 1 if `i < n % k`.
- Validation indices run from `start` up to but not including `start + size`.
- Training indices are `0` up to but not including `start`, followed by `start + size` up to but not including `n`.
- After the fold, set `start` to `start + size`; that is where the next block begins.
