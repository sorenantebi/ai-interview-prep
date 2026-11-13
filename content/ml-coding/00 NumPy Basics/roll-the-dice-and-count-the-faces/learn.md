# Learn: Roll the Dice and Count the Faces

## The idea

- The task: simulate `n` rolls of a fair six-sided die, then count how often each face (1 to 6) came up.
- You return both the raw rolls and the counts, as a tuple.
- Where it shows up in data work:
  - Counting class labels to check whether a dataset is balanced.
  - Building histograms of values.
  - Tallying predictions for an evaluation report.
- Seeded randomness matters because the same seed gives the same "random" numbers every time, so experiments and tests are reproducible.
- **Generator**: an object that produces random numbers.
  - You create it with a **seed**, a starting number that fixes the sequence it will produce.
- **Exclusive upper bound**: in `integers(low, high)`, `high` itself is never drawn.
  - So to get faces 1 to 6, the upper bound is not 6.
- **Slicing**: picking a part of an array with `a[start:stop]`.
- **Counting by index**: `np.bincount` stores the count of value `v` at position `v`.
  - That position-equals-value rule is the key to lining faces up with the output.

## Work it by hand

Example 1: `n = 0`, `seed = 0`.

1. Create the generator from seed 0.
2. Ask for 0 rolls.
   - The result is an empty integer array, shape `(0,)`. That is `rolls`.
3. Count the faces.
   - There is nothing to count, so every face has count 0.
4. The counts array must still have 6 entries, one per face, so its shape is `(6,)`.

| Step | Value | Shape |
|---|---|---|
| rolls | `[]` | `(0,)` |
| counts | `[0, 0, 0, 0, 0, 0]` | `(6,)` |

- Output: `([], [0,0,0,0,0,0])`.
- Check: `counts.sum() == 0 == n`.

A tiny case with rolls (made up, not a test):

- Suppose the rolls were `[2, 2, 5]`.
- Face 1 appears 0 times, face 2 twice, face 5 once.
- Counts: `[0, 2, 0, 0, 1, 0]`, which sum to 3, which is `n`.

## Tools you'll need

### np.random.default_rng(seed)

- Creates a random number generator.
- The same seed always gives the same numbers.

```python
import numpy as np

a = np.random.default_rng(42)
b = np.random.default_rng(42)
print(a.random() == b.random())  # True
```

### Generator.integers(low, high, size=...)

- Draws random whole numbers from `low` up to, but **not including**, `high`.
- `size` sets the output shape.

```python
import numpy as np

rng = np.random.default_rng(1)
x = rng.integers(10, 13, size=5)
print(x.shape)  # (5,)
print(x.min() >= 10 and x.max() <= 12)  # True
```

- Here the values can only be 10, 11 or 12.

### np.bincount(x, minlength=...)

- Counts how often each non-negative integer occurs.
  - Entry `i` of the result is the number of times `i` appears in `x`.
- The result has length `max(x) + 1`, or `minlength` if that is larger.
  - So `minlength` guarantees a minimum length, even for an empty input.
- Index 0 is counted too, because values start at 0.

```python
import numpy as np

x = np.array([0, 3, 3, 1])
print(np.bincount(x))                # [1 1 0 2]
print(np.bincount(x, minlength=6))   # [1 1 0 2 0 0]
print(np.bincount(np.array([], dtype=int), minlength=3))  # [0 0 0]
```

### Slicing: a[start:stop]

- Takes a part of an array.
  - `a[1:]` means "everything from index 1 on".
- The result is a view with a smaller shape.

```python
import numpy as np

a = np.array([7, 8, 9, 10])
print(a[1:])        # [ 8  9 10]
print(a[1:].shape)  # (3,)
print(a[:2])        # [7 8]
```

## Common mistakes

- **Using `integers(1, 6)`.**
  - The upper bound is exclusive, so 6 would never appear.
  - Follow the bounds the problem statement gives.
- **Off-by-one between faces and indices.**
  - `bincount` puts value `v` at index `v`, so face 1 lands at index 1, but the output needs face 1 at index 0.
  - Work out how to line them up.
- **Choosing the wrong `minlength`.**
  - If a face is missing at the top (say no 6 appears), `bincount` returns a shorter array unless `minlength` is big enough.
  - Decide the length you need before any slicing.
- **Drawing twice.**
  - A second call to `integers` gives different numbers and breaks the match with the tests.
  - Draw once and reuse the array.
- **Forgetting the empty case.**
  - With `n = 0`, `bincount` must still return the full length.
  - `minlength` handles this.

## Hints

### Hint 1
- Make a seeded generator.
- Draw all `n` rolls in one go.
- Count how many times each face appears.
- Return the rolls and the counts together as a tuple.

### Hint 2
- Generator: `np.random.default_rng(seed)`.
- Rolls: `integers` with size `n`, giving shape `(n,)`.
- Counts: `np.bincount` on the rolls with a `minlength`, giving a 1-D array.
- Trim the counts with a slice to reach shape `(6,)`.

### Hint 3
- `bincount` puts the count of value `v` at index `v`, so index 0 is for the value 0, which a die never shows.
- Set `minlength` to 7, so the result has indices 0 to 6.
  - Face 1 sits at index 1 and face 6 at index 6.
- Drop index 0 with a slice that starts at 1.
- You get exactly 6 entries, where entry `i` is the count of face `i + 1`.
